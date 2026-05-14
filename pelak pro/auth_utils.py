import sqlite3
import hashlib
import os
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

# --- Configuration ---
# این فرض می‌کند که دیتابیس اصلی شما mydata.db نام دارد.
DB_NAME = "mydata.db"
PASSWORD_HASH_ITERATIONS = 100000
SALT_SIZE = 16
LOGIN_ATTEMPTS_BEFORE_LOCKOUT = 3
LOCKOUT_DURATION_SECONDS = 60 # 1 دقیقه

# --- Database Schema Check ---
# این تابع چک می‌کند که آیا جدول 'users' وجود دارد یا نه.
# اگر وجود ندارد، آن را با ساختار مناسب ایجاد می‌کند.
# ساختار جدول 'users':
# id: کلید اصلی (از جدول اصلی شما یا مجزا)
# username: نام کاربری برای ورود (UNIQUE)
# password_hash: هش شده رمز عبور
# last_login_attempt: زمان آخرین تلاش ناموفق برای ورود (برای قفل کردن حساب)
# failed_login_attempts: تعداد تلاش‌های ناموفق پشت سر هم
def initialize_auth_schema():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Try to create the users table if it doesn't exist
        # We assume 'id' might be linked to your main table or a separate auth ID
        # For simplicity, let's use a separate 'auth_id' or make username the primary key if unique
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY NOT NULL,
                password_hash BLOB NOT NULL,
                last_login_attempt TIMESTAMP NULL,
                failed_login_attempts INTEGER DEFAULT 0
            )
        """)
        # If you want to link to an existing ID from your main table,
        # you would need to pass that ID during user creation and adjust the schema/queries.
        # For now, username is the unique identifier.

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error during schema initialization: {e}")
    finally:
        conn.close()

# --- Password Hashing Utilities ---
def hash_password(password: str) -> bytes:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a random salt."""
    salt = os.urandom(SALT_SIZE)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_HASH_ITERATIONS
    )
    return salt + pwd_hash # Store salt prefixed to the hash

def verify_password(password: str, stored_value: bytes) -> bool:
    """Verifies a password against a stored salt and hash."""
    if not stored_value or len(stored_value) < SALT_SIZE:
        return False # Invalid stored value

    salt = stored_value[:SALT_SIZE]
    stored_hash = stored_value[SALT_SIZE:]

    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_HASH_ITERATIONS
    )

    return new_hash == stored_hash

# --- Authentication Database Functions ---

def add_user(username: str, password: str, db_conn=None) -> tuple[bool, str]:
    """Adds a new user with a hashed password to the auth table."""
    conn = db_conn if db_conn else sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        if not username or not password:
            return False, "Username and password cannot be empty."

        # Check if username already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            return False, "Username already exists."

        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, pwd_hash)
        )
        if not db_conn: # Commit only if we opened the connection here
            conn.commit()
        return True, "User created successfully."
    except sqlite3.Error as e:
        # Rollback if an error occurs and we are managing the connection
        if not db_conn:
            conn.rollback()
        return False, f"Database error: {e}"
    except Exception as e:
        if not db_conn:
            conn.rollback()
        return False, f"An unexpected error occurred: {e}"
    finally:
        if not db_conn: # Close connection only if we opened it
            conn.close()

def create_default_admin_if_not_exists():
    """Creates a default admin user ('admin'/'admin123') if the username 'admin' does not exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT username FROM users WHERE username = ?", ("admin",))
        if cursor.fetchone() is None:
            print("Creating default admin user (username: admin, password: admin123)")
            add_user("admin", "admin123", conn) # Use the add_user function with the connection
            conn.commit() # Commit after add_user completes
            print("Default admin created.")
        else:
            print("Admin user already exists.")
    except sqlite3.Error as e:
        print(f"Error setting up default admin: {e}")
        conn.rollback()
    finally:
        conn.close()

def check_login(username: str, password: str, db_conn=None) -> tuple[bool, str | None]:
    """
    Checks if the provided username and password are valid.
    Returns (True, username) on success, (False, error_message) on failure.
    Handles lockout logic.
    """
    conn = db_conn if db_conn else sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    error_message = None
    success = False
    logged_in_username = None

    try:
        # Fetch user details
        cursor.execute(
            "SELECT password_hash, last_login_attempt, failed_login_attempts FROM users WHERE username = ?",
            (username,)
        )
        user_data = cursor.fetchone()

        if user_data is None:
            error_message = "Invalid username or password."
        else:
            stored_hash, last_attempt_ts, failed_attempts = user_data
            current_time = datetime.now()

            # Check lockout status
            lockout_until = None
            if last_attempt_ts:
                last_attempt_dt = datetime.strptime(last_attempt_ts, "%Y-%m-%d %H:%M:%S")
                if current_time < last_attempt_dt + timedelta(seconds=LOCKOUT_DURATION_SECONDS):
                    # Account is still locked
                    lockout_end_time = last_attempt_dt + timedelta(seconds=LOCKOUT_DURATION_SECONDS)
                    remaining_seconds = max(0, (lockout_end_time - current_time).total_seconds())
                    error_message = f"Account locked. Please try again in {int(remaining_seconds)} seconds."
                else:
                    # Lockout period has passed, reset attempts
                    cursor.execute("""
                        UPDATE users SET failed_login_attempts = 0, last_login_attempt = NULL
                        WHERE username = ?
                    """, (username,))
                    failed_attempts = 0 # Update local variable

            # If not locked, proceed with password verification
            if error_message is None: # Check if account is not locked
                if verify_password(password, stored_hash):
                    # Login successful
                    success = True
                    logged_in_username = username
                    # Reset failed attempts on successful login
                    cursor.execute("""
                        UPDATE users SET failed_login_attempts = 0, last_login_attempt = NULL
                        WHERE username = ?
                    """, (username,))
                else:
                    # Password incorrect
                    failed_attempts += 1
                    cursor.execute("""
                        UPDATE users SET failed_login_attempts = ?, last_login_attempt = ?
                        WHERE username = ?
                    """, (failed_attempts, current_time.strftime("%Y-%m-%d %H:%M:%S"), username))

                    if failed_attempts >= LOGIN_ATTEMPTS_BEFORE_LOCKOUT:
                        # Lock the account
                        lockout_end_time = current_time + timedelta(seconds=LOCKOUT_DURATION_SECONDS)
                        error_message = f"Invalid password. Too many attempts. Account locked for {LOCKOUT_DURATION_SECONDS} seconds."
                    else:
                        error_message = f"Invalid password. {LOGIN_ATTEMPTS_BEFORE_LOCKOUT - failed_attempts} attempts remaining."

        if not db_conn: # Commit changes if we managed the connection
            conn.commit()

    except sqlite3.Error as e:
        if not db_conn:
            conn.rollback()
        error_message = f"Database error during login check: {e}"
        print(error_message)
    except Exception as e:
        if not db_conn:
            conn.rollback()
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
    finally:
        if not db_conn: # Close connection only if we opened it
            conn.close()

    if success:
        return True, logged_in_username
    else:
        return False, error_message


# --- Login Screen UI Components ---
class LoginScreen(BoxLayout):
    def __init__(self, on_login_success=None, on_registration_success=None, **kwargs):
        super().__init__(orientation="vertical", spacing=10, padding=25, **kwargs)
        self.on_login_success = on_login_success
        self.on_registration_success = on_registration_success

        # Ensure DB schema is ready before building UI
        initialize_auth_schema()
        create_default_admin_if_not_exists()

        self.build_ui()

    def build_ui(self):
        self.clear_widgets() # Clear previous widgets

        self.add_widget(Label(text="Secure Application", font_size='30sp', size_hint_y=None, height='50dp'))
        self.add_widget(Label(text="Login", font_size='24sp', size_hint_y=None, height='40dp'))

        self.username_input = TextInput(
            hint_text="Username", multiline=False, font_size='18sp', size_hint_y=None, height='45dp',
            padding=(10, 10, 10, 10) # left, top, right, bottom
        )
        self.add_widget(self.username_input)

        self.password_input = TextInput(
            hint_text="Password", multiline=False, password=True, font_size='18sp', size_hint_y=None, height='45dp',
            padding=(10, 10, 10, 10)
        )
        self.add_widget(self.password_input)

        login_btn = Button(
            text="Login",
            font_size='20sp',
            size_hint_y=None,
            height='50dp',
            background_color=(0.2, 0.6, 0.9, 1), # Blueish
            color=(1, 1, 1, 1)
        )
        login_btn.bind(on_press=self.attempt_login)
        self.add_widget(login_btn)

        self.error_label = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height='30dp')
        self.add_widget(self.error_label)

        register_btn = Button(
            text="Create New Account",
            font_size='16sp',
            size_hint_y=None,
            height='45dp',
            background_color=(0.5, 0.5, 0.5, 1), # Gray
            color=(1, 1, 1, 1)
        )
        register_btn.bind(on_press=self.show_registration_popup)
        self.add_widget(register_btn)

    def show_popup(self, title, message, is_error=True, callback=None):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message, color=(1, 0, 0, 1) if is_error else (0, 0, 0, 1)))
        close_btn = Button(text="Close", size_hint_y=None, height='40dp')
        close_btn.bind(on_press=lambda *args: self.dismiss_popup_and_callback(popup, callback))
        content.add_widget(close_btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.7, 0.4),
            auto_dismiss=False # Prevent closing by clicking outside
        )
        popup.open()

    def dismiss_popup_and_callback(self, popup_instance, callback=None):
        popup_instance.dismiss()
        if callback:
            callback()

    def attempt_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        self.error_label.text = "" # Clear previous errors

        if not username or not password:
            self.error_label.text = "Please enter both username and password."
            return

        success, message_or_username = check_login(username, password)

        if success:
            # Login successful
            self.error_label.text = "" # Clear error message
            # Optionally show a brief success message before navigating
            self.show_popup("Login Successful", f"Welcome, {message_or_username}!", is_error=False,
                             callback=lambda: self.on_login_success(message_or_username) if self.on_login_success else None)
        else:
            # Login failed
            self.error_label.text = message_or_username # Display error message from check_login

    def show_registration_popup(self, instance):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        reg_username = TextInput(hint_text="New Username", multiline=False, font_size='18sp', height='45dp')
        reg_password = TextInput(hint_text="New Password", multiline=False, password=True, font_size='18sp', height='45dp')
        reg_confirm_password = TextInput(hint_text="Confirm Password", multiline=False, password=True, font_size='18sp', height='45dp')
        reg_error_label = Label(text="", color=(1, 0, 0, 1), size_hint_y=None, height=30)

        def perform_registration():
            username = reg_username.text.strip()
            password = reg_password.text.strip()
            confirm_password = reg_confirm_password.text.strip()

            if not username or not password or not confirm_password:
                reg_error_label.text = "All fields are required."
                return

            if password != confirm_password:
                reg_error_label.text = "Passwords do not match."
                return

            # Use add_user function from this module
            success, message = add_user(username, password)
            if success:
                registration_popup.dismiss()
                # Show success message and then call the app's registration success handler
                self.show_popup("Registration Successful", message, is_error=False,
                                 callback=lambda: self.on_registration_success(username) if self.on_registration_success else None)
            else:
                reg_error_label.text = message

        register_button = Button(text="Register", size_hint_y=None, height='45dp', font_size='18sp')
        register_button.bind(on_press=lambda *args: perform_registration())

        content.add_widget(Label(text="Create Account", font_size='22sp', size_hint_y=None, height='40dp'))
        content.add_widget(reg_username)
        content.add_widget(reg_password)
        content.add_widget(reg_confirm_password)
        content.add_widget(reg_error_label)
        content.add_widget(register_button)

        registration_popup = Popup(
            title="User Registration",
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=False
        )
        registration_popup.open()


# --- Function to get the Login Screen UI ---
def get_login_screen_widget(on_login_success=None, on_registration_success=None):
    """Returns an instance of the LoginScreen with callbacks."""
    return LoginScreen(on_login_success=on_login_success, on_registration_success=on_registration_success)

import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView # اضافه شد
from kivy.uix.gridlayout import GridLayout # اضافه شد

DB_NAME = "mydata.db"

# --- توابع دیتابیس ---

def get_db_connection():
    """اتصال به دیتابیس را برقرار می‌کند."""
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_or_update_table():
    """
    این تابع جدول 'users' را ایجاد یا در صورت نیاز به‌روزرسانی می‌کند.
    - اگر جدول وجود نداشته باشد، آن را با ساختار صحیح می‌سازد.
    - اگر جدول وجود دارد ولی ساختار آن اشتباه است (مثلاً ستون 'first' را ندارد)،
      آن را حذف و دوباره با ساختار صحیح می‌سازد.
    """
    conn = get_db_connection()
    if conn is None:
        print("Cannot connect to database. Table creation aborted.")
        return # خروج اگر اتصال برقرار نشد

    cur = conn.cursor()
    table_exists = False

    try:
        # ابتدا بررسی می‌کنیم جدول users اصلا وجود دارد یا نه
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if cur.fetchone():
            table_exists = True
            # حالا اطلاعات ستون‌ها را می‌گیریم
            cur.execute("PRAGMA table_info(users)")
            columns_info = cur.fetchall()
            column_names = [info[1] for info in columns_info]

            required_columns = ["id", "first", "alphabet", "second", "color", "explain"]

            # بررسی اینکه آیا همه ستون‌های مورد نیاز وجود دارند
            if not all(col in column_names for col in required_columns):
                print("Existing 'users' table has incorrect structure. Recreating...")
                cur.execute("DROP TABLE IF EXISTS users")
                # مجبور به ساخت مجدد می‌شویم
                raise sqlite3.OperationalError("Table structure mismatch")
            else:
                # اگر جدول و ستون‌ها صحیح بودند، کار تمام است
                print("Table 'users' already exists with the correct structure.")
        else:
            # اگر جدول وجود نداشت
            print("Table 'users' does not exist. Creating it...")
            raise sqlite3.OperationalError("Table does not exist") # برای رفتن به بلوک CREATE TABLE

    except sqlite3.OperationalError:
        # این بلوک زمانی اجرا می‌شود که جدول وجود نداشته باشد یا ساختارش اشتباه باشد
        try:
            print("Creating 'users' table...")
            cur.execute('''
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first TEXT NOT NULL,
                    alphabet TEXT NOT NULL,
                    second TEXT NOT NULL,
                    color TEXT,
                    explain TEXT
                )
            ''')
            print("Table 'users' created successfully.")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    finally:
        conn.commit()
        conn.close()

def insert_user(first, alphabet, second, color, explain):
    """کاربر جدید را در دیتابیس درج می‌کند."""
    conn = get_db_connection()
    if conn is None: return False

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (first, alphabet, second, color, explain) VALUES (?, ?, ?, ?, ?)",
            (first, alphabet, second, color, explain)
        )
        conn.commit()
        print("User registered successfully.")
        return True
    except sqlite3.Error as e:
        print(f"Error registering user: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def fetch_users():
    """همه کاربران را از جدول 'users' بازیابی می‌کند."""
    conn = get_db_connection()
    if conn is None: return []

    cur = conn.cursor()
    users_data = []
    try:
        # انتخاب همه ستون‌ها به ترتیب دلخواه (id, first, alphabet, ...)
        cur.execute("SELECT id, first, alphabet, second, color, explain FROM users ORDER BY id ASC")
        users_data = cur.fetchall()
        print(f"Fetched {len(users_data)} users from the database.")
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
    finally:
        conn.close()
    return users_data

# --- رابط کاربری ---

# ویجت برای نمایش یک ردیف از اطلاعات کاربر
class UserRow(BoxLayout):
    def __init__(self, user_info, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=50, spacing=5, padding=5, **kwargs)
        user_id, first, alphabet, second, color, explain = user_info

        # اضافه کردن لیبل‌ها برای هر فیلد
        self.add_widget(Label(text=str(user_id), size_hint=(0.1, 1), font_size=16))
        self.add_widget(Label(text=first, size_hint=(0.2, 1), font_size=16))
        self.add_widget(Label(text=alphabet, size_hint=(0.2, 1), font_size=16))
        self.add_widget(Label(text=second, size_hint=(0.2, 1), font_size=16))
        # اگر مقدار color یا explain خالی بود، "-" نمایش بده
        self.add_widget(Label(text=color if color else "-", size_hint=(0.15, 1), font_size=16))
        self.add_widget(Label(text=explain if explain else "-", size_hint=(0.15, 1), font_size=16))

class MyAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=15, **kwargs)
        self.fields = ["first", "alphabet", "second", "color", "explain"]
        self.inputs = {}

        # تنظیم اندازه پنجره
        Window.size = (800, 700)

        # --- بخش ورودی‌ها ---
        input_section = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=5)
        for f in self.fields:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
            box.add_widget(Label(text=f.capitalize(), size_hint=(0.3, 1), font_size=20,
                                 halign='right', valign='middle')) # ترازبندی راست برای لیبل
            inp = TextInput(multiline=False, size_hint=(0.7, 1), font_size=20, padding_y=(5,5))
            box.add_widget(inp)
            self.inputs[f] = inp
            input_section.add_widget(box)

        save_btn = Button(text="Enter information", size_hint=(1, None), height=50, font_size=25)
        save_btn.bind(on_press=self.save_data)
        input_section.add_widget(save_btn)
        self.add_widget(input_section)

        # --- بخش نمایش اطلاعات ---
        display_section = BoxLayout(orientation='vertical', size_hint_y=0.6, spacing=5)

        # دکمه برای بازخوانی اطلاعات
        view_btn = Button(text="View Registered Users", size_hint=(1, None), height=50, font_size=25)
        view_btn.bind(on_press=self.load_users)
        display_section.add_widget(view_btn)

        # اسکرول ویو برای لیست کاربران
        scroll_view = ScrollView(size_hint=(1, 1))
        # گرید برای چیدمان ردیف‌های کاربر - cols=1 یعنی هر ردیف کاربر در یک خط است
        self.user_list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        # تنظیم ارتفاع گرید بر اساس محتوای آن
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))

        # اضافه کردن هدر به جدول
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, padding=5)
        header.add_widget(Label(text="ID", size_hint=(0.1, 1), bold=True, font_size=18))
        header.add_widget(Label(text="First", size_hint=(0.2, 1), bold=True, font_size=18))
        header.add_widget(Label(text="Alphabet", size_hint=(0.2, 1), bold=True, font_size=18))
        header.add_widget(Label(text="Second", size_hint=(0.2, 1), bold=True, font_size=18))
        header.add_widget(Label(text="Color", size_hint=(0.15, 1), bold=True, font_size=18))
        header.add_widget(Label(text="Explain", size_hint=(0.15, 1), bold=True, font_size=18))
        self.user_list_layout.add_widget(header)

        scroll_view.add_widget(self.user_list_layout)
        display_section.add_widget(scroll_view)

        self.add_widget(display_section)

    def save_data(self, instance):
        data = [self.inputs[f].text.strip() for f in self.fields]
        required_data_values = data[:-1] # فیلد 'explain' اختیاری است

        if all(required_data_values):
            success = insert_user(*data)
            if success:
                Popup(title='Success', content=Label(text="Registration successful!"),
                      size_hint=(0.5, 0.3)).open()
                # پاک کردن فیلدها پس از موفقیت
                for f in self.fields:
                    self.inputs[f].text = ""
                # بلافاصله لیست کاربران را به‌روز کن
                self.load_users(None)
            else:
                # اگر insert_user خطا برگرداند
                Popup(title='Database Error', content=Label(text="Failed to save data. Please try again."),
                      size_hint=(0.5, 0.3)).open()
        else:
            Popup(title='Error', content=Label(text="Please fill all required fields (except 'explain')."),
                  size_hint=(0.5, 0.3)).open()

    def load_users(self, instance):
        """اطلاعات کاربران را از دیتابیس خوانده و نمایش می‌دهد."""
        # پاک کردن ردیف‌های قبلی کاربر (به جز هدر)
        # self.user_list_layout.children شامل هدر و ردیف‌های کاربر است
        widgets_to_remove = self.user_list_layout.children[1:] # همه به جز آیتم اول (هدر)
        for widget in widgets_to_remove:
             self.user_list_layout.remove_widget(widget)

        users = fetch_users()
        if not users:
            # اگر کاربری نبود، یک پیام نمایش بده
            no_users_label = Label(text="No users registered yet.", size_hint_y=None, height=50, font_size=18)
            self.user_list_layout.add_widget(no_users_label)
            return

        # اضافه کردن ردیف‌های کاربر جدید
        for user_info in users:
            user_row = UserRow(user_info)
            self.user_list_layout.add_widget(user_row)

class MyApp(App):
    def build(self):
        # قبل از اجرای رابط کاربری، مطمئن شو جدول آماده است
        create_or_update_table()
        return MyAppLayout()

MyApp().run()

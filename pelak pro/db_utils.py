import sqlite3

DB_NAME = "mydata.db"


def get_db_connection():
    """اتصال به دیتابیس را برقرار می‌کند."""
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None


def create_or_update_table():
    """
    جدول users را ایجاد می‌کند اگر وجود نداشته باشد.
    اگر ساختار جدول اشتباه باشد، آن را حذف و دوباره ایجاد می‌کند.
    """
    conn = get_db_connection()
    if conn is None:
        print("Cannot connect to database.")
        return

    cur = conn.cursor()

    try:
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if cur.fetchone():
            cur.execute("PRAGMA table_info(users)")
            columns_info = cur.fetchall()
            column_names = [info[1] for info in columns_info]

            required_columns = ["id", "first", "alphabet", "second", "color", "explain"]

            if not all(col in column_names for col in required_columns):
                print("Existing 'users' table has incorrect structure. Recreating...")
                cur.execute("DROP TABLE IF EXISTS users")
                raise sqlite3.OperationalError("Table structure mismatch")
            else:
                print("Table 'users' already exists with correct structure.")
        else:
            raise sqlite3.OperationalError("Table does not exist")

    except sqlite3.OperationalError:
        try:
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
    """یک کاربر جدید در جدول users ثبت می‌کند."""
    conn = get_db_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (first, alphabet, second, color, explain) VALUES (?, ?, ?, ?, ?)",
            (first, alphabet, second, color, explain)
        )
        conn.commit()
        print("User inserted successfully.")
        return True
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()


def fetch_users():
    """تمام کاربران را از دیتابیس برمی‌گرداند."""
    conn = get_db_connection()
    if conn is None:
        return []

    cur = conn.cursor()

    try:
        cur.execute("SELECT id, first, alphabet, second, color, explain FROM users ORDER BY id ASC")
        users = cur.fetchall()
        return users
    except sqlite3.Error as e:
        print(f"Error fetching users: {e}")
        return []
    finally:
        conn.close()


def delete_user_by_id(user_id):
    """کاربر را بر اساس id حذف می‌کند."""
    conn = get_db_connection()
    if conn is None:
        return False

    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()

        if cur.rowcount > 0:
            print(f"User with id {user_id} deleted successfully.")
            return True
        else:
            print(f"No user found with id {user_id}.")
            return False

    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
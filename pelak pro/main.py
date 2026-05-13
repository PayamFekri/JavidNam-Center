import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window

DB_NAME = "mydata.db"

# --- توابع دیتابیس ---

def get_db_connection():
    """اتصال به دیتابیس را برقرار می‌کند."""
    return sqlite3.connect(DB_NAME)

def create_or_update_table():
    """
    این تابع جدول 'users' را ایجاد یا در صورت نیاز به‌روزرسانی می‌کند.
    - اگر جدول وجود نداشته باشد، آن را با ساختار صحیح می‌سازد.
    - اگر جدول وجود دارد ولی ساختار آن اشتباه است (مثلاً ستون 'first' را ندارد)،
      آن را حذف و دوباره با ساختار صحیح می‌سازد.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # بررسی وجود جدول و ستون‌های مورد نیاز
        cur.execute("PRAGMA table_info(users)")
        columns_info = cur.fetchall()
        column_names = [info[1] for info in columns_info]

        required_columns = ["id", "first", "alphabet", "second", "color", "explain"]

        # بررسی اینکه آیا همه ستون‌های مورد نیاز وجود دارند
        if not all(col in column_names for col in required_columns):
            print("user is here but structure has a mistake")
            cur.execute("DROP TABLE IF EXISTS users")
            raise sqlite3.OperationalError("Table structure mismatch") # مجبور به ساخت مجدد

        # اگر جدول و ستون‌ها صحیح بودند، هیچ کاری انجام نمی‌شود
        print("user table is trueth with true structure")

    except sqlite3.OperationalError:
        # اگر جدول وجود نداشت یا ساختار آن اشتباه بود، آن را می‌سازیم
        print("در حال ایجاد جدول 'users'...")
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
        print("user existation was successful")

    finally:
        conn.commit()
        conn.close()

def insert_user(first, alphabet, second, color, explain):
    """کاربر جدید را در دیتابیس درج می‌کند."""
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (first, alphabet, second, color, explain) VALUES (?, ?, ?, ?, ?)",
            (first, alphabet, second, color, explain)
        )
        conn.commit()
        print("register was successful")
        return True
    except sqlite3.Error as e:
        print(f"error to register : {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

# --- رابط کاربری ---

class MyAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=15, **kwargs)
        self.fields = ["first", "alphabet", "second", "color", "explain"]
        self.inputs = {}

        # تنظیم اندازه پنجره (اختیاری)
        Window.size = (800, 600)

        for f in self.fields:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=60)
            # استفاده از text_size برای ترازبندی بهتر متن در لیبل
            box.add_widget(Label(text=f.capitalize(), size_hint=(0.3, 1), font_size=20,
                                 halign='right', valign='middle'))
            inp = TextInput(multiline=False, size_hint=(0.7, 1), font_size=20, padding_y=(5,5))
            box.add_widget(inp)
            self.inputs[f] = inp
            self.add_widget(box)

        save_btn = Button(text="Enter information", size_hint=(1, None), height=50, font_size=25)
        save_btn.bind(on_press=self.save_data)
        self.add_widget(save_btn)

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
            else:
                # اگر insert_user خطا برگرداند
                Popup(title='Database Error', content=Label(text="Failed to save data. Please try again."),
                      size_hint=(0.5, 0.3)).open()
        else:
            Popup(title='Error', content=Label(text="Please fill all required fields (except 'explain')."),
                  size_hint=(0.5, 0.3)).open()

class MyApp(App):
    def build(self):
        # قبل از اجرای رابط کاربری، مطمئن شو جدول آماده است
        create_or_update_table()
        return MyAppLayout()


MyApp().run()

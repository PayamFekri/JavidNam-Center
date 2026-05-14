# main.py

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
import sqlite3
import os

# === تنظیمات فونت ===
# نام فونت فارسی نصب شده روی سیستم خودتان را اینجا بگذارید.
# مثلاً: "Arial", "Tahoma", "B Nazanin", "Yas", ...
# اگر فایل TTF دارید، مسیر کامل آن را بدهید.
Farsi_font = "Arial"

# === کلاس‌های سفارشی برای پشتیبانی از فارسی ===
class PersianTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = Farsi_font
        self.text_align = 'right'
        # تنظیم فیلتر ورودی: فقط اجازه یک کاراکتر را بدهد
        # ما از یک فیلتر سفارشی استفاده می‌کنیم که طول متن را هم چک کند
        self.input_filter = self._custom_filter
        self.text = "" # اطمینان از خالی بودن اولیه

    def _custom_filter(self, character):
        # اگر متن فعلی خالی است و کاراکتر ورودی، فارسی است (یا هر کاراکتری)
        # و طول متن نهایی بیشتر از 1 نشود، اجازه ورود بده.
        if len(self.text) < 1 and len(character) == 1:
             # اینجا می‌توانی چک کنی که کاراکتر واقعاً فارسی باشد (اختیاری)
             # برای سادگی، فعلاً فقط طول را چک می‌کنیم
             return character
        return '' # در غیر این صورت، ورودی را رد کن

class PersianLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = Farsi_font
        self.text_size = (self.width, None)
        self.valign = 'middle'
        self.halign = 'right'

# === Layout اصلی ===
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        Window.size = (400, 300) # اندازه کوچکتر برای این مثال

        # --- بخش ورودی یک کاراکتر فارسی ---
        self.char_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.char_input_layout.add_widget(PersianLabel(text="کاراکتر:", size_hint_x=0.3))
        self.char_input = PersianTextInput(hint_text="یک حرف فارسی", size_hint_x=0.7, font_name=Farsi_font) # اینجا فونت را دوباره مشخص می‌کنیم
        self.char_input_layout.add_widget(self.char_input)
        self.add_widget(self.char_input_layout)

        # دکمه ذخیره
        save_button = Button(text="ثبت کاراکتر", size_hint_y=None, height=50)
        save_button.bind(on_press=self.save_character)
        self.add_widget(save_button)

        # نمایش آخرین کاراکتر ذخیره شده
        self.display_label = PersianLabel(text="آخرین کاراکتر ثبت شده:")
        self.add_widget(self.display_label)
        self.load_last_char()

    def save_character(self, instance):
        char = self.char_input.text.strip() # حذف فضاهای خالی احتمالی

        if not char:
            self.show_popup("خطا", "لطفاً یک کاراکتر وارد کنید.")
            return

        if len(char) != 1:
            # این حالت نباید اتفاق بیفتد چون فیلتر ورودی کار می‌کند، ولی برای اطمینان
            self.show_popup("خطا", "فقط یک کاراکتر مجاز است.")
            return

        # اینجا کد ذخیره در SQLite
        if self.save_to_db(char):
            self.char_input.text = "" # پاک کردن فیلد بعد از ثبت موفق
            self.load_last_char()
        else:
            self.show_popup("خطا", "خطا در ثبت کاراکتر در دیتابیس.")

    def save_to_db(self, character):
        try:
            # ایجاد یا اتصال به دیتابیس
            conn = sqlite3.connect('characters.db')
            cursor = conn.cursor()

            # ایجاد جدول اگر وجود نداشت
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS persian_chars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    char TEXT NOT NULL UNIQUE -- UNIQUE یعنی هر کاراکتر فقط یک بار ثبت شود
                )
            ''')

            # اضافه کردن کاراکتر جدید
            # از INSERT OR IGNORE استفاده می‌کنیم تا اگر کاراکتر تکراری بود، خطا ندهد
            cursor.execute("INSERT OR IGNORE INTO persian_chars (char) VALUES (?)", (character,))

            # اگر کاراکتر جدید اضافه شده باشد (و تکراری نبوده باشد)
            if cursor.rowcount > 0:
                conn.commit()
                print(f"کاراکتر '{character}' با موفقیت ذخیره شد.")
                conn.close()
                return True
            else:
                print(f"کاراکتر '{character}' قبلاً در دیتابیس وجود دارد.")
                self.show_popup("تکراری", f"کاراکتر '{character}' قبلاً ثبت شده است.")
                conn.close()
                return False # چون کاراکتر قبلاً بوده

        except sqlite3.Error as e:
            print(f"خطای SQLite: {e}")
            conn.close()
            return False

    def load_last_char(self):
        try:
            conn = sqlite3.connect('characters.db')
            cursor = conn.cursor()
            # آخرین کاراکتر ذخیره شده را بگیر
            cursor.execute("SELECT char FROM persian_chars ORDER BY id DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if row:
                self.display_label.text = f"آخرین کاراکتر ثبت شده: {row[0]}"
            else:
                self.display_label.text = "هنوز کاراکتری ثبت نشده است."
        except sqlite3.Error as e:
            print(f"خطای SQLite هنگام بارگذاری: {e}")
            self.display_label.text = "خطا در بارگذاری."

    def show_popup(self, title, message):
        # پاپ‌آپ برای نمایش پیام‌ها
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(PersianLabel(text=message, font_name=Farsi_font, halign='center'))
        close_button = Button(text="باشه", size_hint_y=None, height=40)
        close_button.bind(on_press=lambda instance: self.dismiss_popup(popup_layout.parent))
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.7, 0.4))
        popup.open()

    def dismiss_popup(self, popup_instance):
        popup_instance.dismiss()


# === کلاس اصلی برنامه ===
class PersianCharApp(App):
    def build(self):
        # تنظیم انکودینگ اولیه پایتون
        import sys
        import os
        os.environ["PYTHONIOENCODING"] = "utf-8"
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            if hasattr(sys.stderr, "reconfigure"):
                sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
        return MainLayout()

if __name__ == '__main__':
    PersianCharApp().run()

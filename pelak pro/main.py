import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# ====== دیتابیس ======
def create_table():
    conn = sqlite3.connect("mydata.db")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first TEXT,
            alphabet TEXT,
            second TEXT,
            color TEXT,
            explain TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(first, alphabet, second, color, explain):
    conn = sqlite3.connect("mydata.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (first, alphabet, second, color, explain) VALUES (?, ?, ?, ?, ?)",
        (first, alphabet, second, color, explain)
    )
    conn.commit()
    conn.close()

# ====== UI ======
class MyAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=15, **kwargs)

        self.inputs = {}
        fields = ["first", "alphabet", "second", "color", "explain"]

        for f in fields:
            box = BoxLayout(orientation='horizontal', size_hint_y=3, height=60)
            box.add_widget(Label(text=f, size_hint=(0.3, None), height=60, font_size=25))
            inp = TextInput(multiline=False, size_hint_y=None, height=55, font_size=25)
            box.add_widget(inp)
            self.inputs[f] = inp
            self.add_widget(box)

        save_btn = Button(text="Enter information", size_hint=(1, None), height=50)
        save_btn.bind(on_press=self.save_data)
        self.add_widget(save_btn)

    def save_data(self, instance):
        data = [self.inputs[f].text.strip() for f in self.inputs]
        required_data = data[:-1]  # فیلد آخر اختیاری

        if all(required_data):
            insert_user(*data)
            Popup(title='Success', content=Label(text="Register was successful!"),
                  size_hint=(0.5, 0.3)).open()
            for f in self.inputs:
                self.inputs[f].text = ""
        else:
            Popup(title='Error', content=Label(text="Please fill all required fields."),
                  size_hint=(0.5, 0.3)).open()

class MyApp(App):
    def build(self):
        create_table()
        return MyAppLayout()

MyApp().run()

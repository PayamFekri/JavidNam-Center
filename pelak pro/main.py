from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from db_utils import create_or_update_table, insert_user, fetch_users, delete_user_by_id


class UserRow(BoxLayout):
    def __init__(self, user_info, **kwargs):
        super().__init__(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=5,
            padding=5,
            **kwargs
        )

        user_id, first, alphabet, second, color, explain = user_info

        self.add_widget(Label(text=str(user_id), size_hint=(0.1, 1), font_size=16))
        self.add_widget(Label(text=first, size_hint=(0.18, 1), font_size=16))
        self.add_widget(Label(text=alphabet, size_hint=(0.18, 1), font_size=16))
        self.add_widget(Label(text=second, size_hint=(0.18, 1), font_size=16))
        self.add_widget(Label(text=color if color else "-", size_hint=(0.18, 1), font_size=16))
        self.add_widget(Label(text=explain if explain else "-", size_hint=(0.18, 1), font_size=16))


class MyAppLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=15, **kwargs)

        Window.size = (900, 750)

        self.fields = ["first", "alphabet", "second", "color", "explain"]
        self.inputs = {}

        # -------------------------
        # بخش ورود اطلاعات
        # -------------------------
        input_section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=380,
            spacing=8
        )

        for field_name in self.fields:
            row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=60,
                spacing=10
            )

            label = Label(
                text=field_name.capitalize(),
                size_hint=(0.3, 1),
                font_size=20
            )

            text_input = TextInput(
                multiline=False,
                size_hint=(0.7, 1),
                font_size=20
            )

            self.inputs[field_name] = text_input

            row.add_widget(label)
            row.add_widget(text_input)
            input_section.add_widget(row)

        save_btn = Button(
            text="Enter Information",
            size_hint=(1, None),
            height=50,
            font_size=22
        )
        save_btn.bind(on_press=self.save_data)
        input_section.add_widget(save_btn)

        self.add_widget(input_section)

        # -------------------------
        # بخش حذف کاربر
        # -------------------------
        delete_section = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=55,
            spacing=10
        )

        self.delete_input = TextInput(
            hint_text="Enter user ID to delete",
            multiline=False,
            size_hint=(0.7, 1),
            font_size=20
        )

        delete_btn = Button(
            text="Delete User",
            size_hint=(0.3, 1),
            font_size=20
        )
        delete_btn.bind(on_press=self.remove_user)

        delete_section.add_widget(self.delete_input)
        delete_section.add_widget(delete_btn)

        self.add_widget(delete_section)

        # -------------------------
        # بخش نمایش کاربران
        # -------------------------
        display_section = BoxLayout(
            orientation='vertical',
            size_hint=(1, 1),
            spacing=5
        )

        control_buttons = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=50,
            spacing=10
        )

        view_btn = Button(
            text="View Registered Users",
            font_size=20
        )
        view_btn.bind(on_press=self.load_users)

        refresh_btn = Button(
            text="Refresh List",
            font_size=20
        )
        refresh_btn.bind(on_press=self.load_users)

        control_buttons.add_widget(view_btn)
        control_buttons.add_widget(refresh_btn)

        display_section.add_widget(control_buttons)

        # هدر جدول
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=40,
            padding=5,
            spacing=5
        )

        with header.canvas.before:
            Color(0.85, 0.85, 0.85, 1)
            self.header_rect = Rectangle(pos=header.pos, size=header.size)

        header.bind(pos=self.update_header_rect, size=self.update_header_rect)

        headers = [
            ("ID", 0.1),
            ("First", 0.18),
            ("Alphabet", 0.18),
            ("Second", 0.18),
            ("Color", 0.18),
            ("Explain", 0.18),
        ]

        for title, width in headers:
            header.add_widget(Label(text=title, size_hint=(width, 1), bold=True, font_size=16))

        display_section.add_widget(header)

        # اسکرول و لیست کاربران
        scroll_view = ScrollView(size_hint=(1, 1))

        self.user_list_layout = GridLayout(
            cols=1,
            spacing=5,
            size_hint_y=None
        )
        self.user_list_layout.bind(minimum_height=self.user_list_layout.setter('height'))

        scroll_view.add_widget(self.user_list_layout)
        display_section.add_widget(scroll_view)

        self.add_widget(display_section)

        # بارگذاری اولیه
        self.load_users(None)

    def update_header_rect(self, instance, value):
        self.header_rect.pos = instance.pos
        self.header_rect.size = instance.size

    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()

    def save_data(self, instance):
        first = self.inputs["first"].text.strip()
        alphabet = self.inputs["alphabet"].text.strip()
        second = self.inputs["second"].text.strip()
        color = self.inputs["color"].text.strip()
        explain = self.inputs["explain"].text.strip()

        if not first or not alphabet or not second:
            self.show_popup("Error", "Please fill in First, Alphabet, and Second fields.")
            return

        success = insert_user(first, alphabet, second, color, explain)

        if success:
            self.show_popup("Success", "User information saved successfully.")
            for inp in self.inputs.values():
                inp.text = ""
            self.load_users(None)
        else:
            self.show_popup("Error", "Failed to save user information.")

    def load_users(self, instance):
        self.user_list_layout.clear_widgets()

        users = fetch_users()

        if not users:
            self.user_list_layout.add_widget(
                Label(
                    text="No users registered yet.",
                    size_hint_y=None,
                    height=40,
                    font_size=18
                )
            )
            return

        for user in users:
            self.user_list_layout.add_widget(UserRow(user))

    def remove_user(self, instance):
        user_id_text = self.delete_input.text.strip()

        if not user_id_text:
            self.show_popup("Error", "Please enter a user ID.")
            return

        if not user_id_text.isdigit():
            self.show_popup("Error", "User ID must be numeric.")
            return

        user_id = int(user_id_text)
        success = delete_user_by_id(user_id)

        if success:
            self.show_popup("Success", f"User with ID {user_id} deleted successfully.")
            self.delete_input.text = ""
            self.load_users(None)
        else:
            self.show_popup("Error", f"No user found with ID {user_id}.")


class MyApp(App):
    def build(self):
        self.title = "Mozdur Manager"
        create_or_update_table()
        return MyAppLayout()


if __name__ == "__main__":
    MyApp().run()

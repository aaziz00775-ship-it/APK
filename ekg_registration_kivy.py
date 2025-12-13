"""
Мобильное приложение для регистрации пациентов кабинета ЭКГ (Kivy версия)
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import sqlite3
import os
from kivy.utils import platform

# Для работы с Excel на Android нужен другой подход
try:
    import openpyxl
    from openpyxl import load_workbook
    EXCEL_AVAILABLE = True
except:
    EXCEL_AVAILABLE = False

class EKGRegistrationForm(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Имя файла базы данных
        if platform == 'android':
            from android.storage import primary_external_storage_path
            self.db_file = os.path.join(primary_external_storage_path(), 'ekg_patients.db')
            self.excel_file = os.path.join(primary_external_storage_path(), 'ekg_patients.xlsx')
        else:
            self.db_file = "ekg_patients.db"
            self.excel_file = "ekg_patients.xlsx"
        
        # Последнее имя врача
        self.last_doctor_name = ""
        
        # Создать базу данных
        self.create_database_if_not_exists()
        
        # Загрузить последнее имя врача
        self.load_last_doctor_name()
        
        # Создать интерфейс
        self.create_widgets()
    
    def create_database_if_not_exists(self):
        """Создать базу данных SQLite с таблицей пациентов, если её нет"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                birth_date TEXT,
                address TEXT,
                insurance TEXT NOT NULL,
                receipt TEXT NOT NULL,
                doctor_name TEXT,
                registration_date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_last_doctor_name(self):
        """Загрузить последнее имя врача из базы данных"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT doctor_name FROM patients WHERE doctor_name IS NOT NULL AND doctor_name != "" ORDER BY id DESC LIMIT 1')
            result = cursor.fetchone()
            if result:
                self.last_doctor_name = result[0]
            conn.close()
        except:
            self.last_doctor_name = ""
    
    def create_widgets(self):
        """Создать элементы интерфейса"""
        # Заголовок
        title = Label(
            text="EKG kabinetiniň kesellerini hasaba almak",
            size_hint_y=None,
            height=50,
            font_size=18,
            bold=True
        )
        self.add_widget(title)
        
        # ScrollView для формы
        scroll = ScrollView()
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Имя
        form_layout.add_widget(Label(text="Ady:", size_hint_y=None, height=30))
        self.first_name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.first_name_input)
        
        # Фамилия
        form_layout.add_widget(Label(text="Familiýasy:", size_hint_y=None, height=30))
        self.last_name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.last_name_input)
        
        # Пол
        form_layout.add_widget(Label(text="Jynsy:", size_hint_y=None, height=30))
        self.gender_spinner = Spinner(
            text='Erkek',
            values=('Erkek', 'Aýal'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.gender_spinner)
        
        # Дата рождения
        form_layout.add_widget(Label(text="Doglan senesi (GGGG.AA.GG):", size_hint_y=None, height=30))
        self.birth_date_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.birth_date_input)
        
        # Место проживания - тип
        form_layout.add_widget(Label(text="Ýaşaýan ýeri:", size_hint_y=None, height=30))
        address_type_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        self.address_type_spinner = Spinner(
            text='Şäher',
            values=('Şäher', 'Etrap'),
            size_hint_x=0.3,
            size_hint_y=None,
            height=40
        )
        address_type_layout.add_widget(self.address_type_spinner)
        self.address_input = TextInput(multiline=False, size_hint_x=0.7, size_hint_y=None, height=40)
        address_type_layout.add_widget(self.address_input)
        form_layout.add_widget(address_type_layout)
        
        # Страховка
        form_layout.add_widget(Label(text="Saglyk ätiýaçlandyrma:", size_hint_y=None, height=30))
        self.insurance_spinner = Spinner(
            text='Bar',
            values=('Bar', 'Ýok'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.insurance_spinner)
        
        # Номер квитанции
        form_layout.add_widget(Label(text="Kwitansiýa belgisi:", size_hint_y=None, height=30))
        self.receipt_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_layout.add_widget(self.receipt_input)
        
        # Имя врача
        form_layout.add_widget(Label(text="Lukmanyň ady:", size_hint_y=None, height=30))
        self.doctor_name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        if self.last_doctor_name:
            self.doctor_name_input.text = self.last_doctor_name
        form_layout.add_widget(self.doctor_name_input)
        
        scroll.add_widget(form_layout)
        self.add_widget(scroll)
        
        # Кнопки
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        save_button = Button(
            text="Ýatda saklamak",
            size_hint_x=0.5,
            background_color=(0.3, 0.7, 0.3, 1)
        )
        save_button.bind(on_press=self.save_patient)
        button_layout.add_widget(save_button)
        
        clear_button = Button(
            text="Arassalamak",
            size_hint_x=0.5,
            background_color=(0.9, 0.3, 0.3, 1)
        )
        clear_button.bind(on_press=self.clear_form)
        button_layout.add_widget(clear_button)
        
        self.add_widget(button_layout)
        
        # Статус
        self.status_label = Label(
            text="",
            size_hint_y=None,
            height=30,
            color=(0, 0.7, 0, 1)
        )
        self.add_widget(self.status_label)
    
    def validate_form(self):
        """Проверка заполнения всех обязательных полей"""
        if not self.first_name_input.text.strip():
            self.show_error("Adyňyzy giriziň")
            return False
        
        if not self.last_name_input.text.strip():
            self.show_error("Familiýaňyzy giriziň")
            return False
        
        if not self.receipt_input.text.strip():
            self.show_error("Kwitansiýa belgisini giriziň")
            return False
        
        return True
    
    def show_error(self, message):
        """Показать сообщение об ошибке"""
        popup = Popup(
            title='Ýalňyşlyk',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_success(self, message):
        """Показать сообщение об успехе"""
        popup = Popup(
            title='Üstünlik',
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def save_patient(self, instance):
        """Сохранить данные пациента"""
        if not self.validate_form():
            return
        
        try:
            # Получить данные из формы
            first_name = self.first_name_input.text.strip()
            last_name = self.last_name_input.text.strip()
            gender = self.gender_spinner.text.lower()
            birth_date = self.birth_date_input.text.strip() or None
            address_type = self.address_type_spinner.text.lower()
            address_name = self.address_input.text.strip()
            address = f"{address_type}, {address_name}" if address_name else address_type
            insurance = self.insurance_spinner.text.lower()
            receipt = self.receipt_input.text.strip()
            doctor_name = self.doctor_name_input.text.strip() or None
            registration_date = datetime.now().strftime("%d.%m.%Y %H:%M")
            
            # Сохранить имя врача для следующего раза
            if doctor_name:
                self.last_doctor_name = doctor_name
            
            # Сохранить в базу данных
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO patients 
                (first_name, last_name, gender, birth_date, address, insurance, 
                 receipt, doctor_name, registration_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (first_name, last_name, gender, birth_date, address,
                  insurance, receipt, doctor_name, registration_date))
            
            conn.commit()
            conn.close()
            
            # Показать сообщение об успехе
            self.show_success(f"Lukman {first_name} {last_name} üstünlikli hasaba alyndy!")
            
            # Очистить форму
            self.clear_form()
            
            # Обновить статус
            self.status_label.text = f"Soňky hasaba almak: {datetime.now().strftime('%H:%M:%S')}"
            
        except Exception as e:
            self.show_error(f"Saklamakda ýalňyşlyk: {str(e)}")
    
    def clear_form(self, instance=None):
        """Очистить все поля формы"""
        self.first_name_input.text = ""
        self.last_name_input.text = ""
        self.gender_spinner.text = "Erkek"
        self.birth_date_input.text = ""
        self.address_type_spinner.text = "Şäher"
        self.address_input.text = ""
        self.insurance_spinner.text = "Bar"
        self.receipt_input.text = ""
        self.doctor_name_input.text = self.last_doctor_name if self.last_doctor_name else ""
        self.status_label.text = ""

class EKGRegistrationApp(App):
    def build(self):
        return EKGRegistrationForm()

if __name__ == '__main__':
    EKGRegistrationApp().run()


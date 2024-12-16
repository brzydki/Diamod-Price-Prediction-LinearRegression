import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from modelpredict import predict, valuepredict  # Подключаем вашу функцию valuepredict
from plot import plot_1


class MainMenu(BoxLayout):
    def __init__(self, switch_to_manual, switch_to_file, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text='Выберите способ ввода данных алмаза:')
        self.add_widget(self.label)

        self.manual_button = Button(text='Ввести данные вручную')
        self.manual_button.bind(on_press=lambda x: switch_to_manual())
        self.add_widget(self.manual_button)

        self.file_button = Button(text='Выбрать файл с алмазом (CSV)')
        self.file_button.bind(on_press=lambda x: switch_to_file())
        self.add_widget(self.file_button)


class ManualInputMenu(BoxLayout):
    def __init__(self, switch_to_main, process_manual_data, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text='Введите данные алмаза:')
        self.add_widget(self.label)

        self.fields = {}
        field_names = ["Карат", "Глубина", "Ширина верхней части", "Длина в мм", "Ширина в мм", "Высота в мм"]

        for name in field_names:
            label = Label(text=name)
            self.add_widget(label)
            self.fields[name] = TextInput(hint_text=f'Введите {name.lower()}', multiline=False)
            self.add_widget(self.fields[name])

        self.submit_button = Button(text='Отправить')
        self.submit_button.bind(on_press=lambda x: process_manual_data(self.fields))
        self.add_widget(self.submit_button)

        self.back_button = Button(text='Назад')
        self.back_button.bind(on_press=lambda x: switch_to_main())
        self.add_widget(self.back_button)


class FileInputMenu(BoxLayout):
    def __init__(self, switch_to_main, process_file, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text='Выберите файл с данными алмаза:')
        self.add_widget(self.label)

        self.file_path = TextInput(hint_text='Выбранный файл будет отображен здесь', multiline=False, readonly=True)
        self.add_widget(self.file_path)

        self.file_chooser = FileChooserListView(filters=["*.csv"], path=".", size_hint=(1, 0.7))
        self.file_chooser.bind(selection=self.update_file_path)  # Обработчик выбора файла
        self.add_widget(self.file_chooser)

        self.submit_button = Button(text='Отправить', size_hint=(1, 0.2))
        self.submit_button.bind(on_press=lambda x: process_file(self.file_path.text))
        self.add_widget(self.submit_button)

        self.back_button = Button(text='Назад', size_hint=(1, 0.2))
        self.back_button.bind(on_press=lambda x: switch_to_main())
        self.add_widget(self.back_button)

    def update_file_path(self, filechooser, selection):
        """Обновляет текстовое поле при выборе файла."""
        if selection and len(selection) > 0:  # Проверяем, что файл выбран
            self.file_path.text = selection[0]  # Записываем путь к файлу



class ResultMenu(BoxLayout):
    def __init__(self, predicted_price, switch_to_main, process_user_price, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.label = Label(text='Результаты предсказания цены алмаза:')
        self.add_widget(self.label)

        self.predicted_price_label = Label(text=f'Предсказанная цена: {predicted_price}')
        self.add_widget(self.predicted_price_label)

        self.user_price_label = Label(text='Введите желаемую цену для подбора параметров:')
        self.add_widget(self.user_price_label)

        self.user_price_input = TextInput(hint_text='Введите цену в USD', multiline=False)
        self.add_widget(self.user_price_input)

        self.submit_button = Button(text='Отправить')
        self.submit_button.bind(on_press=lambda x: process_user_price(self.user_price_input.text))
        self.add_widget(self.submit_button)

        self.plot_button = Button(text='Вывести график')
        self.plot_button.bind(on_press=self.plot_placeholder)
        self.add_widget(self.plot_button)

        self.back_button = Button(text='Назад')
        self.back_button.bind(on_press=lambda x: switch_to_main())
        self.add_widget(self.back_button)

    def plot_placeholder(self, instance):
        plot_1()


class MyApp(App):
    def build(self):
        self.main_menu = MainMenu(switch_to_manual=self.show_manual_input_menu,
                                  switch_to_file=self.show_file_input_menu)
        self.manual_input_menu = ManualInputMenu(switch_to_main=self.show_main_menu,
                                                 process_manual_data=self.process_manual_data)
        self.file_input_menu = FileInputMenu(switch_to_main=self.show_main_menu, process_file=self.process_file)
        self.result_menu = None
        self.current_menu = self.main_menu
        return self.current_menu

    def show_main_menu(self):
        self.root.clear_widgets()
        self.root.add_widget(self.main_menu)
        self.current_menu = self.main_menu

    def show_manual_input_menu(self):
        self.root.clear_widgets()
        self.root.add_widget(self.manual_input_menu)
        self.current_menu = self.manual_input_menu

    def show_file_input_menu(self):
        self.root.clear_widgets()
        self.root.add_widget(self.file_input_menu)
        self.current_menu = self.file_input_menu

    def show_result_menu(self, predicted_price):
        self.result_menu = ResultMenu(
            predicted_price=predicted_price,
            switch_to_main=self.show_main_menu,
            process_user_price=self.process_user_price
        )
        self.root.clear_widgets()
        self.root.add_widget(self.result_menu)
        self.current_menu = self.result_menu

    def process_manual_data(self, fields):
        data = {
            "carat": float(fields["Карат"].text or 0),
            "depth": float(fields["Глубина"].text or 0),
            "table": float(fields["Ширина верхней части"].text or 0),
            "x": float(fields["Длина в мм"].text or 0),
            "y": float(fields["Ширина в мм"].text or 0),
            "z": float(fields["Высота в мм"].text or 0)
        }
        file_path = "diamond_temp.csv"
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        print(f"CSV файл создан: {file_path}")
        predicted_price = self.predict_price(data)
        self.show_result_menu(predicted_price)

    def process_file(self, file_path):
        if not file_path:
            print("Файл не выбран!")
            return
        try:
            self.file_handler_stub(file_path)  # Вызов функции-заглушки
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data = {k: float(v) for k, v in row.items()}
                    predicted_price = self.predict_price(data)
                    self.show_result_menu(predicted_price)
                    return
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

    def predict_price(self, data):
        return predict()

    def process_user_price(self, user_price):
        try:
            target_price = float(user_price)
        except ValueError:
            print("Неверно введена цена! Пожалуйста, введите число.")
            return
        predicted_values = valuepredict(target_price)
        print(f"Подобранные параметры для цены {target_price}: {predicted_values}")

    def file_handler_stub(self, file_path):
        print(f"Переданный путь к файлу: {file_path}")
        # Здесь можно добавить код для обработки файла


if __name__ == '__main__':
    MyApp().run()

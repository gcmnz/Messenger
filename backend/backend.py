import json

from .client import Client
from GUI.custom_widget.list import ListItem


def check_connection_status_without_hide(func: staticmethod):
    """
    Декоратор для проверки статуса подключения к серверу при нажатии на кнопку
    """
    def wrapper(*args):
        if args[0].client.is_connected():
            return func(args[0])
        else:
            args[0].show_notification()

    return wrapper


def check_connection_status_with_hide(func: staticmethod):
    """
    Декоратор для проверки статуса подключения к серверу при нажатии на кнопку
    """
    def wrapper(*args):
        if args[0].client.is_connected():
            args[0].hide_notifications()
            return func(args[0])
        else:
            args[0].show_notification()

    return wrapper


class Backend:
    def __init__(self, main_window) -> None:
        self.__window = main_window
        self.__current_widget = None

        with open('config.json') as f:
            config = json.load(f)

        self.client = Client(self, config['ip'], config['port'])
        self.client.connect()

    @check_connection_status_with_hide
    def change_to_registration(self) -> None:
        """
        Для переключения на виджет регистрации
        """
        self.__window.stacked_widget.setCurrentWidget(self.__window.registration_widget)
        self.__current_widget = self.__window.registration_widget

    def set_widget(self) -> None:
        """
        Метод для присваивания self.__current_widget виджет, воизбежание обращению к NoneType
        """
        self.__current_widget = self.__window.authorization_widget

    @check_connection_status_with_hide
    def change_to_authorization(self) -> None:
        """
        Для переключения на виджет авторизации
        """
        self.__window.stacked_widget.setCurrentWidget(self.__window.authorization_widget)
        self.__current_widget = self.__window.authorization_widget

    @check_connection_status_with_hide
    def change_to_messaging(self) -> None:
        """
        Для переключения на виджет общения
        """
        self.__window.messaging_widget.load_messages()
        self.__window.stacked_widget.setCurrentWidget(self.__window.messaging_widget)
        self.__current_widget = self.__window.messaging_widget

    @check_connection_status_without_hide
    def enter_account_button_func(self) -> None:
        """
        Для проверки на валидность логина и пароля и дальнейшего запроса на сервер
        """
        login = self.__window.authorization_widget.login.text()
        password = self.__window.authorization_widget.password.text()

        if login and password:
            self.client.enter_account(login, password)

    @check_connection_status_without_hide
    def create_account_button_func(self) -> None:
        """
        Для проверки логина и пароля и дальнейшего запроса на сервер
        """
        login = self.__window.registration_widget.login.text()
        password = self.__window.registration_widget.password.text()

        if login and password:
            if 3 < len(login) < 33:
                self.client.create_account(login, password)
            else:
                self.show_notification('Недопустимая длина логина')

    @check_connection_status_without_hide
    def send_message_button_func(self) -> None:
        """
        Метод для отправки запроса с получателем и текстом сообщения на сервер
        """
        print(123)
        receiver = self.__window.messaging_widget.receiver.text()
        message = self.__window.messaging_widget.message.text()

        if receiver and message:
            self.client.send_message(receiver, message)

    @check_connection_status_without_hide
    def load_all_messages(self) -> None:
        """
        Вызов запроса на получение всех сообщений из базы
        """
        self.client.send_load_messages_request()

    def load_messages_from_server(self, messages: dict):
        for interlocutor in messages:
            item = ListItem(interlocutor)
            msg_item = ListItem(interlocutor)
            self.__window.messaging_widget.list_interlocutor.addItem(item)
            self.__window.messaging_widget.list_messages.addItem(msg_item)
            # for message in messages[interlocutor]:
            #     print(message)

    def show_notification(self, text: str = 'Connection lost') -> None:
        """
        Метод для отображения уведомления на текущем виджете
        """
        self.__current_widget.notification.setVisible(True)
        self.__current_widget.notification.setText(text)

    def hide_notifications(self) -> None:
        """
        Метод для скрытия уведомлений на всех виджетах
        """
        self.__window.authorization_widget.notification.setVisible(False)
        self.__window.registration_widget.notification.setVisible(False)
        self.__window.messaging_widget.notification.setVisible(False)

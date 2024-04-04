import json

from .client import Client
from GUI.custom_widget.list import ListItem


def check_connection_status_without_hide(func: staticmethod):
    """
    Декоратор для проверки статуса подключения к серверу при нажатии на кнопку
    """
    def wrapper(*args):
        if args[0].client.is_connected():
            return func(*args)
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
        messaging_widget = self.__window.messaging_widget

        if messaging_widget.interlocutors_widget.list_interlocutor.currentItem() is not None:  # Если выбрали получателя
            receiver = messaging_widget.interlocutors_widget.list_interlocutor.currentItem().interlocutor
            message = messaging_widget.messages_widget.enter_message_textfield.text()

            if message:
                messaging_widget.messages_widget.message_sended(message)
                self.client.send_message(receiver, message)

    def message_received(self, sender: str, message: str):
        self.__window.messaging_widget.on_message_received(sender, message)

    def on_interlocutor_change(self, current_interlocutor):
        """
        Метод для обновления сообщений на виджете после нажатия на QListItem с другим собеседником
        """
        if current_interlocutor:
            self.__window.messaging_widget.messages_widget.set_messages(current_interlocutor.messages, current_interlocutor.is_sender)

    @check_connection_status_without_hide
    def load_all_messages(self) -> None:
        """
        Вызов запроса на получение всех сообщений из базы
        """
        self.client.send_load_messages_request()

    def display_messages_from_server_after_loading(self, loaded_messages: dict) -> None:
        """
        Метод для создания QListItems в списке собеседников
        """
        list_interlocutor = self.__window.messaging_widget.interlocutors_widget.list_interlocutor
        for interlocutor in loaded_messages:
            item = ListItem(interlocutor, loaded_messages[interlocutor][:-1], loaded_messages[interlocutor][-1])
            list_interlocutor.addItem(item)

        list_interlocutor.setCurrentItem(list_interlocutor.item(0))

    @check_connection_status_without_hide
    def find_users_by_nickname(self, nickname: str) -> None:
        """
        Вызов метода клиента для отправки запроса на получение всех аккаунтов, схожих в nickname
        """
        if nickname:
            self.client.get_users_by_nickname_request(nickname)
        else:
            self.__window.messaging_widget.interlocutors_widget.list_interlocutor.show_all_items()

    def display_found_users(self, users_array: list[tuple[str]], login: str) -> None:
        users_array = [user for user in users_array if login not in user]
        self.__window.messaging_widget.interlocutors_widget.list_interlocutor.sort(users_array)

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

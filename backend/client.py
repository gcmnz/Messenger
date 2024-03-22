import socket
import threading
import time

from .message import Message


class Client:
    __PKT_HEARTBEAT = bytearray([0x01])
    __PKT_CLOSE = bytearray([0x04])

    # Account
    __PKT_REQUEST_ACCOUNT_CREATE = bytearray([0x02, 0x01, 0x01])
    __PKT_REQUEST_ACCOUNT_ENTER = bytearray([0x02, 0x01, 0x02])

    # Message
    __PKT_REQUEST_MESSAGE_SEND = bytearray([0x02, 0x02])

    def __init__(self, backend, host: str, port: int) -> None:
        self.__backend = backend
        self.__HOST = host
        self.__PORT = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection_status = False

        self.__sent_message = Message(self.__PKT_HEARTBEAT)
        self.__received_message = Message()

    def connect(self) -> None:
        """
        Старт потока подключения к серверу
        """
        threading.Thread(target=self.__connect_thread).start()

    def __connect_thread(self) -> None:
        """
        Подключение к серверу в отдельном потоке, чтобы задержка между обменами пакетами не останавливала работу приложения
        """
        try:
            self.__server.connect((self.__HOST, self.__PORT))
            self.__connection_status = True
            threading.Thread(target=self.communicating).start()
        except ConnectionRefusedError:
            self.__connection_status = False

    def disconnect(self) -> None:
        """
        Отправка пакета о закрытии соединения, чтобы сервер перестал читать пакеты воизбежания ConnectionRefusedError
        """
        self.__sent_message.update(self.__PKT_CLOSE)

    def communicating(self) -> None:
        """
        Поток обмена пакетами с сервером
        """
        while self.__connection_status:
            try:
                if self.__sent_message.bytes()[0] == self.__sent_message.CLOSE:
                    self.__connection_status = False

                self.__server.send(self.__sent_message.bytes())
                self.__sent_message.update(self.__PKT_HEARTBEAT)

                self.__receiving_message_handle()

                time.sleep(self.__sent_message.timeout())

            except ConnectionResetError:  # Для безопасного закрытия соединения при резком завершении работы сервера
                self.__connection_status = False

        time.sleep(Message.timeout())
        self.__server.close()

    def __receiving_message_handle(self):
        """
        Обработка входящих пакетов
        """
        self.__received_message.update(self.__server.recv(self.__received_message.BUFFER_SIZE))
        message = self.__received_message.bytes()

        if message[0] == self.__received_message.RESPONSE:
            if message[1] == self.__received_message.ACCOUNT:
                if message[2] == self.__received_message.CREATE:
                    if message[3] == self.__received_message.SUCCESS:
                        self.__backend.change_to_messaging()
                    else:
                        notification = self.__received_message.decode_responce_account_unsuccess()
                        self.__backend.show_notification(notification)

                elif message[2] == self.__received_message.ENTER:
                    if message[3] == self.__received_message.SUCCESS:
                        self.__backend.change_to_messaging()
                    else:
                        notification = self.__received_message.decode_responce_account_unsuccess()
                        self.__backend.show_notification(notification)

            elif message[1] == self.__received_message.MESSAGE:
                if message[2] == self.__received_message.SEND:
                    notification = self.__received_message.decode_responce_message_send()
                    self.__backend.show_notification(notification)

                elif message[2] == self.__received_message.RECEIVE:  # Это сообщение сервер отправил без очереди
                    sender_lenght = message[3]

                    sender: str = message[4:4+sender_lenght].decode('utf-8')
                    message_text: str = message[4+sender_lenght:].decode('utf-8')

                    print(sender, message_text)

                    self.__receiving_message_handle()  # снова читаем пакет, чтобы соблюсти очередность

    def create_account(self, login: str, password: str) -> None:
        """
        Метод для формирования пакета с запросом создания аккаунта
        """
        login_length = bytearray(len(login).to_bytes(1, 'big'))

        login_text = bytearray(login.encode('utf-8'))
        password_text = bytearray(password.encode('utf-8'))

        pkt = self.__PKT_REQUEST_ACCOUNT_CREATE + login_length + login_text + password_text

        self.__sent_message.update(pkt)

    def enter_account(self, login: str, password: str) -> None:
        """
        Метод для формирования пакета с запросом об авторизации
        """
        login_length = bytearray(len(login).to_bytes(1, 'big'))

        login_text = bytearray(login.encode('utf-8'))
        password_text = bytearray(password.encode('utf-8'))

        pkt = self.__PKT_REQUEST_ACCOUNT_ENTER + login_length + login_text + password_text

        self.__sent_message.update(pkt)

    def send_message(self, receiver: str, message: str) -> None:
        """
        Метод для формирования пакета с запросом об отправке сообщения
        """
        receiver_length = bytearray(len(receiver).to_bytes(1, 'big'))

        receiver_text = bytearray(receiver.encode('utf-8'))
        message_text = bytearray(message.encode('utf-8'))

        pkt = self.__PKT_REQUEST_MESSAGE_SEND + receiver_length + receiver_text + message_text

        self.__sent_message.update(pkt)

    def is_connected(self) -> bool:
        """
        Получение статуса подключения
        """
        return self.__connection_status

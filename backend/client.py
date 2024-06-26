import socket
import threading
import time
import pickle

from .message import Message


class Client:
    __PKT_HEARTBEAT = bytearray([0x01])
    __PKT_CLOSE = bytearray([0x04])

    # Account
    __PKT_REQUEST_ACCOUNT_CREATE = bytearray([0x02, 0x01, 0x01])
    __PKT_REQUEST_ACCOUNT_ENTER = bytearray([0x02, 0x01, 0x02])

    # Message
    __PKT_REQUEST_MESSAGE_SEND = bytearray([0x02, 0x02, 0x03])
    __PKT_REQUEST_MESSAGE_GETALL = bytearray([0x02, 0x02, 0x05])

    # Users
    __PKT_REQUEST_USERS_GETALL = bytearray([0x02, 0x03, 0x05])

    def __init__(self, backend, host: str, port: int) -> None:
        self.__backend = backend
        self.__HOST = host
        self.__PORT = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection_status = False

        self.__sent_message = Message(self.__PKT_HEARTBEAT)
        self.__received_message = Message()

        self.__login = None

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
            threading.Thread(target=self.__sending_message_handle).start()
        except ConnectionRefusedError:
            self.__connection_status = False

    def disconnect(self) -> None:
        """
        Отправка пакета о закрытии соединения, чтобы сервер перестал читать пакеты воизбежания ConnectionRefusedError
        """
        self.__sent_message.update(self.__PKT_CLOSE)

    def __sending_message_handle(self) -> None:
        """
        Поток обмена пакетами с сервером
        """
        while self.__connection_status:
            try:
                if self.__sent_message.bytes()[0] == self.__sent_message.CLOSE:
                    self.__connection_status = False
                    self.__server.send(self.__sent_message.bytes())
                    break

                self.__server.send(self.__sent_message.bytes())
                self.__sent_message.update(self.__PKT_HEARTBEAT)

                self.__receiving_message_handle()

                time.sleep(self.__sent_message.timeout())

            except ConnectionAbortedError:  # Для безопасного закрытия соединения при резком завершении работы сервера
                self.__connection_status = False

        self.__server.close()

    def __receiving_message_handle(self) -> None:
        """
        Обработка входящих пакетов
        """
        self.__received_message.update(self.__server.recv(self.__received_message.BUFFER_SIZE))
        recv_message = self.__received_message
        message = self.__received_message.bytes()

        if message[0] == recv_message.RESPONSE:
            if message[1] == recv_message.ACCOUNT:
                if message[2] == recv_message.CREATE or message[2] == recv_message.ENTER:
                    if message[3] == recv_message.SUCCESS:
                        self.__backend.change_to_messaging()
                    else:
                        notification = recv_message.decode_responce_account_unsuccess()
                        self.__backend.show_notification(notification)

            elif message[1] == recv_message.MESSAGE:
                if message[2] == recv_message.SEND:
                    pass

                elif message[2] == recv_message.RECEIVE:  # Это сообщение сервер отправил без очереди
                    sender_lenght = message[3]

                    sender: str = message[4:4+sender_lenght].decode('utf-8')
                    message_text: str = message[4+sender_lenght:].decode('utf-8')

                    self.__backend.message_received(sender, message_text)

                    self.__receiving_message_handle()  # снова читаем пакет, чтобы соблюсти очередность

                elif message[2] == recv_message.GETALL:
                    res = bytearray()

                    data = recv_message.bytes()

                    parts_count = int.from_bytes(data[3:6], byteorder='little')

                    payload = data[6:]
                    res += payload

                    for i in range(parts_count - 1):
                        data = bytearray(self.__server.recv(Message.BUFFER_SIZE))
                        payload = data[6:]
                        res += payload

                    self.__backend.display_messages_from_server_after_loading(pickle.loads(res))

            elif message[1] == recv_message.USERS:
                if message[2] == recv_message.GETALL:
                    res = bytearray()

                    data = recv_message.bytes()

                    parts_count = int.from_bytes(data[3:6], byteorder='little')

                    payload = data[6:]
                    res += payload

                    for i in range(parts_count - 1):
                        data = bytearray(self.__server.recv(Message.BUFFER_SIZE))
                        payload = data[6:]
                        res += payload

                    result_array: list[tuple[str]] = pickle.loads(res)

                    self.__backend.display_found_users([user[0] for user in result_array], self.__login)

    def create_account(self, login: str, password: str) -> None:
        """
        Метод для формирования пакета с запросом создания аккаунта
        """
        self.__login = login

        login_length = bytearray(len(login).to_bytes(1, 'big'))

        login_text = bytearray(login.encode('utf-8'))
        password_text = bytearray(password.encode('utf-8'))

        pkt = self.__PKT_REQUEST_ACCOUNT_CREATE + login_length + login_text + password_text

        self.__sent_message.update(pkt)

    def enter_account(self, login: str, password: str) -> None:
        """
        Метод для формирования пакета с запросом об авторизации
        """
        self.__login = login

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

    def send_load_messages_request(self) -> None:
        """
        Метод для формирования пакета с запросом о получении сообщений
        """
        self.__sent_message.update(self.__PKT_REQUEST_MESSAGE_GETALL)

    def get_users_by_nickname_request(self, nickname: str) -> None:
        """
        Метод для формирования запроса на получение пользователей по введённому логину в строке search
        """
        nickname_text = bytearray(nickname.encode('utf-8'))

        pkt = self.__PKT_REQUEST_USERS_GETALL + nickname_text
        self.__sent_message.update(pkt)

    def handle_responce(self, message: bytearray):
        pass

    def is_connected(self) -> bool:
        """
        Получение статуса подключения
        """
        return self.__connection_status

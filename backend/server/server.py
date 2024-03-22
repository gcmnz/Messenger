import socket
import threading

from database import AccountDatabase, MessageDatabase
from backend.message import Message
import json


class Server:
    """
    Константные пакеты для взаимодействия с клиентом
    """
    __PKT_HEARTBEAT = bytearray([0x01])

    # Account
    __PKT_RESPONCE_ACCOUNT_CREATE_FAIL_ALREADY_EXISTS = (
        bytearray([0x03, 0x01, 0x01, 0x00, 0x01]))
    __PKT_RESPONCE_ACCOUNT_CREATE_SUCCESS_CREATED = (
        bytearray([0x03, 0x01, 0x01, 0x01, 0x04]))
    __PKT_RESPONCE_ACCOUNT_ENTER_FAIL_INVALID_LOGIN = (
        bytearray([0x03, 0x01, 0x02, 0x00, 0x02]))
    __PKT_RESPONCE_ACCOUNT_ENTER_FAIL_INVALID_PASSWORD = (
        bytearray([0x03, 0x01, 0x02, 0x00, 0x03]))
    __PKT_RESPONCE_ACCOUNT_ENTER_SUCCESS_PASSED = (
        bytearray([0x03, 0x01, 0x02, 0x01, 0x05]))

    # Message
    __PKT_RESPONCE_MESSAGE_SEND_FAIL_RECEIVER_DOESNT_EXISTS = (
        bytearray([0x03, 0x02, 0x03, 0x00, 0x06]))
    __PKT_RESPONCE_MESSAGE_SEND_FAIL_SEND_TO_SELF = (
        bytearray([0x03, 0x02, 0x03, 0x00, 0x07]))
    __PKT_RESPONCE_MESSAGE_SEND_SENDED = (
        bytearray([0x03, 0x02, 0x03, 0x01, 0x08]))
    __PKT_RESPONCE_MESSAGE_RECEIVE = (
        bytearray([0x03, 0x02, 0x04])
    )

    def __init__(self, host: str, port: int) -> None:
        self.__HOST: str = host
        self.__PORT: int = port
        self.__starting: bool = False
        self.__server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP

        self.__accounts_database = AccountDatabase()
        self.__messages_database = MessageDatabase()

        self.__online_users: dict = {}

    def __del__(self) -> None:
        self.stop()

    def start(self) -> None:
        """
        Запуск сервера и приёма подключений
        """
        print(f'Server started: {self.__HOST} | {self.__PORT}')
        self.__server.bind((self.__HOST, self.__PORT))
        self.__server.listen()
        self.__starting = True
        self.connection_listener()

    def stop(self) -> None:
        print(f'Server closed: {self.__HOST} | {self.__PORT}')
        self.__starting = False
        self.__server.close()

    def connection_listener(self) -> None:
        """
        Метод для отслеживания подключений
        """
        while self.__starting:
            client, addr = self.__server.accept()
            threading.Thread(target=self.communicating, args=(client, addr)).start()

    def communicating(self, client: socket.socket, addr: tuple) -> None:
        """
        Метод, реагирующий на подключение и взаимодействующий с клиентом в отдельном потоке (N подключений = N потоков)
        """
        print(f'{addr} Successfully connected!')

        received_message = Message()
        sent_message = Message(self.__PKT_HEARTBEAT)
        current_login = None

        user_connected = True
        while user_connected:
            received_message.update(client.recv(received_message.BUFFER_SIZE))
            message = received_message.bytes()

            if message[0] == received_message.REQUEST:
                if message[1] == received_message.ACCOUNT:
                    login, password = received_message.decode_request_account()

                    if message[2] == received_message.CREATE:
                        success = not self.__accounts_database.check_login_exists(login)
                        if success:
                            self.__accounts_database.add_user(login, password)
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_CREATE_SUCCESS_CREATED)
                            current_login = login
                            self.__online_users[login] = client
                        else:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_CREATE_FAIL_ALREADY_EXISTS)

                    elif message[2] == received_message.ENTER:
                        success = self.__accounts_database.check_account_password(login, password)

                        if success == 2:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_ENTER_SUCCESS_PASSED)
                            current_login = login
                            self.__online_users[login] = client
                        elif success == 1:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_ENTER_FAIL_INVALID_PASSWORD)
                        elif success == 0:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_ENTER_FAIL_INVALID_LOGIN)

                elif message[1] == received_message.MESSAGE:
                    receiver, message_ = received_message.decode_request_message()

                    if not self.__accounts_database.check_login_exists(receiver):  # Если аккаунта получателя не существует
                        sent_message.update(self.__PKT_RESPONCE_MESSAGE_SEND_FAIL_RECEIVER_DOESNT_EXISTS)
                    elif receiver == current_login:  # Пытаемся отправить себе
                        sent_message.update(self.__PKT_RESPONCE_MESSAGE_SEND_FAIL_SEND_TO_SELF)
                    else:
                        sender = current_login
                        self.__messages_database.add_message(sender, receiver, message_)
                        sent_message.update(self.__PKT_RESPONCE_MESSAGE_SEND_SENDED)

                        # if receiver in self.__online_users:
                        #     msg = Message(self.__PKT_RESPONCE_MESSAGE_RECEIVE)
                        #     msg.encode_responce_message_receive(sender, message_)
                        #
                        #     self.__online_users[receiver].send(msg.bytes())

                        # todo remove
                        msg = Message(self.__PKT_RESPONCE_MESSAGE_RECEIVE)
                        msg.encode_responce_message_receive(sender, message_)

                        self.__online_users[sender].send(msg.bytes())
                        # todo remove

            elif message[0] == received_message.CLOSE:
                user_connected = False

                if current_login in self.__online_users:
                    del self.__online_users[current_login]

                print(f'{addr} Disconnected!')

            client.send(sent_message.bytes())
            sent_message.update(self.__PKT_HEARTBEAT)


if __name__ == '__main__':
    with open('../../config.json') as f:
        config = json.load(f)

    server = Server(config['ip'], config['port'])
    server.start()

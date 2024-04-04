import pickle
import json
import asyncio

from database import AccountDatabase, MessageDatabase
from backend.message import Message


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
    __PKT_RESPONCE_MESSAGE_SEND_SUCCESS_SENDED = (
        bytearray([0x03, 0x02, 0x03, 0x01, 0x08]))
    __PKT_RESPONCE_MESSAGE_RECEIVE = (
        bytearray([0x03, 0x02, 0x04])
    )
    __PKT_RESPONCE_MESSAGE_GETALL = (
        bytearray([0x03, 0x02, 0x05])
    )

    # Users
    __PKT_RESPONCE_USERS_GETALL = (
        bytearray([0x03, 0x03, 0x05])
    )

    def __init__(self, host: str, port: int) -> None:
        self.__HOST: str = host
        self.__PORT: int = port
        self.__starting: bool = False

        self.__server = None

        self.__accounts_database = AccountDatabase()
        self.__messages_database = MessageDatabase()

        self.__online_users: dict = {}

    def __del__(self) -> None:
        asyncio.run(self.stop())

    async def stop(self) -> None:
        if self.__server is not None:
            self.__server.close()
            await self.__server.wait_closed()
            print(f"Server stopped: {self.__HOST} | {self.__PORT}")

    def start(self) -> None:
        asyncio.run(self.__async_start())

    async def __async_start(self) -> None:
        print(f'Server started: {self.__HOST} | {self.__PORT}')
        self.__server = await asyncio.start_server(self.handle_client, self.__HOST, self.__PORT)
        async with self.__server:
            await self.__server.serve_forever()

    async def handle_client(self, reader, writer) -> None:
        # Получаем информацию о соединении
        peername = writer.get_extra_info('peername')
        if peername is not None:
            ip, port = peername
            print(f"Client connected: {ip}:{port}")
        else:
            ip, port = None, None
            print("Client connected, but could not get IP address")

        received_message = Message()
        sent_message = Message(self.__PKT_HEARTBEAT)
        current_login = None

        while True:
            received_message.update((await reader.read(received_message.BUFFER_SIZE)))
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
                            self.__online_users[login] = reader
                        else:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_CREATE_FAIL_ALREADY_EXISTS)

                    elif message[2] == received_message.ENTER:
                        success = self.__accounts_database.check_account_password(login, password)

                        if success == 2:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_ENTER_SUCCESS_PASSED)
                            current_login = login
                            self.__online_users[login] = reader
                        elif success == 1:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_ENTER_FAIL_INVALID_PASSWORD)
                        elif success == 0:
                            sent_message.update(self.__PKT_RESPONCE_ACCOUNT_ENTER_FAIL_INVALID_LOGIN)

                elif message[1] == received_message.MESSAGE:
                    if message[2] == received_message.SEND:
                        receiver, message_ = received_message.decode_request_message()

                        if not self.__accounts_database.check_login_exists(receiver):  # Если аккаунта получателя не существует
                            sent_message.update(self.__PKT_RESPONCE_MESSAGE_SEND_FAIL_RECEIVER_DOESNT_EXISTS)
                        elif receiver == current_login:  # Пытаемся отправить себе
                            sent_message.update(self.__PKT_RESPONCE_MESSAGE_SEND_FAIL_SEND_TO_SELF)
                        else:
                            sender = current_login
                            self.__messages_database.add_message(sender, receiver, message_)
                            sent_message.update(self.__PKT_RESPONCE_MESSAGE_SEND_SUCCESS_SENDED)

                            if receiver in self.__online_users:
                                msg = Message(self.__PKT_RESPONCE_MESSAGE_RECEIVE)
                                msg.encode_responce_message_receive(sender, message_)

                                self.__online_users[receiver].send(msg.bytes())

                    elif message[2] == received_message.GETALL:
                        data_dict = self.__messages_database.get_all_messages_for(current_login)

                        payload = bytearray(pickle.dumps(data_dict))

                        # Подготовка заголовка
                        msg_pkt = self.__PKT_RESPONCE_MESSAGE_GETALL
                        self.__getall_handler(writer, msg_pkt, payload)

                elif message[1] == received_message.USERS:
                    if message[2] == received_message.GETALL:
                        nickname_to_find = received_message.decode_responce_users_getall()
                        found_nicknames = self.__accounts_database.get_all_users_by(nickname_to_find)

                        payload = pickle.dumps(found_nicknames)
                        msg_pkt = self.__PKT_RESPONCE_USERS_GETALL

                        self.__getall_handler(writer, msg_pkt, payload)

            elif message[0] == received_message.CLOSE:
                if current_login in self.__online_users:
                    del self.__online_users[current_login]

                await writer.drain()
                writer.close()

                if ip:
                    print(f"Client disconnected: {ip}:{port}")
                else:
                    print('Client disconnected: unknown')
                break

            writer.write(sent_message.bytes())
            sent_message.update(self.__PKT_HEARTBEAT)

    @staticmethod
    def __getall_handler(writer, msg_pkt, payload):
        """
        Метод для разбива пакетов на части и отправки после типа сообщения GETALL
        """
        parts_count = len(payload) // (Message.BUFFER_SIZE - len(msg_pkt) - 3) + 1
        parts_ct = bytearray(parts_count.to_bytes(3, byteorder='little'))

        pkt = msg_pkt + parts_ct

        result_packet = bytearray()
        result_payload = bytearray()

        for i in range(parts_count):
            pl = payload[i * (Message.BUFFER_SIZE - len(msg_pkt) - 3):(i + 1) * (Message.BUFFER_SIZE - len(msg_pkt) - 3)]
            packet = (pkt + pl)
            result_packet += packet
            result_payload += pl
            writer.write(packet)


if __name__ == '__main__':
    with open('../../config.json') as f:
        config = json.load(f)

    async_server = Server(config['ip'], config['port'])
    async_server.start()

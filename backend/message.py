
class Message:
    __TIMEOUT = 0.1
    BUFFER_SIZE = 512

    # 1 byte - type
    HEARTBEAT = 1
    REQUEST = 2
    RESPONSE = 3
    CLOSE = 4

    # 2 byte
    ACCOUNT = 1
    MESSAGE = 2
    USERS = 3

    # 3 byte
    CREATE = 1
    ENTER = 2
    SEND = 3
    RECEIVE = 4
    GETALL = 5

    # 4 byte - status
    SUCCESS = 1
    FAIL = 0

    # 5 byte - reason
    ALREADY_EXISTS = 1
    INVALID_LOGIN = 2
    INVALID_PASSWORD = 3
    CREATED = 4
    PASSED = 5
    RECEIVER_DOESNT_EXISTS = 6
    SEND_TO_SELF = 7
    SENDED = 8

    def __init__(self, packet: bytearray = None):
        self.__packet = packet

    def bytes(self) -> bytearray:
        """
        Метод для получения пакета в байтах
        """
        return self.__packet

    def update(self, packet):
        """
        Метод, переопределяющий аттрибут пакета, чтобы не создавать отдельный объект
        """
        self.__packet = packet

    def decode_request_account(self) -> tuple[str, str]:
        """
        Метод для получения логина и пароля при запросе ACCOUNT на сервер
        """
        pkt = self.__packet
        login_length = pkt[3]

        login = pkt[4: 4 + login_length].decode('utf-8')
        password = pkt[4 + login_length:].decode('utf-8')

        return login, password

    def decode_responce_account_unsuccess(self) -> str:
        """
        Метод для получения текста ошибки из пакета
        """
        pkt = self.__packet
        if pkt[4] == 1:
            return 'Аккаунт уже существует'
        elif pkt[4] == 2:
            return 'Такого аккаунта не существует'
        elif pkt[4] == 3:
            return 'Неверный пароль'

    def decode_request_message(self) -> tuple[str, str]:
        """
        Метод для вывода результата отправки сообщения
        """
        pkt = self.__packet
        receiver_length = pkt[3]

        receiver = pkt[4: 4 + receiver_length].decode('utf-8')
        message = pkt[4 + receiver_length:].decode('utf-8')

        return receiver, message

    def decode_responce_message_send(self) -> str:
        pkt = self.__packet
        if pkt[3] == self.SUCCESS:
            return 'Сообщение доставлено'
        else:
            if pkt[4] == self.SEND_TO_SELF:
                return 'Нельзя отправить себе'
            elif pkt[4] == self.RECEIVER_DOESNT_EXISTS:
                return 'Получателя не существует'

    def encode_responce_message_receive(self, sender: str, message: str) -> None:
        """
        Метод для кодировки сообщения об отправителе и тексте сообщения для передачи клиенту получателя
        """
        pkt = self.__packet
        sender_length = int.to_bytes(len(sender), 1, byteorder='little')
        self.__packet = pkt + sender_length + sender.encode('utf-8') + message.encode('utf-8')

    def decode_responce_users_getall(self) -> str:
        """
        Метод для получения искомого nickname из пакета
        """
        pkt = self.__packet
        return pkt[3:].decode('utf-8')

    @classmethod
    def timeout(cls):
        """
        Задержка между обменами пакетами (client - send | server - receive -> server - send | client- receive)
        """
        return cls.__TIMEOUT

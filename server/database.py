import sqlite3
import hashlib
from datetime import datetime


class Database:
    """
    Родительский класс для СУБД
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.connection = sqlite3.connect(self.filename, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __del__(self) -> None:
        self.cursor.close()
        self.connection.close()

    def create_table(self, *args) -> None:
        """
        usage: create_table(table_name, column_names ...)
        example: create_table('accounts', 'login', 'password', 'online_status')
        """
        # открываем базу
        with self.connection:
            # получаем количество таблиц с нужным нам именем
            data = self.connection.execute(
                f"select count(*) from sqlite_master where type='table' and name='{args[0]}'")
            for row in data:
                # если таких таблиц нет
                if row[0] == 0:
                    # создаём таблицу
                    with self.connection:
                        names = ''
                        for name in args[1:]:
                            if name == args[-1]:
                                names += f'{name} VARCHAR'
                            else:
                                names += f'{name} VARCHAR,\n'

                        self.connection.execute(f"""
                            CREATE TABLE {args[0]} (
                                {names}
                            );
                        """)

    def delete_table(self, table_name: str) -> None:
        with self.connection:
            self.cursor.execute(f'DROP TABLE {table_name};')

    def clear(self, table_name) -> None:
        with self.connection:
            self.cursor.execute(f"DELETE FROM {table_name}")

    def get_table_content(self, table_name: str):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            return self.cursor.fetchall()

    @staticmethod
    def create_password_hash(password: str) -> str:
        """
        Хеширование пароля (типо средство защиты)
        """
        return hashlib.sha256(password.encode()).hexdigest()


class AccountDatabase(Database):
    """
    Класс для управления базой с аккаутами
    """
    def __init__(self) -> None:
        super().__init__('databases/accounts.db')

    def add_user(self, login: str, password: str) -> None:
        """
        Добавления только что созданного аккаунта в базу
        """
        password = self.create_password_hash(password)
        with self.connection:
            self.connection.execute('INSERT INTO accounts (login, password) VALUES (?, ?)', (login, password))
            self.connection.commit()

    def remove_user(self, login: str) -> None:
        """
        Удаление аккаунта
        """
        with self.connection:
            self.connection.execute('DELETE FROM accounts WHERE Login = ?', (login,))
            self.connection.commit()

    def check_login_exists(self, login: str) -> bool:
        """
        Проверка на существование аккаунта
        """
        self.cursor.execute('SELECT * FROM accounts WHERE login=?', (login,))
        return bool(self.cursor.fetchone())

    def check_account_password(self, login: str, password: str) -> int:
        """
        Проверка для проверки пароля
        """
        if self.check_login_exists(login):
            self.cursor.execute('SELECT password FROM accounts WHERE login=?', (login,))
            if self.cursor.fetchone()[0] == self.create_password_hash(password):
                return 2
            return 1
        return 0

    def get_all_users_by(self, desired_login: str) -> list[str]:
        """
        Метод возвращает список из пользователей, в логинах которых есть desired_login
        """
        with self.connection:
            result = self.cursor.execute(f"SELECT login FROM accounts WHERE login LIKE '{desired_login}%'").fetchall()

        return result


class MessageDatabase(Database):
    """
    Класс для управления базой с сообщениями
    """
    def __init__(self) -> None:
        super().__init__('databases/messages.db')

    def __is_table_exists(self, sender: str, receiver: str) -> int:
        """
        Проверка на наличие переписки отправителя с получателем
        :return:
        0 если нет
        1 если порядок неверный (sender = receiver)
        2 если порядок верный (sender = sender)
        """
        with self.connection:
            return_1 = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{receiver}_{sender}'").fetchone()
            if not return_1:
                return_2 = self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{sender}_{receiver}'").fetchone()
                if not return_2:
                    return 0
                return 2
            return 1

    def add_message(self, sender: str, receiver: str, message: str) -> None:
        """
        Метод для добавления сообщения в базу
        """
        status = self.__is_table_exists(sender, receiver)
        date = datetime.now().strftime('%Y.%m.%d')
        time_ = str(datetime.now().time())

        if status == 1:
            with self.connection:
                self.cursor.execute(f'INSERT INTO "{receiver}_{sender}" (is_sender, message, date, time) VALUES (?, ?, ?, ?)',
                                    (0, message, date, time_))
        elif status == 2:
            with self.connection:
                self.cursor.execute(f'INSERT INTO "{sender}_{receiver}" (is_sender, message, date, time) VALUES (?, ?, ?, ?)',
                                    (1, message, date, time_))
        else:
            self.create_table(f'{sender}_{receiver}', 'is_sender', 'message', 'date', 'time')
            with self.connection:
                self.cursor.execute(f'INSERT INTO "{sender}_{receiver}" (is_sender, message, date, time) VALUES (?, ?, ?, ?)',
                                    (1, message, date, time_))

    def get_all_messages_for(self, login: str) -> dict:
        """
        Получение из базы всех переписок с пользователями от login
        """
        with self.connection:
            all_tables_fetch = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            all_tables = [table[0] for table in all_tables_fetch]
            tables = [table for table in all_tables if login in table]
            result: dict = {}

            for table in tables:
                interlocutor = list(set(table.split('_')) - {login})[0]
                content = self.get_table_content(table)
                content.append(int(login == table.split('_')[0]))
                result[interlocutor] = content

            return result


if __name__ == '__main__':
    # database = AccountDatabase()
    database = MessageDatabase()

from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class ListInterlocutor(QListWidget):
    def __init__(self):
        super().__init__()
        self.__current_items: list = []

    def save_current_items(self):
        self.__current_items = [self.item(i) for i in range(self.count())]

    def sort_by_searching(self, users: list[str]) -> None:
        """
        Алгоритм сортировки пользователей и добавления items в listwidget
        """
        self.clear()

        for user in users:
            # Находим элемент в self.__current_items, у которого interlocutor равен user
            found_item = next((item for item in self.__current_items if item.interlocutor == user), None)
            if found_item:
                # Создаем новый ListItem на основе найденного элемента
                new_item = ListItem(found_item.interlocutor, found_item.messages, found_item.is_sender)
                self.addItem(new_item)
            else:
                list_item = ListItem(user, [], 0)
                self.addItem(list_item)

    def restore_items(self) -> None:
        """
        Метод для отображения только тех пользователей, с которыми есть переписка (вызывается при пустом поле поиска)
        """
        self.clear()

        for item in self.__current_items:
            new_item = ListItem(item.interlocutor, item.messages, item.is_sender)
            self.addItem(new_item)

    def add_current_item(self, item) -> None:
        """
        Добавление новой переписки, при отправке сообщения только что найденному через поиск пользователю
        """
        self.__current_items.append(item)

    def get_current_items(self) -> list:
        """
        Получение массива всех пользователей, с которыми есть переписка
        """
        return self.__current_items


class ListItem(QListWidgetItem):
    def __init__(self, interlocutor: str, messages: list[tuple], is_sender: int) -> None:
        super().__init__(interlocutor)

        self.interlocutor: str = interlocutor
        self.messages: list[tuple] = messages
        self.is_sender: int = is_sender

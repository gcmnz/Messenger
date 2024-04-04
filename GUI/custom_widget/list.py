from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class ListInterlocutor(QListWidget):
    def __init__(self):
        super().__init__()
        self.original_items = []

    # def save_current_items(self):
    #     self.original_items = [self.item(i) for i in range(self.count())]
    #
    # def set_items(self, users: list[tuple[str]]):
    #     self.clear()
    #     # Добавление новых элементов
    #     for user in users:
    #         # Проверяем, есть ли пользователь в списке original_items
    #         original_item = next((item for item in self.original_items if item.interlocutor == user[0]), None)
    #         if original_item:
    #             # Если пользователь найден, создаем ListItem с атрибутами original_item
    #             list_item = ListItem(original_item.interlocutor, original_item.messages, original_item.is_sender)
    #         else:
    #             # Если пользователь не найден, создаем ListItem с новыми значениями
    #             list_item = ListItem(user[0], [], 0)
    #         self.addItem(list_item)
    #
    # def restore_original_items(self):
    #     # Удаление всех текущих элементов
    #     self.clear()
    #     # Добавление обратно исходных элементов
    #     for item in self.original_items:
    #         new_item = ListItem(item.interlocutor, item.messages, item.is_sender)
    #         self.addItem(new_item)

    def sort(self, users: list[tuple[str]]):
        for i in range(self.count()):
            current_item = self.item(i)

            if not any(current_item.interlocutor in user for user in users):
                current_item.setHidden(True)
            else:
                current_item.setHidden(False)

    def show_all_items(self):
        for i in range(self.count()):
            self.item(i).setHidden(False)


class ListItem(QListWidgetItem):
    def __init__(self, interlocutor: str, messages: list[tuple], is_sender: int):
        super().__init__(interlocutor)

        self.interlocutor = interlocutor
        self.messages = messages
        self.is_sender = is_sender

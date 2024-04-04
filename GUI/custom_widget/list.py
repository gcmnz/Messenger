from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class ListInterlocutor(QListWidget):
    def __init__(self):
        super().__init__()

    def sort_by_searching(self, users: list[tuple[str]]) -> None:
        for i in range(self.count()):
            current_item = self.item(i)

            # noinspection PyUnresolvedReferences
            if not any(current_item.interlocutor in user for user in users):
                current_item.setHidden(True)
            else:
                current_item.setHidden(False)

    def show_all_items(self) -> None:
        for i in range(self.count()):
            self.item(i).setHidden(False)


class ListItem(QListWidgetItem):
    def __init__(self, interlocutor: str, messages: list[tuple], is_sender: int) -> None:
        super().__init__(interlocutor)

        self.interlocutor: str = interlocutor
        self.messages: list[tuple] = messages
        self.is_sender: int = is_sender

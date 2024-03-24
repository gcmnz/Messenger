from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class ListInterlocutor(QListWidget):
    def __init__(self):
        super().__init__()


class ListItem(QListWidgetItem):
    def __init__(self, interlocutor: str, messages: list[tuple], is_sender: int):
        super().__init__(interlocutor)

        self.interlocutor = interlocutor
        self.messages = messages
        self.is_sender = is_sender

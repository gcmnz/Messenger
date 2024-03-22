from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class ListInterlocutor(QListWidget):
    def __init__(self):
        super().__init__()


class ListMessages(QListWidget):
    def __init__(self):
        super().__init__()


class ListItem(QListWidgetItem):
    def __init__(self, text: str):
        super().__init__(text)

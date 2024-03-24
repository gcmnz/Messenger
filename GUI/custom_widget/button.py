from PyQt5.QtWidgets import QPushButton
from PyQt5.Qt import Qt


class AuthorizationButton(QPushButton):
    def __init__(self, text: str, func: staticmethod) -> None:
        super().__init__()

        self.setText(text)
        self.__on_click = func

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__on_click()


class SendMessageButton(QPushButton):
    def __init__(self, text: str, func: staticmethod) -> None:
        super().__init__()

        self.setText(text)
        self.__on_click = func

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.__on_click:
                self.__on_click()


class MessageButton(QPushButton):
    def __init__(self, text: str) -> None:
        super().__init__()

        self.setText(text)

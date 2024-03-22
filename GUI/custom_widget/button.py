from PyQt5.QtWidgets import QPushButton
from PyQt5.Qt import Qt


class AuthorizationButton(QPushButton):
    def __init__(self, widget, text: str, func: staticmethod) -> None:
        super().__init__(widget)

        self.__widget = widget
        self.setText(text)
        self.__on_click = func

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__on_click()

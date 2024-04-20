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
        self.setStyleSheet("""
        background-color: rgb(33, 55, 80);
        
        min-width: 100px;
        max-width: 350px;
        
        min-height: 30px;
        
        margin: 2px 2px 0px 0px;
        padding: 0px 10px 0px 10px;
        border-radius: 15px;
        font-size: 13px;
        color: rgba(255, 255, 255, 180);""")

        self.setText(text)

    def line_break(self, strings_count: int) -> None:
        current_text = self.text()
        for string_num in range(strings_count):
            print(current_text[string_num])

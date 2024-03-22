from PyQt5.QtWidgets import QLineEdit


class AuthorizationTextField(QLineEdit):
    def __init__(self, window, text: str) -> None:
        super().__init__(window)

        self.setPlaceholderText(text)

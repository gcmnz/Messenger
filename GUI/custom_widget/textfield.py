from PyQt5.QtWidgets import QLineEdit


class AuthorizationTextField(QLineEdit):
    def __init__(self, text: str) -> None:
        super().__init__()

        self.setPlaceholderText(text)


class AuthorizationPasswordTextField(AuthorizationTextField):
    def __init__(self, text: str):
        super().__init__(text)

        self.setEchoMode(QLineEdit.Password)


class EnterMessageTextField(QLineEdit):
    def __init__(self, text: str) -> None:
        super().__init__()

        self.setPlaceholderText(text)


class SearchUserTextField(QLineEdit):
    def __init__(self, text: str) -> None:
        super().__init__()

        self.setPlaceholderText(text)

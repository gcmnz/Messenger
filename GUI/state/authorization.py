from GUI.custom_widget.button import AuthorizationButton
from GUI.custom_widget.textfield import AuthorizationTextField, AuthorizationPasswordTextField
from GUI.custom_widget.label import AuthorizationLabel

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.Qt import Qt


class Authorization(QWidget):
    def __init__(self, backend) -> None:
        super().__init__()

        self.login = AuthorizationTextField('Login')
        self.password = AuthorizationPasswordTextField('Password')

        self.login.setText('slavique')
        self.password.setText('ez')

        self.enter = AuthorizationButton('Sign in', backend.enter_account_button_func)
        self.create_account_button = AuthorizationButton('Create account', backend.change_to_registration)

        self.notification = AuthorizationLabel()

        self.__layout = QVBoxLayout()
        self.__layout.addWidget(self.login)
        self.__layout.addWidget(self.password)
        self.__layout.addWidget(self.enter)
        self.__layout.addWidget(self.create_account_button)
        self.__layout.addWidget(self.notification)
        self.__layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.__layout)

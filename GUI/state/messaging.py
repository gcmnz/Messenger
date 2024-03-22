from GUI.custom_widget.list import ListMessages, ListInterlocutor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QLineEdit
from GUI.custom_widget.label import AuthorizationLabel
from GUI.custom_widget.button import AuthorizationButton
from PyQt5.Qt import Qt


class Messaging(QWidget):
    def __init__(self, backend):
        super().__init__()

        self.__backend = backend

        self.list_interlocutor = ListInterlocutor()
        self.list_messages = ListMessages()

        self.__layout = QHBoxLayout()
        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.list_interlocutor)
        self.__splitter.addWidget(self.list_messages)
        self.__layout.addWidget(self.__splitter)

        self.receiver = QLineEdit()
        self.receiver.setPlaceholderText('receiver')

        self.message = QLineEdit()
        self.message.setPlaceholderText('message')

        self.send_btn = AuthorizationButton(self, 'Send', self.__backend.send_message_button_func)

        self.notification = AuthorizationLabel()

        # self.__layout = QVBoxLayout()
        # self.__layout.addWidget(self.receiver)
        # self.__layout.addWidget(self.message)
        # self.__layout.addWidget(self.send_btn)
        # self.__layout.addWidget(self.notification)
        # self.__layout.setAlignment(Qt.AlignCenter)

        self.setLayout(self.__layout)

    def load_messages(self):
        self.__backend.load_all_messages()

    # todo remove
    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.__backend.change_to_authorization()
    # todo remove

from GUI.custom_widget.list import ListMessages, ListReceivers
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.Qt import Qt


class Messaging(QWidget):
    def __init__(self, backend):
        super().__init__()

        # todo remove
        self.__backend = backend
        # todo remove

        self.receivers = ListReceivers()
        self.messages = ListMessages()

        self.__layout = QHBoxLayout()
        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.receivers)
        self.__splitter.addWidget(self.messages)
        self.__layout.addWidget(self.__splitter)
        self.setLayout(self.__layout)

        # self.receiver = QLineEdit()
        # self.receiver.setPlaceholderText('receiver')
        #
        # self.message = QLineEdit()
        # self.message.setPlaceholderText('message')
        #
        # self.send_btn = AuthorizationButton(self, 'Send', self.__backend.send_message_button_func)
        #
        # self.notification = AuthorizationLabel()
        #
        # self.__layout = QVBoxLayout()
        # self.__layout.addWidget(self.receiver)
        # self.__layout.addWidget(self.message)
        # self.__layout.addWidget(self.send_btn)
        # self.__layout.addWidget(self.notification)
        # self.__layout.setAlignment(Qt.AlignCenter)
        #
        # self.setLayout(self.__layout)

    # todo remove
    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.__backend.change_to_authorization()
    # todo remove

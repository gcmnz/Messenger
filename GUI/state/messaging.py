from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt5.Qt import Qt

from GUI.custom_widget.messages_widget import MessagesWidget
from GUI.custom_widget.interlocutors_widget import InterlocutorsWidget


class Messaging(QWidget):
    def __init__(self, backend):
        super().__init__()

        self.__backend = backend

        self.interlocutors_widget = InterlocutorsWidget(self.__backend)
        self.messages_widget = MessagesWidget(self.__backend)

        self.__splitter = QSplitter(Qt.Horizontal)
        self.__splitter.addWidget(self.interlocutors_widget)
        self.__splitter.addWidget(self.messages_widget)
        self.__splitter.setStretchFactor(1, 1)

        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.__splitter)

        self.setLayout(self.__layout)

    def load_messages(self):
        self.__backend.load_all_messages()

    def on_message_received(self, sender: str, message: str):
        print(f'Получено сообщение от: {sender}: {message}')

    # todo remove
    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.__backend.change_to_authorization()
    # todo remove

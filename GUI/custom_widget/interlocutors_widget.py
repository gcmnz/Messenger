from PyQt5.QtWidgets import QWidget, QVBoxLayout

from .list import ListInterlocutor
from .textfield import SearchUserTextField


class InterlocutorsWidget(QWidget):
    def __init__(self, backend):
        super().__init__()

        self.search_user = SearchUserTextField('Search')
        self.search_user.textChanged[str].connect(backend.find_users_by_nickname)

        self.list_interlocutor = ListInterlocutor()
        # noinspection PyUnresolvedReferences
        self.list_interlocutor.currentItemChanged.connect(backend.on_interlocutor_change)

        self.__vlayout = QVBoxLayout()
        self.__vlayout.addWidget(self.search_user)
        self.__vlayout.addWidget(self.list_interlocutor)
        self.setLayout(self.__vlayout)

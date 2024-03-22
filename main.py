from GUI import *
from backend import *

from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(300, 300)
        self.setGeometry(500, 400, 800, 500)
        self.setMaximumSize(800, 600)

        self.setStyleSheet(WINDOW_STYLE + AUTHORIZATION_STYLE + MESSAGING_STYLE)

        self.backend = Backend(self)

        self.authorization_widget = Authorization(self.backend)
        self.registration_widget = Registration(self.backend)
        self.messaging_widget = Messaging(self.backend)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.authorization_widget)
        self.stacked_widget.addWidget(self.registration_widget)
        self.stacked_widget.addWidget(self.messaging_widget)
        self.setCentralWidget(self.stacked_widget)

        self.backend.set_widget()

    def closeEvent(self, event):
        self.backend.client.disconnect()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

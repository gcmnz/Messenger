from PyQt5.QtWidgets import QLabel
from PyQt5.Qt import Qt


class AuthorizationLabel(QLabel):
    def __init__(self) -> None:
        super().__init__()

        self.setVisible(False)
        self.setAlignment(Qt.AlignCenter)

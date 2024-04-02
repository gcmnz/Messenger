from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt, QTimer

from .textfield import EnterMessageTextField
from .button import SendMessageButton, MessageButton


class MessagesWidget(QWidget):
    def __init__(self, backend):
        super().__init__()

        # Создание виджета, который будет содержать содержимое QScrollArea
        self.__scroll_content = QWidget()
        self.__scroll_layout = QVBoxLayout(self.__scroll_content)
        self.__scroll_layout.setSpacing(0)  # Установка минимального пространства между виджетами
        self.__scroll_layout.setAlignment(Qt.AlignBottom)  # Выравнивание кнопок по правому краю

        self.enter_message_textfield = EnterMessageTextField('Write a message...')
        self.__send_message_button = SendMessageButton('Отправить', backend.send_message_button_func)

        # Создание QScrollArea
        self.__scroll_area = QScrollArea()
        self.__scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.__scroll_area.setWidgetResizable(True)  # Разрешить изменение размера содержимого QScrollArea
        self.__scroll_area.setWidget(self.__scroll_content)

        self.enter_message_layout = QHBoxLayout()
        self.enter_message_layout.addWidget(self.enter_message_textfield)
        self.enter_message_layout.addWidget(self.__send_message_button)

        # Создание внешнего виджета, который будет содержать QScrollArea
        self.__scroll_area_container_layout = QVBoxLayout()
        self.__scroll_area_container_layout.addWidget(self.__scroll_area)
        self.__scroll_area_container_layout.addLayout(self.enter_message_layout)

        # Установка внешнего виджета в качестве layout для MessagesWidget
        self.setLayout(self.__scroll_area_container_layout)

    def set_messages(self, messages, is_sender_: bool):
        self.__clear_scroll_layout()

        for message in messages:
            is_sender, text, date_, time_ = message

            button = MessageButton(text)
            if int(is_sender) == int(is_sender_):
                alignment = Qt.AlignRight
            else:
                alignment = Qt.AlignLeft

            self.__scroll_layout.addWidget(button, alignment=alignment)

        self.__scroll_to_bottom()

    def __scroll_to_bottom(self):
        scroll_bar = self.__scroll_area.verticalScrollBar()
        QTimer.singleShot(20, lambda: scroll_bar.setValue(scroll_bar.maximum()))

    def message_sended(self, message: str):
        self.enter_message_textfield.setText('')
        self.__scroll_layout.addWidget(MessageButton(message), alignment=Qt.AlignRight)
        self.__scroll_to_bottom()

    def __clear_scroll_layout(self):
        while self.__scroll_layout.count():
            child = self.__scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    # def resizeEvent(self, a0):
    #     layout = self.__scroll_layout
    #     message_count = layout.count()
    #     for i in range(message_count):
    #         item = layout.itemAt(i)
    #         if item.widget():  # Проверка, что элемент макета является виджетом
    #             message_button = item.widget()
    #             font_metrics = message_button.fontMetrics()
    #             message_button_width = font_metrics.boundingRect(message_button.text()).width()
    #             layout_width = self.__scroll_area.size().width()
    #
    #             if message_button_width > layout_width:
    #                 strings_count = message_button_width // layout_width + 1
    #                 message_button.line_break(strings_count)

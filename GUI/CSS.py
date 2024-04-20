
# FONT_STYLE = """<font style='
#         color: rgba(210, 210, 210, 255);
#         font-weight: 611;
#         font-family: Comic Sans MS;
#         font-size: 22px;'>"""

WINDOW_STYLE = """
    MainWindow {
        background-color: rgba(36, 47, 61, 255);
    }
"""

AUTHORIZATION_STYLE = """
    AuthorizationTextField {
        max-width: 200px;
        min-width: 200px;

        min-height: 40px;
        padding: 0px 5px 0px 5px;
        background-color: rgb(27, 39, 52);
        border-radius: 15px;
        font-size: 14px;
        font-weight: 400;
        color: rgba(255, 255, 255, 160);
    }

    AuthorizationTextField::hover {
        background-color: rgb(43, 82, 120);
    }

    AuthorizationButton {
       background-color: rgb(27, 39, 52);
       max-width: 150px;
       min-height: 35px;
       margin: 0px 0px 0px 25px;
       border-radius: 17px;
       font-size: 15px;
       font-weight: 400;
       color: rgba(255, 255, 255, 160);
    }

    AuthorizationButton::hover {
       background-color: rgb(43, 82, 120);
    }

    AuthorizationButton::pressed {
        background-color: lightcoral;
    }
"""

MESSAGING_STYLE = """
    ListInterlocutor {
        background-color: rgb(27, 39, 52);
        font-size: 16px;
        font-weight: 611;
        border: 2px;
    }
    
    ListInterlocutor::item {
        padding: 10px;
        background-color: rgb(27, 39, 52);
        color: white;
    }
    
    ListInterlocutor::item:hover {
        background-color: rgb(33, 55, 80);
    }

    ListInterlocutor::item:selected {
        background-color: rgb(43, 82, 120);
    }
    
    EnterMessageTextField {
        margin: 0px;
        min-height: 25px;
        border-radius: 5px;
        font-size: 13px;
        background-color: rgb(27, 39, 52);
        color: white;
    }
    
    EnterMessageTextField:hover {
        background-color: rgb(27, 39, 52);
    }
    
    SendMessageButton {
        min-height: 25px;
        min-width: 90px;
        margin: 0px;
        border-radius: 6px;
        background-color: rgb(27, 39, 52);
        font-size: 13px;
        color: rgba(255, 255, 255, 180);
    }
    
    SendMessageButton:hover {
        background-color: rgb(27, 39, 52);
    }
    
    SendMessageButton:pressed {
    
    }
    
    MessagesWidget {
        background-color: rgb(27, 39, 52);
    }
    
    MessageButton:hover {
    
    }
    
    SearchUserTextField {
        margin: 0px;
        padding: 0px 5px 0px 5px;
        min-height: 25px;
        font-size: 13px;
        background-color: rgb(27, 39, 52);
        color: rgba(255, 255, 255, 180);
        border-radius: 0px;
    }
    
    SearchUserTextField:hover {
        background-color: rgb(33, 55, 80);
    }
    
    QSplitter::handle {
        background: rgba(255, 255, 255, 0);
        margin: 10px 0px;
    }
    
    QSplitter::handle:hover {
        background: rgba(255, 255, 255, 255);
    }
    
    QSplitter::handle:pressed {
        background: rgba(255, 255, 255, 25);
    }
    
    QScrollBar:vertical {
        width: 15px;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
        background: transparent;
    }
"""

MESSAGING_STYLEs = """
    ListMessages::item {
        padding:  10px;
        border-bottom:  1px solid #ccc;
    }

    ListMessages::item:selected {
        background: lightblue;
        color: white;
    }
    
    ListInterlocutor::item {
        padding:  10px;
        border-bottom:  1px solid #ccc;
    }

    ListInterlocutor::item:selected {
        background: lightblue;
        color: white;
    }
    
"""

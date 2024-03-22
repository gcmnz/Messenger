
WINDOW_STYLE = """

"""

AUTHORIZATION_STYLE = """
    AuthorizationTextField {
        max-width: 200px;
        min-width: 200px;

        min-height: 35px;

        background-color: rgba(112,  43,  229,  255);
        border-radius: 15px;
    }


    AuthorizationTextField::hover {
        background-color: rgba(112,  43,  229,  100);
    }

    AuthorizationButton {
       background-color: rgba(112, 43, 229, 255);
       max-width: 100px;
       min-height: 30px;
       margin: 0px 0px 0px 50px;
       border-radius: 15px;
    }


    AuthorizationButton::hover {
       background-color: rgba(112, 43, 229, 200);
    }

    AuthorizationButton::pressed {
        background-color: lightcoral;
    }
"""

MESSAGING_STYLE = """
    
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

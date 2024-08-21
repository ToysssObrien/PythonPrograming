import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from car import MainWindow  # Assuming your MainWindow class is in the 'car' module
from mysqlconnector import db, cur

class Login(QDialog):
    def __init__(self):
        super().__init__()

        # Load the UI file
        uic.loadUi('login.ui', self)

        # Find widgets in the UI file using object names
        self.username = self.findChild(QLineEdit, 'username')
        self.password = self.findChild(QLineEdit, 'password')  # Change here
        self.btnLogin = self.findChild(QPushButton, 'btnLogin')

        # Set password edit to show dots for password input
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        # Connect login button signal to a slot (function)
        self.btnLogin.clicked.connect(self.login_attempt)

    def login_attempt(self):
        # Get entered username and password
        username = self.username.text()
        password = self.password.text()

        # Add your authentication logic here (e.g., check against a database)
        # For simplicity, a basic example is provided below
        if username == 'supertoy' and password == '123456':
            # Successful login, open the main window
            self.accept()
        else:
            # Failed login, show an error message (you can customize this part)
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = Login()

    if login_window.exec() == QDialog.accepted:
        # If login was successful, create and show the main window
        main_window = MainWindow()
        main_window.show()

    sys.exit(app.exec())

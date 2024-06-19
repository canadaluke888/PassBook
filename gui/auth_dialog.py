import json
import os

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

from encryption.crypto_manager import CryptoManager


class AuthDialog(QDialog):
    def __init__(self, is_first_time=False, parent=None):
        super(AuthDialog, self).__init__(parent)
        self.is_first_time = self.check_first_time()
        self.crypto_manager = CryptoManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PassBook - Authentication')
        layout = QVBoxLayout()

        self.label = QLabel('Enter Password:' if not self.is_first_time else 'Set New Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.check_password)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def check_first_time(self):
        return not os.path.exists('PassBookPassword/password.json')

    def check_password(self):
        password = self.password_input.text()
        if self.is_first_time:
            self.save_password(password)
            QMessageBox.information(self, 'Success', 'Password set successfully.')
            self.accept()
        else:
            if self.verify_password(password):
                self.accept()
            else:
                QMessageBox.warning(self, 'Error', 'Incorrect password.')

    def save_password(self, password):
        os.makedirs('PassBookPassword', exist_ok=True)
        encrypted_password = self.crypto_manager.encrypt(password)
        password_data = {'password': encrypted_password.decode()}
        with open('PassBookPassword/password.json', 'w') as json_file:
            json.dump(password_data, json_file)

    def verify_password(self, password):
        if self.is_first_time:
            return True

        try:
            with open('PassBookPassword/password.json', 'r') as json_file:
                password_data = json.load(json_file)
                encrypted_password = password_data['password']
                decrypted_password = self.crypto_manager.decrypt(encrypted_password.encode())
                return decrypted_password == password
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            return False


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = AuthDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print("Password accepted")
    else:
        print("Password rejected")

    sys.exit(app.exec())

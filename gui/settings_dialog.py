import json

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox


class SettingsDialog(QDialog):
    def __init__(self, crypto_manager, auth_dialog, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('Settings')
        self.crypto_manager = crypto_manager
        self.auth_dialog = auth_dialog
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.current_password_label = QLabel('Current Password:')
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.new_password_label = QLabel('New Password:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_password_label = QLabel('Confirm New Password:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_password)

        layout.addWidget(self.current_password_label)
        layout.addWidget(self.current_password_input)
        layout.addWidget(self.new_password_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        layout.addWidget(self.save_button)

    def save_password(self):
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()

        if new_password != confirm_password:
            QMessageBox.warning(self, 'Error', 'New passwords do not match.')
            return

            # Verify current password
        if not self.auth_dialog.verify_password(current_password):
            QMessageBox.warning(self, 'Error', 'Current password is incorrect.')
            return

        # Encrypt and save the new password
        encrypted_new_password = self.crypto_manager.encrypt(new_password)
        password_data = {'password': encrypted_new_password.decode()}
        with open('PassBookPassword/password.json', 'w') as json_file:
            json.dump(password_data, json_file)

        QMessageBox.information(self, 'Success', 'Password changed successfully.')
        self.accept()

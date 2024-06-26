import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QDialog, \
    QLabel, QLineEdit, QHBoxLayout, QMessageBox

from gui.add_pass_dialog import AddPasswordDialog
from gui.auth_dialog import AuthDialog
from encryption.crypto_manager import CryptoManager
from gui.settings_dialog import SettingsDialog
from gui.note_dialog import NoteDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('PassBook')
        self.setGeometry(100, 100, 800, 600)
        self.crypto_manager = CryptoManager()
        self.auth_dialog = AuthDialog()
        self.passwords_file = 'PassBookPassword/passwords.json'
        self.current_identifier = None
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main vertical layout
        main_layout = QVBoxLayout(central_widget)

        # Top layout
        top_layout = QHBoxLayout()
        add_button = QPushButton('+')
        add_button.setFixedSize(30, 30)
        add_button.clicked.connect(self.open_add_password_dialog)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search')
        self.search_bar.textChanged.connect(self.search_passwords)

        settings_button = QPushButton('Settings')
        settings_button.clicked.connect(self.open_settings_dialog)

        top_layout.addWidget(add_button)
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(settings_button)
        main_layout.addLayout(top_layout)

        # Main content layout (password list and details)
        content_layout = QHBoxLayout()

        self.password_list = QListWidget()
        self.password_list.itemClicked.connect(self.display_password_details)

        self.detail_layout = QVBoxLayout()
        self.detail_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.details_widget = QWidget()
        self.details_widget.setLayout(self.detail_layout)

        content_layout.addWidget(self.password_list, 2)
        content_layout.addWidget(self.details_widget, 3)
        main_layout.addLayout(content_layout)

        self.load_passwords()

    def load_passwords(self):
        self.password_list.clear()
        if os.path.exists(self.passwords_file):
            with open(self.passwords_file, 'r') as file:
                passwords = json.load(file)
                for identifier, data in passwords.items():
                    item = QListWidgetItem(identifier)
                    item.setData(Qt.ItemDataRole.UserRole, data['password'])
                    item.setData(Qt.ItemDataRole.UserRole + 1, data.get('notes', ''))
                    self.password_list.addItem(item)

    def open_add_password_dialog(self):
        dialog = AddPasswordDialog(self.crypto_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            identifier, password = dialog.get_password_data()
            self.add_password(identifier, password)

    def add_password(self, identifier, password):
        encrypted_password = self.crypto_manager.encrypt(password).decode()
        item = QListWidgetItem(identifier)
        item.setData(Qt.ItemDataRole.UserRole, encrypted_password)
        item.setData(Qt.ItemDataRole.UserRole + 1, '')
        self.password_list.addItem(item)
        self.save_password(identifier, {'password': encrypted_password, 'notes': ''})

    def save_password(self, identifier, data):
        passwords = {}
        if os.path.exists(self.passwords_file):
            with open(self.passwords_file, 'r') as file:
                passwords = json.load(file)
        passwords[identifier] = data
        with open(self.passwords_file, 'w') as file:
            json.dump(passwords, file)

    def search_passwords(self):
        query = self.search_bar.text().lower()
        for index in range(self.password_list.count()):
            item = self.password_list.item(index)
            if query in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def open_settings_dialog(self):
        dialog = SettingsDialog(self.crypto_manager, self.auth_dialog)
        dialog.exec()

    def display_password_details(self, item):
        for i in reversed(range(self.detail_layout.count())):
            self.detail_layout.itemAt(i).widget().setParent(None)

        identifier = item.text()
        encrypted_password = item.data(Qt.ItemDataRole.UserRole)
        notes = item.data(Qt.ItemDataRole.UserRole + 1)

        decrypted_password = self.crypto_manager.decrypt(encrypted_password.encode())

        self.detail_layout.addWidget(QLabel(f"Identifier: {identifier}"))
        self.detail_layout.addWidget(QLabel(f"Password: {decrypted_password}"))

        copy_button = QPushButton('Copy Password')
        copy_button.clicked.connect(lambda: self.copy_password(decrypted_password))
        self.detail_layout.addWidget(copy_button)

        delete_button = QPushButton('Delete Password')
        delete_button.clicked.connect(lambda: self.delete_password(identifier))
        self.detail_layout.addWidget(delete_button)

        edit_button = QPushButton('Edit Password')
        edit_button.clicked.connect(lambda: self.edit_password(identifier, decrypted_password))
        self.detail_layout.addWidget(edit_button)

        notes_label = QLabel("Notes:")
        self.detail_layout.addWidget(notes_label)

        if notes:
            self.detail_layout.addWidget(QLabel(notes))
            edit_note_button = QPushButton('Edit Note')
            edit_note_button.clicked.connect(lambda: self.open_note_dialog(identifier, notes))
            self.detail_layout.addWidget(edit_note_button)
        else:
            add_note_button = QPushButton('Add Note')
            add_note_button.clicked.connect(lambda: self.open_note_dialog(identifier))
            self.detail_layout.addWidget(add_note_button)

        self.current_identifier = identifier

    def open_note_dialog(self, identifier, note=None):
        dialog = NoteDialog(parent=self, note=note)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_note = dialog.get_note()
            self.save_note(identifier, new_note)
            self.update_password_notes(identifier, new_note)
            self.display_password_details(self.password_list.currentItem())

    def save_note(self, identifier, note):
        passwords = {}
        if os.path.exists(self.passwords_file):
            with open(self.passwords_file, 'r') as file:
                passwords = json.load(file)
        if identifier in passwords:
            passwords[identifier]['notes'] = note
            with open(self.passwords_file, 'w') as file:
                json.dump(passwords, file)

    def update_password_notes(self, identifier, note):
        for index in range(self.password_list.count()):
            item = self.password_list.item(index)
            if item.text() == identifier:
                item.setData(Qt.ItemDataRole.UserRole + 1, note)
                break

    def copy_password(self, password):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(password)
        QMessageBox.information(self, 'Success', 'Password copied to clipboard.')

    def delete_password(self, identifier):
        reply = QMessageBox.question(self, 'Delete Password',
                                     f'Are you sure you want to delete the password for {identifier}?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.remove_password_from_storage(identifier)
            self.load_passwords()

    def remove_password_from_storage(self, identifier):
        passwords = {}
        if os.path.exists(self.passwords_file):
            with open(self.passwords_file, 'r') as file:
                passwords = json.load(file)
        passwords.pop(identifier, None)
        with open(self.passwords_file, 'w') as file:
            json.dump(passwords, file)

    def edit_password(self, identifier, old_password):
        dialog = AddPasswordDialog(self.crypto_manager, parent=self, edit=True, identifier=identifier,
                                   password=old_password)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_identifier, new_password = dialog.get_password_data()
            self.remove_password_from_storage(identifier)
            self.add_password(new_identifier, new_password)


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

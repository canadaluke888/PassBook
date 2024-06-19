from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QCheckBox, QSpinBox

class AddPasswordDialog(QDialog):
    def __init__(self, crypto_manager, parent=None, edit=False, identifier=None, password=None):
        super(AddPasswordDialog, self).__init__(parent)
        self.crypto_manager = crypto_manager
        self.edit_mode = edit
        self.identifier = identifier
        self.password = password
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.name_label = QLabel('Name:')
        self.name_input = QLineEdit()
        if self.edit_mode and self.identifier:
            self.name_input.setText(self.identifier)

        self.password_label = QLabel('Password:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        if self.edit_mode and self.password:
            self.password_input.setText(self.password)

        self.generate_button = QPushButton('Generate Password')
        self.generate_button.clicked.connect(self.generate_password)

        self.length_label = QLabel('Password Length:')
        self.length_scroll_input = QSpinBox()
        self.length_scroll_input.setMinimum(12)
        self.length_scroll_input.setMaximum(20)

        self.add_button = QPushButton('Save' if self.edit_mode else 'Add')
        self.add_button.clicked.connect(self.accept)

        self.include_numbers = QCheckBox('Include Numbers')
        self.include_uppercase = QCheckBox('Include Uppercase')
        self.include_special = QCheckBox('Include Special Characters')
        self.encrypt_password = QCheckBox('Encrypt')

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_scroll_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.include_numbers)
        layout.addWidget(self.include_uppercase)
        layout.addWidget(self.include_special)
        layout.addWidget(self.encrypt_password)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        self.setWindowTitle('Edit Password' if self.edit_mode else 'Add Password')

    def generate_password(self):
        import random
        import string

        length = self.length_scroll_input.value()
        characters = string.ascii_lowercase
        if self.include_uppercase.isChecked():
            characters += string.ascii_uppercase
        if self.include_numbers.isChecked():
            characters += string.digits
        if self.include_special.isChecked():
            characters += string.punctuation

        password = ''.join(random.choice(characters) for i in range(length))
        self.password_input.setText(password)

    def get_password_data(self):
        return self.name_input.text(), self.password_input.text()

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPlainTextEdit, QDialogButtonBox


class NoteDialog(QDialog):
    def __init__(self, parent=None, note=None):
        super(NoteDialog, self).__init__(parent)
        self.setWindowTitle('Add Note' if note is None else 'Edit Note')
        self.note = note

        layout = QVBoxLayout()

        self.note_text_edit = QPlainTextEdit()
        if note:
            self.note_text_edit.setPlainText(note)
        layout.addWidget(QLabel('Note:'))
        layout.addWidget(self.note_text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_note(self):
        return self.note_text_edit.toPlainText()

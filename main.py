import sys

from PyQt6.QtWidgets import QApplication

from gui.auth_dialog import AuthDialog
from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    auth_dialog = AuthDialog()
    if auth_dialog.exec() == AuthDialog.DialogCode.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec())


if __name__ == '__main__':
    main()

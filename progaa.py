import sys

from PyQt6.QtWidgets import QApplication, QMessageBox

from db import db
from login_window import LoginWindow


def main() -> None:
    app = QApplication(sys.argv)

    try:
        db.connect()
        db.ensure_schema()
    except Exception as e:
        QMessageBox.critical(None, "Ошибка БД", str(e))
        sys.exit(1)

    login = LoginWindow()
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()



import hashlib

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QMessageBox,
)
from PyQt6.QtCore import Qt

from db import db
from main_window import MainWindow


class LoginWindow(QWidget):
    """Окно входа в систему."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ГостиТут – Вход")
        self.setGeometry(200, 120, 960, 560)

        # Общий стиль
        self.setStyleSheet("""
            QWidget { background-color: #dedede; }
            QLineEdit {
                background: #ffffff;
                border: none;
                border-radius: 18px;
                padding-left: 20px;
                padding-right: 20px;
                height: 48px;
                font-size: 16px;
            }
            QPushButton#loginBtn {
                background: #111111;
                color: #ffffff;
                border-radius: 20px;
                padding: 12px 30px;
                font-size: 18px;
            }
            QPushButton#loginBtn:hover {
                background: #222222;
            }
            QFrame#logoBox {
                background: #7d7d7d;
                border: 2px solid #7d7d7d;
                border-radius: 2px;
            }
            QLabel#logoLabel {
                color: #ffffff;
                font-size: 18px;
                background: transparent;
            }
        """)

        # Логотип в левом верхнем углу
        logo_box = QFrame(self)
        logo_box.setObjectName("logoBox")
        logo_box.setFixedSize(180, 64)
        logo_label = QLabel("ГостиТут", logo_box)
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout = QVBoxLayout(logo_box)
        logo_layout.setContentsMargins(10, 10, 10, 10)
        logo_layout.addWidget(logo_label)

        # Поля логина и пароля
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("логин")
        self.login_input.setFixedWidth(360)
        self.login_input.setFixedHeight(48)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(360)
        self.password_input.setFixedHeight(48)

        # Кнопка входа
        self.btn = QPushButton("Вход")
        self.btn.setObjectName("loginBtn")
        self.btn.setFixedWidth(160)
        self.btn.setFixedHeight(48)
        self.btn.clicked.connect(self.check_login)

        # Колонка по центру
        center_col = QVBoxLayout()
        center_col.setSpacing(20)
        center_col.addWidget(self.login_input, alignment=Qt.AlignmentFlag.AlignCenter)
        center_col.addWidget(self.password_input, alignment=Qt.AlignmentFlag.AlignCenter)
        center_col.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        center_widget = QWidget()
        center_widget.setLayout(center_col)

        # Сетка: логотип слева сверху, форма по центру
        grid = QGridLayout()
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setColumnStretch(0, 1)
        grid.setRowStretch(0, 0)
        grid.setRowStretch(1, 1)
        grid.addWidget(logo_box, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        grid.addWidget(center_widget, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(grid)

    def check_login(self):
        """Проверяем логин и пароль в базе."""
        username = self.login_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        pass_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            row = db.fetchone(
                """
                SELECT id, username, password_hash, first_name, last_name
                FROM admins
                WHERE username=%s AND password_hash=%s
                """,
                (username, pass_hash),
            )

            if not row:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
                return

            self.admin = {
                "id": row[0],
                "username": row[1],
                "first_name": row[3],
                "last_name": row[4],
            }

            self.open_main()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", str(e))

    def open_main(self):
        """Открываем основное окно после входа."""
        self.main = MainWindow(self.admin)
        self.main.show()
        self.close()



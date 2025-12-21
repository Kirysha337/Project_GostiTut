import os

from PyQt6.QtGui import QFont

# Настройки пути к картинке и подключению к БД
MAIN_IMAGE_PATH = "/mnt/data/36c0ac0b-3e9d-4eaf-90fa-9b01e602c097.png"
SIDEBAR_COLOR = os.getenv("SIDEBAR_COLOR", "#6d5e5e")
GOST_DSN = os.getenv("GOST_DSN", "dbname=gostitut user=apple password= host=localhost port=5432")
GOST_KEY_ENV = os.getenv("GOST_KEY", None)  # ключ AES в base64

# Цвета статусов номера
COLOR_FREE = "#cfead0"      # свободен
COLOR_CLEANING = "#fff7b8"  # уборка
COLOR_OCCUPIED = "#f4b3b3"  # занят
COLOR_BOOKED = "#cfcfcf"    # бронь

# Шрифты интерфейса
TITLE_FONT = QFont("Arial", 20)
SECTION_FONT = QFont("Arial", 12)
ROOM_FONT = QFont("Arial", 10)



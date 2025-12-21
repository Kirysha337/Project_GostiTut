import psycopg2

from config import GOST_DSN
from crypto_utils import sha256_hash


class DB:
    def __init__(self, dsn: str = GOST_DSN):
        self.dsn = dsn
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(self.dsn)

    def ensure_schema(self):
        """Создаём нужные таблицы и минимальные данные, если их ещё нет."""
        q = """
        CREATE TABLE IF NOT EXISTS admins (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            created_at TIMESTAMPTZ DEFAULT now()
        );
        CREATE TABLE IF NOT EXISTS room_types (
            id SERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            base_price NUMERIC(10,2) DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS rooms (
            id SERIAL PRIMARY KEY,
            number TEXT UNIQUE NOT NULL,
            type_id INTEGER REFERENCES room_types(id) ON DELETE SET NULL,
            floor INTEGER,
            max_guests INTEGER DEFAULT 2,
            status TEXT NOT NULL DEFAULT 'свободен',
            created_at TIMESTAMPTZ DEFAULT now()
        );
        CREATE TABLE IF NOT EXISTS guests (
            id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            passport_encrypted BYTEA,
            passport_iv BYTEA,
            discount NUMERIC(5,2) DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT now()
        );
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            room_id INTEGER REFERENCES rooms(id) ON DELETE CASCADE,
            guest_id INTEGER REFERENCES guests(id) ON DELETE CASCADE,
            created_by INTEGER REFERENCES admins(id),
            date_from DATE NOT NULL,
            date_to DATE NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            total_price NUMERIC(12,2) DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT now()
        );
        CREATE TABLE IF NOT EXISTS room_status_history (
            id SERIAL PRIMARY KEY,
            room_id INTEGER REFERENCES rooms(id),
            old_status TEXT,
            new_status TEXT,
            changed_by INTEGER REFERENCES admins(id),
            changed_at TIMESTAMPTZ DEFAULT now()
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(q)
            # безопасно добавим недостающий столбец скидки (если база была создана ранее)
            cur.execute("ALTER TABLE guests ADD COLUMN IF NOT EXISTS discount NUMERIC(5,2) DEFAULT 0;")
            # Добавим дефолтного админа, если нет пользователей
            cur.execute("SELECT COUNT(*) FROM admins")
            cnt = cur.fetchone()[0]
            if cnt == 0:
                # дефолтный логин admin/admin (SHA256)
                cur.execute(
                    "INSERT INTO admins(username, password_hash, first_name, last_name) VALUES (%s,%s,%s,%s)",
                    ("admin", sha256_hash("admin"), "Кирилл", "Кириллов")
                )
            # Добавим несколько категорий и номеров, если пусто (для начального макета)
            cur.execute("SELECT COUNT(*) FROM room_types")
            cnt_rt = cur.fetchone()[0]
            if cnt_rt == 0:
                cur.execute(
                    "INSERT INTO room_types(name, description, base_price) VALUES (%s,%s,%s)",
                    ("Стандарт", "Базовая категория", 100)
                )
                cur.execute(
                    "INSERT INTO room_types(name, description, base_price) VALUES (%s,%s,%s)",
                    ("Комфорт+", "С улучшенными условиями", 150)
                )
                cur.execute(
                    "INSERT INTO room_types(name, description, base_price) VALUES (%s,%s,%s)",
                    ("Люкс", "VIP", 250)
                )
            cur.execute("SELECT COUNT(*) FROM rooms")
            cnt_rooms = cur.fetchone()[0]
            if cnt_rooms == 0:
                # добавим примеры
                cur.execute(
                    "INSERT INTO rooms(number, type_id, floor, status) VALUES (%s,%s,%s,%s)",
                    ("2-101", 1, 2, 'свободен')
                )
                cur.execute(
                    "INSERT INTO rooms(number, type_id, floor, status) VALUES (%s,%s,%s,%s)",
                    ("2-102", 1, 2, 'уборка')
                )
                cur.execute(
                    "INSERT INTO rooms(number, type_id, floor, status) VALUES (%s,%s,%s,%s)",
                    ("3-101", 2, 3, 'занят')
                )
                cur.execute(
                    "INSERT INTO rooms(number, type_id, floor, status) VALUES (%s,%s,%s,%s)",
                    ("4-101", 3, 4, 'бронь')
                )
            self.conn.commit()

    def fetchall(self, query, params=()):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    def fetchone(self, query, params=()):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()

    def execute(self, query, params=()):
        with self.conn.cursor() as cur:
            cur.execute(query, params)
        self.conn.commit()


db = DB()



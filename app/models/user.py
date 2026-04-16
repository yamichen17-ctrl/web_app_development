from app.models.db_helper import get_db_connection

class User:
    @staticmethod
    def create(username: str, email: str, password_hash: str):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(u) for u in users]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id: int):
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email: str):
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(user) if user else None
        finally:
            conn.close()

    @staticmethod
    def update(user_id: int, username: str, email: str):
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE users SET username = ?, email = ? WHERE id = ?",
                (username, email, user_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def delete(user_id: int):
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        finally:
            conn.close()

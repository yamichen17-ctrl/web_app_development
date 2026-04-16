from app.models.db_helper import get_db_connection

class Favorite:
    @staticmethod
    def create(user_id: int, restaurant_id: int):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO favorites (user_id, restaurant_id) VALUES (?, ?)",
                (user_id, restaurant_id)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception:
            # 可能是 UNIQUE 限制衝突
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            favorites = conn.execute("SELECT * FROM favorites").fetchall()
            return [dict(f) for f in favorites]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(favorite_id: int):
        conn = get_db_connection()
        try:
            favorite = conn.execute("SELECT * FROM favorites WHERE id = ?", (favorite_id,)).fetchone()
            return dict(favorite) if favorite else None
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id: int):
        conn = get_db_connection()
        try:
            query = """
                SELECT f.id as favorite_id, r.*
                FROM favorites f
                JOIN restaurants r ON f.restaurant_id = r.id
                WHERE f.user_id = ?
                ORDER BY f.created_at DESC
            """
            favorites = conn.execute(query, (user_id,)).fetchall()
            return [dict(f) for f in favorites]
        finally:
            conn.close()

    @staticmethod
    def is_favorite(user_id: int, restaurant_id: int):
        conn = get_db_connection()
        try:
            favorite = conn.execute(
                "SELECT id FROM favorites WHERE user_id = ? AND restaurant_id = ?",
                (user_id, restaurant_id)
            ).fetchone()
            return bool(favorite)
        finally:
            conn.close()

    @staticmethod
    def delete(user_id: int, restaurant_id: int):
        conn = get_db_connection()
        try:
            conn.execute(
                "DELETE FROM favorites WHERE user_id = ? AND restaurant_id = ?", 
                (user_id, restaurant_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

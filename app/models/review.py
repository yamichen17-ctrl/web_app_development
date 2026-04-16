from app.models.db_helper import get_db_connection

class Review:
    @staticmethod
    def create(user_id: int, restaurant_id: int, rating: int, comment: str = None):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reviews (user_id, restaurant_id, rating, comment) VALUES (?, ?, ?, ?)",
                (user_id, restaurant_id, rating, comment)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            reviews = conn.execute("SELECT * FROM reviews").fetchall()
            return [dict(r) for r in reviews]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(review_id: int):
        conn = get_db_connection()
        try:
            review = conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
            return dict(review) if review else None
        finally:
            conn.close()

    @staticmethod
    def get_by_restaurant(restaurant_id: int):
        conn = get_db_connection()
        try:
            # JOIN with users to get the username
            query = """
                SELECT r.*, u.username 
                FROM reviews r
                JOIN users u ON r.user_id = u.id
                WHERE r.restaurant_id = ?
                ORDER BY r.created_at DESC
            """
            reviews = conn.execute(query, (restaurant_id,)).fetchall()
            return [dict(r) for r in reviews]
        finally:
            conn.close()

    @staticmethod
    def update(review_id: int, rating: int, comment: str = None):
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE reviews SET rating = ?, comment = ? WHERE id = ?",
                (rating, comment, review_id)
            )
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def delete(review_id: int):
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
            conn.commit()
            return True
        finally:
            conn.close()

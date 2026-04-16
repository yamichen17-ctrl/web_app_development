from app.models.db_helper import get_db_connection

class Restaurant:
    @staticmethod
    def create(name: str, description: str = None, category: str = None, price_range: str = None, distance: int = None, image_url: str = None):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO restaurants (name, description, category, price_range, distance, image_url)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (name, description, category, price_range, distance, image_url)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            restaurants = conn.execute("SELECT * FROM restaurants").fetchall()
            return [dict(r) for r in restaurants]
        finally:
            conn.close()

    @staticmethod
    def get_by_id(restaurant_id: int):
        conn = get_db_connection()
        try:
            restaurant = conn.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,)).fetchone()
            return dict(restaurant) if restaurant else None
        finally:
            conn.close()

    @staticmethod
    def search(keyword: str):
        conn = get_db_connection()
        try:
            query = "%" + keyword + "%"
            restaurants = conn.execute(
                "SELECT * FROM restaurants WHERE name LIKE ? OR category LIKE ?", 
                (query, query)
            ).fetchall()
            return [dict(r) for r in restaurants]
        finally:
            conn.close()

    @staticmethod
    def update(restaurant_id: int, **kwargs):
        conn = get_db_connection()
        try:
            if not kwargs:
                return False
            
            columns = ", ".join(f"{k} = ?" for k in kwargs.keys())
            values = list(kwargs.values())
            values.append(restaurant_id)
            
            conn.execute(f"UPDATE restaurants SET {columns} WHERE id = ?", values)
            conn.commit()
            return True
        finally:
            conn.close()

    @staticmethod
    def delete(restaurant_id: int):
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM restaurants WHERE id = ?", (restaurant_id,))
            conn.commit()
            return True
        finally:
            conn.close()

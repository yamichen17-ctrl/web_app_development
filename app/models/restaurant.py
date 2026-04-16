from app.models.db_helper import get_db_connection

class Restaurant:
    @staticmethod
    def create(name: str, description: str = None, category: str = None, price_range: str = None, distance: int = None, image_url: str = None):
        """
        新增一筆餐廳記錄。
        參數:
            name: 餐廳名稱
            ...其他欄位
        回傳:
            成功回傳 id，失敗回傳 None。
        """
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
        except Exception as e:
            print(f"Error creating restaurant: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有餐廳記錄。
        回傳:
            所有餐廳的字典名單。
        """
        conn = get_db_connection()
        try:
            restaurants = conn.execute("SELECT * FROM restaurants").fetchall()
            return [dict(r) for r in restaurants]
        except Exception as e:
            print(f"Error getting all restaurants: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(restaurant_id: int):
        """
        取得單筆餐廳記錄。
        參數:
            restaurant_id: 餐廳 ID。
        回傳:
            餐廳字典資料，找不到回傳 None。
        """
        conn = get_db_connection()
        try:
            restaurant = conn.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,)).fetchone()
            return dict(restaurant) if restaurant else None
        except Exception as e:
            print(f"Error getting restaurant by id {restaurant_id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def search(keyword: str):
        """
        根據關鍵字搜尋名稱或分類。
        參數:
            keyword: 搜尋關鍵字。
        回傳:
            符合的餐廳字典名單。
        """
        conn = get_db_connection()
        try:
            query = "%" + keyword + "%"
            restaurants = conn.execute(
                "SELECT * FROM restaurants WHERE name LIKE ? OR category LIKE ?", 
                (query, query)
            ).fetchall()
            return [dict(r) for r in restaurants]
        except Exception as e:
            print(f"Error searching restaurants: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(restaurant_id: int, **kwargs):
        """
        更新記錄。
        參數:
            restaurant_id: 餐廳 ID
            **kwargs: 想要更新的欄位與值
        回傳:
            成功 True，失敗 False。
        """
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
        except Exception as e:
            print(f"Error updating restaurant: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(restaurant_id: int):
        """
        刪除餐廳。
        參數:
            restaurant_id: 餐廳 ID。
        回傳:
            成功 True，失敗 False。
        """
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM restaurants WHERE id = ?", (restaurant_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting restaurant: {e}")
            return False
        finally:
            conn.close()

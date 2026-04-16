from app.models.db_helper import get_db_connection

class Favorite:
    @staticmethod
    def create(user_id: int, restaurant_id: int):
        """
        加入一筆收藏。
        參數:
            user_id: 使用者 ID
            restaurant_id: 餐廳 ID
        回傳:
            成功回傳 id，若已存在或其他錯誤回傳 None
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO favorites (user_id, restaurant_id) VALUES (?, ?)",
                (user_id, restaurant_id)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Favorite creation error (possibly unique constraint): {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有記錄。
        回傳: 字典陣列
        """
        conn = get_db_connection()
        try:
            favorites = conn.execute("SELECT * FROM favorites").fetchall()
            return [dict(f) for f in favorites]
        except Exception as e:
            print(f"Error getting all favorites: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(favorite_id: int):
        """
        取得單筆記錄。
        參數: favorite_id
        回傳: 字典或 None
        """
        conn = get_db_connection()
        try:
            favorite = conn.execute("SELECT * FROM favorites WHERE id = ?", (favorite_id,)).fetchone()
            return dict(favorite) if favorite else None
        except Exception as e:
            print(f"Error getting favorite by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_user(user_id: int):
        """
        取得某位特定使用者收藏的餐廳清單。
        參數: user_id
        回傳: 包含餐廳資訊的字典陣列。
        """
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
        except Exception as e:
            print(f"Error getting user favorites: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def is_favorite(user_id: int, restaurant_id: int):
        """
        判斷是否已收藏。
        回傳: boolean
        """
        conn = get_db_connection()
        try:
            favorite = conn.execute(
                "SELECT id FROM favorites WHERE user_id = ? AND restaurant_id = ?",
                (user_id, restaurant_id)
            ).fetchone()
            return bool(favorite)
        except Exception as e:
            print(f"Error checking if is favorite: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id: int, restaurant_id: int):
        """
        刪除記錄。
        參數:
            user_id: 使用者 ID
            restaurant_id: 餐廳 ID
        回傳: boolean
        """
        conn = get_db_connection()
        try:
            conn.execute(
                "DELETE FROM favorites WHERE user_id = ? AND restaurant_id = ?", 
                (user_id, restaurant_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting favorite: {e}")
            return False
        finally:
            conn.close()

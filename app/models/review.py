from app.models.db_helper import get_db_connection

class Review:
    @staticmethod
    def create(user_id: int, restaurant_id: int, rating: int, comment: str = None):
        """
        新增一筆評論記錄。
        參數:
            user_id: 發布者 ID
            restaurant_id: 餐廳 ID
            rating: 星數
            comment: 評論內容
        回傳:
            新增的 review id，失敗則 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reviews (user_id, restaurant_id, rating, comment) VALUES (?, ?, ?, ?)",
                (user_id, restaurant_id, rating, comment)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating review: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有記錄。
        回傳: 字典陣列。
        """
        conn = get_db_connection()
        try:
            reviews = conn.execute("SELECT * FROM reviews").fetchall()
            return [dict(r) for r in reviews]
        except Exception as e:
            print(f"Error getting all reviews: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(review_id: int):
        """
        取得單筆記錄。
        參數: review_id
        回傳: 字典資料或 None
        """
        conn = get_db_connection()
        try:
            review = conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()
            return dict(review) if review else None
        except Exception as e:
            print(f"Error getting review by id: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_restaurant(restaurant_id: int):
        """
        取得某餐廳所有的紀錄，並包含使用者名稱。
        參數: restaurant_id
        回傳: 字典陣列
        """
        conn = get_db_connection()
        try:
            query = """
                SELECT r.*, u.username 
                FROM reviews r
                JOIN users u ON r.user_id = u.id
                WHERE r.restaurant_id = ?
                ORDER BY r.created_at DESC
            """
            reviews = conn.execute(query, (restaurant_id,)).fetchall()
            return [dict(r) for r in reviews]
        except Exception as e:
            print(f"Error getting reviews for restaurant: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update(review_id: int, rating: int, comment: str = None):
        """
        更新記錄。
        參數:
            review_id: 評論 ID
            rating: 星數
            comment: 內容
        回傳: 成功 True 失敗 False
        """
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE reviews SET rating = ?, comment = ? WHERE id = ?",
                (rating, comment, review_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating review: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(review_id: int):
        """
        刪除記錄。
        參數: review_id
        回傳: boolean
        """
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting review: {e}")
            return False
        finally:
            conn.close()

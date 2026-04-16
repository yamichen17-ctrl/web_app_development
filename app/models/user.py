from app.models.db_helper import get_db_connection

class User:
    @staticmethod
    def create(username: str, email: str, password_hash: str):
        """
        新增一名使用者記錄。
        參數:
            username: 使用者名稱
            email: 使用者信箱
            password_hash: 加密後的密碼
        回傳:
            成功回傳新增的 user id，失敗回傳 None。
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """
        取得所有使用者記錄。
        回傳:
            包含所有使用者資料的字典陣列。
        """
        conn = get_db_connection()
        try:
            users = conn.execute("SELECT * FROM users").fetchall()
            return [dict(u) for u in users]
        except Exception as e:
            print(f"Error getting all users: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id: int):
        """
        根據 ID 取得單一使用者記錄。
        參數:
            user_id: 使用者 ID
        回傳:
            使用者字典資料或 None (若找不到)。
        """
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id {user_id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_email(email: str):
        """
        根據 email 取得單一使用者記錄。
        參數:
            email: 使用者信箱
        回傳:
            使用者字典資料或 None (若找不到)。
        """
        conn = get_db_connection()
        try:
            user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by email {email}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(user_id: int, username: str, email: str):
        """
        更新指定的記錄。
        參數:
            user_id: 使用者 ID
            username: 新的使用者名稱
            email: 新的信箱
        回傳:
            成功回傳 True，失敗回傳 False。
        """
        conn = get_db_connection()
        try:
            conn.execute(
                "UPDATE users SET username = ?, email = ? WHERE id = ?",
                (username, email, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating user {user_id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id: int):
        """
        刪除一筆使用者記錄。
        參數:
            user_id: 使用者 ID
        回傳:
            成功回傳 True，失敗回傳 False。
        """
        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting user {user_id}: {e}")
            return False
        finally:
            conn.close()

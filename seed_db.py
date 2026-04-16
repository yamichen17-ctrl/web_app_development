import sqlite3

db_path = r"c:\Users\User\Desktop\web_app_development\instance\database.db"
conn = sqlite3.connect(db_path)
# 檢查是否已經有資料
if conn.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0] == 0:
    conn.execute("INSERT INTO restaurants (name, description, category, price_range, distance, image_url) VALUES ('美味食堂', '好吃又便宜的學餐', '便當', '$', 2, '')")
    conn.commit()
conn.close()
print("DB Seeded.")

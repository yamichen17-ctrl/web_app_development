# 路由設計文件 (ROUTES)

本文件基於 PRD、系統架構以及資料庫設計，規劃出所有 Flask 路由、HTTP 方法以及對應之 Jinja2 模板，做為前後端頁面與邏輯開發的基礎。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (導向清單) | GET | `/` | — | 直接重導向至 `/restaurants` (預設顯示所有餐廳) |
| 會員註冊頁面 | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| 會員註冊邏輯 | POST | `/auth/register` | — | 接收帳號密碼、寫入 DB、重導向至登入頁面 |
| 會員登入頁面 | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| 會員登入邏輯 | POST | `/auth/login` | — | 驗證帳號密碼、建立 Session、重導向至由哪裡來的頁面或首頁 |
| 會員登出 | POST/GET | `/auth/logout` | — | 清除 Session，重導向至首頁 |
| 餐廳列表 | GET | `/restaurants/` | `templates/restaurant/list.html` | 查詢所有餐廳並顯示列表 (可帶條件參數) |
| 搜尋餐廳 | GET | `/restaurants/search`| `templates/restaurant/list.html` | 使用 `?q=關鍵字` 篩選餐廳，複用 list.html |
| 餐廳詳細資訊 | GET | `/restaurants/<int:id>`| `templates/restaurant/detail.html` | 根據 id 查詢特定餐廳與所屬 Review 紀錄 |
| 新增評論邏輯 | POST | `/restaurants/<int:id>/reviews` | — | 接收表單內容、存入 DB 的 Review、完成後重導向回餐廳詳情頁 |
| 切換收藏狀態 | POST | `/restaurants/<int:id>/favorite`| — | 若無收藏則加入、若已收藏則移除，完成後重導向回原畫面 |
| 個人收藏清單 | GET | `/favorites/` | `templates/user/favorites.html` | 查詢當前 Session user_id 的所有收藏餐廳並顯示 |


## 2. 每個路由的詳細說明

### 2.1. Auth 模組 (`/auth/...`)
- **GET `/auth/register`**
  - **輸入**：無
  - **處理邏輯**：單純回傳註冊頁面。
  - **輸出**：渲染 `auth/register.html`。
- **POST `/auth/register`**
  - **輸入**：表單欄位 `username`, `email`, `password`。
  - **處理邏輯**：檢查 `email` 是否重複。若無重複則加密密碼，呼叫 `User.create(...)`。
  - **輸出**：重導向至 `/auth/login`。
  - **錯誤處理**：資料缺漏或 email 重複時，閃爍提示 (Flash) 並重新渲染註冊表。
- **GET `/auth/login`**
  - **輸入**：無
  - **處理邏輯**：回傳登入頁面。
  - **輸出**：渲染 `auth/login.html`。
- **POST `/auth/login`**
  - **輸入**：表單欄位 `email`, `password`。
  - **處理邏輯**：尋找 `User.get_by_email`，比對密碼。正確則將 `user_id` 存入 `session`。
  - **輸出**：登入成功重導向至首頁。
  - **錯誤處理**：帳號或密碼錯誤時，Flash 錯誤並重新渲染登入表單。
- **GET/POST `/auth/logout`**
  - **處理邏輯**：執行 `session.clear()`。
  - **輸出**：重導向至首頁。

### 2.2. Restaurant 模組 (`/restaurants/...`)
- **GET `/restaurants/`**
  - **輸入**：無
  - **處理邏輯**：呼叫 `Restaurant.get_all()`。
  - **輸出**：將資料送進 `restaurant/list.html` 渲染。
- **GET `/restaurants/search`**
  - **輸入**：URL 變數 `?q=關鍵字`。
  - **處理邏輯**：取得搜尋變數，傳遞至 `Restaurant.search(keyword)` 獲取結果。
  - **輸出**：渲染 `restaurant/list.html`。
- **GET `/restaurants/<int:id>`**
  - **輸入**：URL path parameter `id`。
  - **處理邏輯**：呼叫 `Restaurant.get_by_id(id)`，並呼叫 `Review.get_by_restaurant(id)`、檢查當前登入者 `Favorite.is_favorite(...)` 狀態。
  - **輸出**：渲染 `restaurant/detail.html`。
  - **錯誤處理**：如果找不到餐廳 ID，回傳 404 Not Found。
- **POST `/restaurants/<int:id>/reviews`**
  - **輸入**：表單欄位 `rating`, `comment`，並從 `session` 取出 `user_id`。
  - **處理邏輯**：驗證有無登入。若已備妥，呼叫 `Review.create(...)` 插入資料。
  - **輸出**：成功後重導向至 `/restaurants/<id>`。

### 2.3. Favorite 模組 (`/favorites/...` / 切換 API)
- **POST `/restaurants/<int:id>/favorite`**
  - **輸入**：從 `session` 取出 `user_id`，及 `restaurant_id`。
  - **處理邏輯**：判斷 `Favorite.is_favorite`。如果已收藏，則呼叫 `delete` 移除；反之呼叫 `create`。
  - **輸出**：重導向回先前的頁面。
- **GET `/favorites/`**
  - **輸入**：從 `session` 取 `user_id`。
  - **處理邏輯**：未登入則導向登入頁面。已登入則呼叫 `Favorite.get_by_user(user_id)` 取得收藏列表。
  - **輸出**：渲染 `user/favorites.html`。


## 3. Jinja2 模板清單

所有的模板都會放在專案的 `app/templates/` 之下，並盡可能共用相同的 base:

1. `base.html` - 網站的主板型，包含全域導覽列 (Navbar)、頁腳 (Footer)、以及 Flash 訊息區塊。所有其他頁面都將使用 `{% extends "base.html" %}` 進行繼承。
2. `auth/register.html` - 註冊表單，繼承 base.html。
3. `auth/login.html` - 登入表單，繼承 base.html。
4. `restaurant/list.html` - 首頁與搜尋共用的餐廳清單網格畫面，繼承 base.html。
5. `restaurant/detail.html` - 點進餐廳後的排版，包含照片、詳細資訊、星星、評論列表與「我要留言」表單區塊，繼承 base.html。
6. `user/favorites.html` - 專屬使用者的收藏餐廳列表，排版可與 `list.html` 類似，繼承 base.html。

## 4. 路由骨架程式碼

基於 Blueprint 設計，已在 `app/routes/` 中建立四個核心檔案的程式碼骨架：
- `app/routes/main.py`
- `app/routes/auth.py`
- `app/routes/restaurants.py`
- `app/routes/favorites.py` 
包含裝飾器與函數簽章，供後續實作。

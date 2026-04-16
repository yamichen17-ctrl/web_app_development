from flask import Blueprint, request, session, redirect, url_for, render_template, flash

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/', methods=['GET'])
def list_restaurants():
    """
    GET: 查詢所有餐廳並帶入 list.html 進行渲染
    """
    pass

@restaurants_bp.route('/search', methods=['GET'])
def search_restaurants():
    """
    GET: 取得 ?q= 參數，查詢符合名稱或類型的餐廳，重新渲染 list.html
    """
    pass

@restaurants_bp.route('/<int:id>', methods=['GET'])
def restaurant_detail(id):
    """
    GET: 根據 id 查詢特定餐廳詳情、評論清單，並確認目前使用者的收藏狀態。渲染 detail.html。
    """
    pass

@restaurants_bp.route('/<int:id>/reviews', methods=['POST'])
def add_review(id):
    """
    POST: 驗證使用者登入狀態，接收評價的 rating 與 comment，寫回資料庫後重導向至餐廳詳細頁面。
    """
    pass

@restaurants_bp.route('/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """
    POST: 驗證使用者登入狀態，切換該名使用者對此餐廳的收藏狀態，完成後返回原畫面。
    """
    pass

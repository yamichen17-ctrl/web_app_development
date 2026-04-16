from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from app.models.restaurant import Restaurant
from app.models.review import Review
from app.models.favorite import Favorite

restaurants_bp = Blueprint('restaurants', __name__, url_prefix='/restaurants')

@restaurants_bp.route('/', methods=['GET'])
def list_restaurants():
    """
    GET: 查詢所有餐廳並帶入 list.html 進行渲染
    """
    restaurants = Restaurant.get_all()
    return render_template('restaurant/list.html', restaurants=restaurants)

@restaurants_bp.route('/search', methods=['GET'])
def search_restaurants():
    """
    GET: 取得 ?q= 參數，查詢符合名稱或類型的餐廳，重新渲染 list.html
    """
    keyword = request.args.get('q', '').strip()
    if keyword:
        restaurants = Restaurant.search(keyword)
    else:
        restaurants = Restaurant.get_all()
        
    return render_template('restaurant/list.html', restaurants=restaurants, search_query=keyword)

@restaurants_bp.route('/<int:id>', methods=['GET'])
def restaurant_detail(id):
    """
    GET: 根據 id 查詢特定餐廳詳情、評論清單，並確認目前使用者的收藏狀態。渲染 detail.html。
    """
    restaurant = Restaurant.get_by_id(id)
    if not restaurant:
        flash('找不到該餐廳。', 'danger')
        return redirect(url_for('restaurants.list_restaurants'))

    reviews = Review.get_by_restaurant(id)
    
    is_favorite = False
    if 'user_id' in session:
        is_favorite = Favorite.is_favorite(session['user_id'], id)

    return render_template(
        'restaurant/detail.html', 
        restaurant=restaurant, 
        reviews=reviews, 
        is_favorite=is_favorite
    )

@restaurants_bp.route('/<int:id>/reviews', methods=['POST'])
def add_review(id):
    """
    POST: 驗證使用者登入狀態，接收評價的 rating 與 comment，寫回資料庫後重導向至餐廳詳細頁面。
    """
    if 'user_id' not in session:
        flash('請先登入後才能發表評論。', 'warning')
        return redirect(url_for('auth.login'))

    rating = request.form.get('rating')
    comment = request.form.get('comment', '').strip()

    if not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
        flash('請提供正確的 1~5 評分星數。', 'danger')
        return redirect(url_for('restaurants.restaurant_detail', id=id))

    success = Review.create(
        user_id=session['user_id'],
        restaurant_id=id,
        rating=int(rating),
        comment=comment
    )

    if success:
        flash('評論已成功發佈！', 'success')
    else:
        flash('發佈評論時發生錯誤，請稍後再試。', 'danger')

    return redirect(url_for('restaurants.restaurant_detail', id=id))

@restaurants_bp.route('/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    """
    POST: 驗證使用者登入狀態，切換該名使用者對此餐廳的收藏狀態，完成後返回原畫面。
    """
    if 'user_id' not in session:
        flash('請先登入後才能收藏餐廳。', 'warning')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    if Favorite.is_favorite(user_id, id):
        Favorite.delete(user_id, id)
        flash('已將此餐廳從收藏清單移除。', 'info')
    else:
        Favorite.create(user_id, id)
        flash('已將此餐廳加入收藏！', 'success')
        
    return redirect(url_for('restaurants.restaurant_detail', id=id))

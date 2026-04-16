from flask import Blueprint, session, redirect, url_for, render_template, flash
from app.models.favorite import Favorite

favorites_bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@favorites_bp.route('/', methods=['GET'])
def list_favorites():
    """
    GET: 驗證使用者已登入，查詢該使用者收藏的所有餐廳，渲染 favorites.html。
    """
    if 'user_id' not in session:
        flash('請先登入以檢視您的收藏清單。', 'warning')
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    favorites_list = Favorite.get_by_user(user_id)
    
    return render_template('user/favorites.html', favorites=favorites_list)

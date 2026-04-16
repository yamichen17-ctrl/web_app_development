from flask import Blueprint, request, session, redirect, url_for, render_template, flash

favorites_bp = Blueprint('favorites', __name__, url_prefix='/favorites')

@favorites_bp.route('/', methods=['GET'])
def list_favorites():
    """
    GET: 驗證使用者已登入，查詢該使用者收藏的所有餐廳，渲染 favorites.html。
    """
    pass

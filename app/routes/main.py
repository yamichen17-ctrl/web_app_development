from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    GET: 首頁，直接重導向至餐廳清單。
    """
    pass

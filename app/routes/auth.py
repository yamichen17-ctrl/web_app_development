from flask import Blueprint, request, session, redirect, url_for, render_template, flash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單
    POST: 接收註冊資料(username, email, password)，寫入資料庫並導向登入頁面
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單
    POST: 驗證帳號密碼，成功則設定 session 並導向首頁
    """
    pass

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    清除 session，導向首頁
    """
    pass

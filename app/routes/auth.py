from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    GET: 顯示註冊表單
    POST: 接收註冊資料(username, email, password)，寫入資料庫並導向登入頁面
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('所有欄位都是必填的。', 'danger')
            return render_template('auth/register.html')

        user = User.get_by_email(email)
        if user:
            flash('該 Email 已經被註冊過！', 'warning')
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        User.create(username, email, password_hash)
        
        flash('註冊成功，請登入！', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 顯示登入表單
    POST: 驗證帳號密碼，成功則設定 session 並導向首頁
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('請輸入 Email 與密碼。', 'danger')
            return render_template('auth/login.html')

        user = User.get_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('登入失敗：Email 或密碼錯誤。', 'danger')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    清除 session，導向首頁
    """
    session.clear()
    flash('您已成功登出。', 'info')
    return redirect(url_for('main.index'))

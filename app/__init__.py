import os
import sqlite3
from flask import Flask
from config import Config

def create_app(config_class=Config):
    # 建立與初始化 Flask 應用程式
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # 確保 instance 目錄存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫腳本
    def init_db():
        db_path = app.config['DATABASE_PATH']
        schema_path = os.path.join(os.path.dirname(app.instance_path), 'database', 'schema.sql')
        if not os.path.exists(db_path) and os.path.exists(schema_path):
            with sqlite3.connect(db_path) as conn:
                with open(schema_path, 'r', encoding='utf-8') as f:
                    conn.executescript(f.read())

    # 在應用程式初始化時啟動初始化
    with app.app_context():
        init_db()

    # 註冊 Blueprints 路由
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.restaurants import restaurants_bp
    from app.routes.favorites import favorites_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(favorites_bp)

    return app

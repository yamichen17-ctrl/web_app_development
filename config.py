import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    # 使用 instance 資料夾來存放 database 檔案
    DATABASE_PATH = os.path.join(basedir, 'instance', 'database.db')

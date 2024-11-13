import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

class Config:
    # Flask-Mail 配置
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # 从环境变量获取
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # 从环境变量获取
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY') or os.urandom(24)
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY') or os.urandom(24)
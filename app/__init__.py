# -*- coding:utf-8 -*-
"""
@author liuning
@date 2019/6/16 14:03
@File __init__.py.py 
@Desciption
"""
import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
from flask_session import Session
from flask_cors import CORS
import os

db = SQLAlchemy() #表示数据库
migrate = Migrate() #数据库迁移引擎
se = Session()
# login.login_message = ('Please log in to access this page.')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    #插件关联
    db.init_app(app)
    migrate.init_app(app, db)
    se.init_app(app)
    CORS(app)
    #注册蓝图
    from app.api import bp as api_bp
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.manage import bp as manage_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(manage_bp,url_prefix='/manage')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp,url_prefix='/api')
    if not app.debug:
        # ...
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/end.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('end startup')

    return app
from app import models
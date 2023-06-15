import os

from flask import Flask

from datetime import timedelta

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
#from flask_mail import Mail
from dotenv import load_dotenv
load_dotenv() # 仕様上、.envファイルは__init__.pyと同階層におく

import sys
sys.path.append(os.path.join('..'))



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_url_path='/static', instance_relative_config=True)
   
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY'),
        #SECRET_KEY='dev',
        DATABASE=os.environ.get('DATABASE_URL')
        #DATABASE=os.environ.get('postgres://inoueyuya:127.0.0.1:5000/flaskr')
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # セッションの有効期限設定
    app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

    # アップロードファイルの最大サイズの制限(100MB未満だけ許可)
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

    # mailの設定
    """app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')"""

    csrf.init_app(app)

    # database
    from . import db
    db.init_app(app)

    # auth
    from . import auth
    app.register_blueprint(auth.bp)

    # upload
    from . import upload
    app.register_blueprint(upload.bp)
    app.add_url_rule('/', endpoint='index')
    return app

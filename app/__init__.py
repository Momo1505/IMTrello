from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
login_manager.login_view = 'authentication.login_page'


from app.models import *
with app.test_request_context():
    db.create_all()

from app.main import main as main_blueprint

app.register_blueprint(main_blueprint, url_prefix='/')

from app.authentification import authentication as authentication_blueprint

app.register_blueprint(authentication_blueprint, url_prefix='/auth')

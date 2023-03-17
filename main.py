import os

from flask import Flask

from config import getconn
from controllers.post_controllers import post_controller
from controllers.user_controllers import user_controller
from models.models import db

app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(post_controller)
app.app_context().push()

if os.getenv("ENV") == "DEVELOPMENT":
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['DEBUG'] = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": getconn
    }
    app.config['DEBUG'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('app_secret')
db.init_app(app)

db.create_all()

if __name__ == "__main__":
    app.run(port=8080)

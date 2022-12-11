import os
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import getconn

# print("Has context in", __name__, flask.has_app_context())
app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
print("Has context in", __name__, flask.has_app_context())
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
from controllers.user_controllers import *

# from controllers.articles_controllers import *
if __name__ == "__main__":
    with app.app_context():
        app.run(port=8080)

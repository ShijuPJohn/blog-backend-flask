import os

from flask import Flask

from config import getconn
from controllers.user_controllers import user_controllers
from models.models import db

app = Flask(__name_
app.register_blueprint(user_controllers)
app.app_context().push()

if os.getenv("ENV") == "DEVELOPMENT":
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "creator": getconn
    }
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']=os.getenv('app_secret')
db.init_app(app)

db.create_all()

if __name__ == "__main__":
    app.run(port=8080, debug=True if os.environ["ENV"] == "DEVELOPMENT" else False)

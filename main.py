import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import getconn

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()
from controllers.user_controllers import *
# from controllers.articles_controllers import *
if __name__ == "__main__":
    app.run(debug=True if os.environ.get("ENV") == "DEVELOPMENT" else False, port=int(os.environ.get("PORT", 8080)))

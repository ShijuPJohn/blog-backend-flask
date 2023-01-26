import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import getconn

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

from controllers.user_controllers import *
db.create_all()
if __name__ == "__main__":
    app.run(port=8080, debug=True if os.environ["ENV"] == "DEVELOPMENT" else False)

import os

from flask import Flask

from config import getconn
from controllers.user_controllers import user_controllers
from models.models import db

app = Flask(__name__)
app.register_blueprint(user_controllers)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "creator": getconn
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

db.create_all()
if __name__ == "__main__":
    app.run(port=8080, debug=True if os.environ["ENV"] == "DEVELOPMENT" else False)

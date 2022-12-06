import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes

app = Flask(__name__)
client = secretmanager.SecretManagerServiceClient()
db_pass_res = "projects/468486424470/secrets/dbps/versions/1"
db_user_res = "projects/468486424470/secrets/db-user/versions/1"
db_dbname_res = "projects/468486424470/secrets/db-name/versions/1"
db_connection_name_res = "projects/468486424470/secrets/db-connection-name/versions/1"
db_password = client.access_secret_version(request={"name": db_pass_res}).payload.data.decode("UTF-8")
db_user = client.access_secret_version(request={"name": db_user_res}).payload.data.decode("UTF-8")
db_name = client.access_secret_version(request={"name": db_dbname_res}).payload.data.decode("UTF-8")
db_connection_name = client.access_secret_version(request={"name": db_connection_name_res}).payload.data.decode("UTF-8")

#
# def getconn():
#     with Connector() as connector:
#         conn = connector.connect(
#             db_connection_name,
#             "pg8000",
#             user=db_user,
#             password=db_password,
#             db=db_name,
#             ip_type=IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
#         )
#         return conn
#
#
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     "creator": getconn
# }
#
# db = SQLAlchemy(app)
# db.init_app(app)
# app.app_context().push()
#
#
# class Student(db.Model):
#     __tablename__ = "student"
#     student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     roll_number = db.Column(db.String, unique=True, nullable=False)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String)
#
#     def __str__(self):
#         return str(self.student_id) + "id and name : " + self.first_name
#
#
# db.create_all()


@app.route("/")
def hello_world():
    return "Hello World"


# @app.route("/create")
# def student_create_get():
#     student = Student(roll_number="123A", first_name="SHIJU", last_name="JOHN")
#     db.session.add(student)
#     db.session.commit()
#     return str(student)
#
#
# @app.route("/fetch")
# def students_fetch_get():
#     students = Student.query.all()
#     return str(students[0])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

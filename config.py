from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes


client = secretmanager.SecretManagerServiceClient()
db_pass_res = "projects/468486424470/secrets/dbps/versions/1"
db_user_res = "projects/468486424470/secrets/db-user/versions/1"
db_dbname_res = "projects/468486424470/secrets/db-name/versions/1"
db_connection_name_res = "projects/468486424470/secrets/db-connection-name/versions/1"
db_password = client.access_secret_version(request={"name": db_pass_res}).payload.data.decode("UTF-8")
db_user = client.access_secret_version(request={"name": db_user_res}).payload.data.decode("UTF-8")
db_name = client.access_secret_version(request={"name": db_dbname_res}).payload.data.decode("UTF-8")
db_connection_name = client.access_secret_version(request={"name": db_connection_name_res}).payload.data.decode("UTF-8")


def getconn():
    with Connector() as connector:
        conn = connector.connect(
            db_connection_name,
            "pg8000",
            user=db_user,
            password=db_password,
            db=db_name,
            ip_type=IPTypes.PUBLIC  # IPTypes.PRIVATE for private IP
        )
        return conn


# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+pg8000://"
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#     "creator": getconn
# }
#
# db = SQLAlchemy(app)
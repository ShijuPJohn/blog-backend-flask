import os

from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes

if os.environ["ENV"] == "PRODUCTION":
    client = secretmanager.SecretManagerServiceClient()
    db_pass_res = "projects/1037996227658/secrets/db_pass/versions/1"
    db_user_res = "projects/1037996227658/secrets/db_user/versions/1"
    db_dbname_res = "projects/1037996227658/secrets/db_dbname/versions/2"
    db_connection_name_res = "projects/1037996227658/secrets/db_connection_name/versions/1"
    app_secret_res = "projects/1037996227658/secrets/app_secret_value/versions/1"
    db_password = client.access_secret_version(request={"name": db_pass_res}).payload.data.decode("UTF-8")
    db_user = client.access_secret_version(request={"name": db_user_res}).payload.data.decode("UTF-8")
    db_name = client.access_secret_version(request={"name": db_dbname_res}).payload.data.decode("UTF-8")
    app_secret = client.access_secret_version(request={"name": app_secret_res}).payload.data.decode("UTF-8")
    db_connection_name = client.access_secret_version(request={"name": db_connection_name_res}).payload.data.decode(
        "UTF-8")
else:
    db_password = os.environ["db_pass"]
    db_user = os.environ["db_user"]
    db_name = os.environ["db_dbname"]
    db_connection_name = os.environ["db_connection_name"]


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


def get_secret():
    return app_secret

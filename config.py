import os

from google.cloud import secretmanager
from google.cloud.sql.connector import Connector, IPTypes


if os.environ["ENV"] == "PRODUCTION":
    client = secretmanager.SecretManagerServiceClient()
    blog_secrets_res = "projects/1037996227658/secrets/blog_secrets/versions/3"
    secrets_string = client.access_secret_version(request={"name": blog_secrets_res}).payload.data.decode("UTF-8")
    secrets_array = secrets_string.split()
    app_secret = secrets_string[0]
    db_user = secrets_string[4]
    db_name = secrets_string[2]
    db_connection_name = secrets_string[1]
    db_password = secrets_string[3]
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

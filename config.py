import os
import urllib.parse as up

import psycopg2
from google.cloud import secretmanager

secret_key = None
if os.environ["ENV"] == "PRODUCTION":
    client = secretmanager.SecretManagerServiceClient()
    secrets_res = "projects/1037996227658/secrets/blog_secrets/versions/4"
    secrets = client.access_secret_version(request={"name": secrets_res}).payload.data.decode("UTF-8")
    secrets_list = secrets.split()
    url = secrets_list[0]
    secret_key = secrets_list[1]
else:
    url = up.urlparse(os.environ["ELE_DATABASE_URL"])
    secret_key = os.environ['app_secret']


def getconn():
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database=url.path[1:],
                            user=url.username,
                            password=url.password,
                            host=url.hostname,
                            port=url.port
                            )
    return conn


def get_secret():
    # return app_secret
    pass

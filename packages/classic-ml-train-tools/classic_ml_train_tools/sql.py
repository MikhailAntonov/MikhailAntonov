import os
import prestodb
import pandas as pd
from typing import Optional
from sqlalchemy.engine import create_engine
from prestodb.auth import BasicAuthentication
from google.cloud import bigquery

protocol: str = "https"
catalog = "hive"


def get_engine():
    host = os.environ["PRESTO_URI"]
    port = os.environ["PRESTO_PORT"]
    secret = get_username_secret(os.environ["PRESTO_SECRET_NAME"])

    conn_string = f"presto://{secret.username}:{secret.password}@{host}:{port}/{catalog}"
    conn_args = {"protocol": f"{protocol}"}
    engine = create_engine(conn_string, connect_args=conn_args, echo=False)
    return engine


def get_connection():
    host = os.environ["PRESTO_URI"]
    port = os.environ["PRESTO_PORT"]
    secret = get_username_secret(os.environ["PRESTO_SECRET_NAME"])

    auth = BasicAuthentication(secret.username, secret.password)
    conn = prestodb.dbapi.connect(
        host=host, port=port, http_scheme=protocol, auth=auth, catalog=catalog
    )
    return conn


def download_query_with_retry(query: str, max_retry: int) -> pd.DataFrame:
    cur_repeat = 0
    while cur_repeat <= max_retry:
        try:
            with get_connection() as conn:
                cur = conn.cursor()
                cur.execute(query)
                rows = cur.fetchall()

                col_names = [i[0] for i in cur.description]
                df = pd.DataFrame(rows, columns=col_names)

                # These calls are not necessary according to GIT PRESTO.DBAPI documentation
                cur.close()
                # This call is needed to supress following warning in unittests:
                # ResourceWarning: unclosed <socket.socket fd=13, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM
                conn._http_session.close()
                conn.close()
                # These calls are not necessary according to GIT PRESTO.DBAPI documentation

                return df
        except Exception as e:
            cur_repeat += 1
            if cur_repeat > max_retry:
                raise e
    return None



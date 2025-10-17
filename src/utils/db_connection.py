# utils/db_connection.py

from sqlalchemy import create_engine
import psycopg2
from config import DB_CONFIG

def get_sqlalchemy_engine():
    """
    Cria e retorna uma engine SQLAlchemy para uso com GeoPandas ou pandas.

    Retorna:
        sqlalchemy.engine.base.Engine: engine conectada ao banco PostgreSQL/PostGIS.
    """
    try:
        url = (
            f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        engine = create_engine(url)
        return engine
    except Exception as e:
        print(f"Erro ao criar engine SQLAlchemy: {e}")
        return None


def get_psycopg2_connection():
    """
    Cria e retorna uma conexão direta com o banco usando psycopg2.

    Retorna:
        psycopg2.extensions.connection: conexão ativa com o banco.
    """
    try:
        conn = psycopg2.connect(
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"]
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar com psycopg2: {e}")
        return None

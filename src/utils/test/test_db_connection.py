import psycopg2
from psycopg2 import OperationalError


def test_db_connection():
    try:
        conn = psycopg2.connect(
            dbname="car",
            user="postgres",
            password="123456",
            host="localhost",
            port="5432"
        )
        print("✅ Conexão bem-sucedida!")
        conn.close()
    except OperationalError as e:
        print("❌ Falha na conexão:")
        print(e)


if __name__ == "__main__":
    test_db_connection()

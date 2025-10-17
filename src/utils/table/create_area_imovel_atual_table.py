import psycopg2

# Configurações de conexão (substitua conforme necessário)
DB_CONFIG = {
    "user": "postgres",
    "password": "123456",
    "host": "localhost",
    "port": "5432",
    "database": "car"
}

# Conecta ao banco de dados
conn = psycopg2.connect(
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    host=DB_CONFIG["host"],
    port=DB_CONFIG["port"],
    database=DB_CONFIG["database"]
)

cursor = conn.cursor()

# Cria a tabela com os tipos corretos
create_table_sql = """
CREATE TABLE IF NOT EXISTS area_imovel_atual (
    cod_tema      TEXT,
    nom_tema      TEXT,
    cod_imovel    TEXT PRIMARY KEY,
    mod_fiscal    DOUBLE PRECISION,
    num_area      DOUBLE PRECISION,
    ind_status    TEXT,
    ind_tipo      TEXT,
    des_condic    TEXT,
    municipio     TEXT,
    cod_estado    TEXT,
    dat_criaca    DATE,
    dat_atuali    DATE,
    geometry      geometry(POLYGON, 4674)
);
"""

cursor.execute(create_table_sql)
conn.commit()
cursor.close()
conn.close()

print("Tabela 'area_imovel_atual' criada com sucesso no banco de dados.")

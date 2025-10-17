import geopandas as gpd
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from config import DB_CONFIG, TARGET_TABLE, HISTORY_TABLE

def get_engine():
    """
    Cria e retorna uma engine SQLAlchemy para uso com GeoPandas ou pandas.
    """
    url = (
        f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url)

def ensure_crs(gdf, epsg=4326):
    """
    Garante que o GeoDataFrame tenha o CRS correto definido.
    Se já houver CRS diferente, sobrescreve sem transformar.
    """
    if gdf.crs is None or gdf.crs.to_epsg() != epsg:
        gdf = gdf.set_crs(epsg=epsg, allow_override=True)
    return gdf

def apply_updates(changes_gdf, change_type):
    """
    Aplica atualizações na tabela principal e registra no histórico.
    Parâmetros:
        changes_gdf (GeoDataFrame): registros a serem inseridos, modificados ou excluídos.
        change_type (str): tipo da alteração ('inclusao', 'modificacao', 'exclusao')
    """
    engine = get_engine()
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for _, row in changes_gdf.iterrows():
        cod_imovel = row['cod_imovel']

        # Cria um GeoDataFrame com a linha atual e garante o CRS
        gdf_row = gpd.GeoDataFrame([row], geometry='geometry')
        gdf_row = ensure_crs(gdf_row, epsg=4326)

        # Renomeia a coluna geométrica para 'geom' conforme esperado pela tabela
        gdf_row = gdf_row.rename_geometry('geom')

        # Converte datas com verificação de nulos
        dat_criaca_raw = row['dat_criaca']
        dat_atuali_raw = row['dat_atuali']

        dat_criaca = pd.to_datetime(dat_criaca_raw, dayfirst=True) if pd.notnull(dat_criaca_raw) else None
        dat_atuali = pd.to_datetime(dat_atuali_raw, dayfirst=True) if pd.notnull(dat_atuali_raw) else None

        dat_criaca = dat_criaca.date() if dat_criaca is not None else None
        dat_atuali = dat_atuali.date() if dat_atuali is not None else None

        # Atualiza os campos no GeoDataFrame
        gdf_row.loc[:, 'dat_criaca'] = dat_criaca
        gdf_row.loc[:, 'dat_atuali'] = dat_atuali

        if change_type == 'inclusao':
            cursor.execute(f"SELECT 1 FROM {TARGET_TABLE} WHERE cod_imovel = %s", (cod_imovel,))
            exists = cursor.fetchone()
            if not exists:
                gdf_row.to_postgis(TARGET_TABLE, engine, if_exists='append', index=False)

        elif change_type == 'modificacao':
            cursor.execute(f"DELETE FROM {TARGET_TABLE} WHERE cod_imovel = %s", (cod_imovel,))
            conn.commit()
            gdf_row.to_postgis(TARGET_TABLE, engine, if_exists='append', index=False)

        elif change_type == 'exclusao':
            cursor.execute(f"DELETE FROM {TARGET_TABLE} WHERE cod_imovel = %s", (cod_imovel,))
            conn.commit()

        # Registra no histórico
        historico_sql = f"""
        INSERT INTO {HISTORY_TABLE} (
            cod_tema, nom_tema, cod_imovel, mod_fiscal, num_area,
            ind_status, ind_tipo, des_condic, municipio, cod_estado,
            dat_criaca, dat_atuali, tipo_alteracao, data_modificacao,
            geom
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_DATE, ST_SetSRID(ST_GeomFromText(%s), 4326))
        """
        cursor.execute(historico_sql, (
            row['cod_tema'], row['nom_tema'], row['cod_imovel'], row['mod_fiscal'], row['num_area'],
            row['ind_status'], row['ind_tipo'], row['des_condic'], row['municipio'], row['cod_estado'],
            dat_criaca, dat_atuali, change_type, row['geometry'].wkt
        ))
        conn.commit()

    cursor.close()
    conn.close()
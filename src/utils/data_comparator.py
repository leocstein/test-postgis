import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPolygon, Polygon
from sqlalchemy import text
from utils.db_connection import get_sqlalchemy_engine
from config import TARGET_TABLE


def load_current_data():
    """
    Carrega os dados atuais da tabela definida em TARGET_TABLE no banco PostgreSQL/PostGIS.
    Retorna:
        GeoDataFrame contendo os registros espaciais atuais do banco.
    """
    engine = get_sqlalchemy_engine()
    if engine is None:
        raise ConnectionError("Não foi possível conectar ao banco de dados.")

    query = f"SELECT * FROM {TARGET_TABLE};"
    current_gdf = gpd.read_postgis(text(query), con=engine, geom_col='geom')
    return current_gdf


def filter_new_records():
    return


def compare_datasets():
    return


def concat_dataframe(old_gdf, new_gdf):
    gdf_combined = pd.concat([old_gdf, new_gdf], ignore_index=True)
    return gdf_combined


def duplicates_rows_dataframe(gdf_combined):
    duplicates = gdf_combined[gdf_combined.duplicated(
        'cod_imovel', keep=False)]

    if not duplicates.empty:
        print(duplicates)
    else:
        print("Não possui valores duplicados!")

    # Exibir resultado
    for cod, group in duplicates.groupby('cod_imovel'):
        if group.nunique().eq(1).all():
            print(f"Os registros duplicados para {cod} são idênticos.")
        else:
            print(f"Diferenças encontradas para {cod}:")
            for column in group.columns:
                unique_vals = group[column].unique()
                if len(unique_vals) > 1:
                    print(
                        f" - Coluna '{column}': valores diferentes -> {unique_vals}")
            print()

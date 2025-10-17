# main.py

from utils.file_handler import list_zip_files, extract_shapefile, read_shapefile
from utils.set_multipolygon import set_multipolygon
from utils.set_datetime_dataframe import set_datetime_dataframe
from utils.data_comparator import concat_dataframe, duplicates_rows_dataframe
import os

# Etapa 1: Listar arquivos .zip válidos
zip_files = list_zip_files()
if not zip_files:
    print("Nenhum arquivo .zip encontrado.")
    exit()

# Etapa 2: Extrair e ler shapefile do primeiro estado
zip_path = zip_files[0]
state = os.path.basename(os.path.dirname(zip_path))
extracted_dir = extract_shapefile(zip_path, state)

old_gdf = read_shapefile(extracted_dir)

if old_gdf is None:
    print("Falha ao ler shapefile.")
    exit()

# Extrair e ler shapefile do segundo estado
zip_path = zip_files[1]
state = os.path.basename(os.path.dirname(zip_path))
extracted_dir = extract_shapefile(zip_path, state)

new_gdf = read_shapefile(extracted_dir)

if new_gdf is None:
    print("Falha ao ler shapefile.")
    exit()

# Etapa 3: Garantir que todas as geometrias do GeoDataFrame sejam do tipo MultiPolygon
old_gdf = set_multipolygon(old_gdf)
new_gdf = set_multipolygon(new_gdf)

# Etapa 4: Garantir que todas as datas do GeoDataFrame estejam do padrão "%y-%m-%d"
old_gdf = set_datetime_dataframe(old_gdf)
new_gdf = set_datetime_dataframe(new_gdf)

# Testes
print(f"GeoDataFrame::OLD:: \n {old_gdf}")
print(f"GeoDataFrame::NEW:: \n {new_gdf}")

gdf_combined = concat_dataframe(old_gdf, new_gdf)
print(f"GeoDataFrame::CONCAT:: \n {gdf_combined}")

duplicates = duplicates_rows_dataframe(gdf_combined)

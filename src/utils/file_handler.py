# utils/file_handler.py

import os
import zipfile
import geopandas as gpd
from config import DATA_DIR, TEMP_DIR
from utils.state import State


def list_zip_files():
    """
    Lista todos os arquivos .zip de shapefiles na estrutura de estados válidos.

    Retorna:
        List[str]: caminhos completos dos arquivos .zip encontrados.
    """
    zip_files = []
    for state in State:
        state_path = os.path.join(DATA_DIR, state.value)
        if os.path.isdir(state_path):
            for file in os.listdir(state_path):
                if file.endswith("AREA_IMOVEL.zip"):
                    zip_files.append(os.path.join(state_path, file))
    print(f"Lista de arquivos ZIP: \n {zip_files}")
    return zip_files


def extract_shapefile(zip_path, state):
    """
    Extrai o conteúdo de um arquivo .zip para a pasta temporária do estado.

    Args:
        zip_path (str): caminho do arquivo .zip.
        state (str): sigla do estado (ex: 'AC').

    Retorna:
        str: caminho da pasta onde os arquivos foram extraídos.
    """
    destination = os.path.join(TEMP_DIR, state)
    os.makedirs(destination, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination)

    return destination


def read_shapefile(directory):
    """
    Lê o shapefile extraído usando GeoPandas.

    Args:
        directory (str): caminho da pasta onde o shapefile foi extraído.

    Retorna:
        GeoDataFrame ou None: dados lidos ou None se falhar.
    """
    try:
        for file in os.listdir(directory):
            if file.endswith(".shp"):
                path_shp = os.path.join(directory, file)
                return gpd.read_file(path_shp)
    except Exception as e:
        print(f"Erro ao ler shapefile em {directory}: {e}")
    return None

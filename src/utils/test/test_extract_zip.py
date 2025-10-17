import zipfile
import os

# Caminho completo do arquivo ZIP
zip_path = "data/AC/AC_AREA_IMOVEL.zip"

# Verifica se o arquivo existe
if not os.path.isfile(zip_path):
    print(f"❌ Arquivo não encontrado: {zip_path}")
    exit(1)

# Nome da pasta de destino (sem extensão .zip)
folder_name = os.path.splitext(os.path.basename(zip_path))[0]
extract_to = os.path.join(os.path.dirname(zip_path), folder_name)

# Cria a pasta se não existir
os.makedirs(extract_to, exist_ok=True)

# Extrai o conteúdo
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)
    print(f"✅ Arquivo extraído para: {extract_to}")

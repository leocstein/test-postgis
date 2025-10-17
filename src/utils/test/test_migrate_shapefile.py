import subprocess
import os


def migrar_shapefile():
    # Caminho do shapefile
    shape_dir = "data/AC/AC_AREA_IMOVEL"
    shape_file = "AREA_IMOVEL_1.shp"
    shape_path = os.path.join(shape_dir, shape_file)

    # Dados do banco
    db_name = "car"
    db_user = "postgres"
    db_pass = "123456"
    db_host = "localhost"
    db_port = "5432"
    table_name = "area_imovel_atual"

    # Comando ogr2ogr
    cmd = [
        "ogr2ogr",
        "-f", "PostgreSQL",
        f"PG:host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_pass}",
        shape_path,
        "-nln", table_name,
        "-nlt", "PROMOTE_TO_MULTI",
        "-lco", "GEOMETRY_NAME=geom",
        "-lco", "FID=gid",
        "-overwrite",
        "-fieldTypeToString", "Real"
    ]

    try:
        print("🔄 Iniciando migração do shapefile...")
        subprocess.run(cmd, check=True)
        print(
            f"✅ Migração concluída para a tabela '{table_name}' no banco '{db_name}'")
    except subprocess.CalledProcessError as e:
        print("❌ Erro ao executar ogr2ogr:")
        print(e)


if __name__ == "__main__":
    migrar_shapefile()

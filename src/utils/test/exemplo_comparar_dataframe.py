import geopandas as gpd
import pandas as pd

# Exemplo fictício de dois GeoDataFrames
gdf_old = gpd.GeoDataFrame({
    'id': [1, 2, 3],
    'name': ['A', 'B', 'C'],
    'geometry': [gpd.points_from_xy([0], [0])[0],
                 gpd.points_from_xy([1], [1])[0],
                 gpd.points_from_xy([2], [2])[0]]
})

gdf_new = gpd.GeoDataFrame({
    'id': [2, 3, 4],
    'name': ['B', 'C_updated', 'D'],
    'geometry': [gpd.points_from_xy([1], [1])[0],
                 gpd.points_from_xy([2.1], [2.1])[0],  # ligeiramente diferente
                 gpd.points_from_xy([3], [3])[0]]
})

# Comparar por ID
merged = gdf_old.merge(gdf_new, on='id', how='outer',
                       suffixes=('_old', '_new'), indicator=True)

merged['geometry_changed'] = ~merged.apply(
    lambda row: row['geometry_old'].equals(
        row['geometry_new']) if row['_merge'] == 'both' else True,
    axis=1
)

# Mostrar registros novos, removidos e alterados
new_records = merged[merged['_merge'] == 'right_only']
removed_records = merged[merged['_merge'] == 'left_only']
changed_geometry = merged[(merged['_merge'] == 'both')
                          & (merged['geometry_changed'])]


print("Todos registros:")
print(merged)

print("Novos registros:")
print(new_records)

print("\nRegistros removidos:")
print(removed_records)

print("\nGeometrias alteradas:")
print(changed_geometry)

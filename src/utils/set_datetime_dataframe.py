import pandas as pd


def set_datetime_dataframe(gdf):
    gdf['dat_criaca'] = pd.to_datetime(
        gdf['dat_criaca'], dayfirst=True, errors='coerce')

    gdf['dat_atuali'] = pd.to_datetime(
        gdf['dat_atuali'], dayfirst=True, errors='coerce')

    return gdf

from shapely.geometry import MultiPolygon, Polygon


def set_multipolygon(gdf):
    """
    Garante que todas as geometrias do GeoDataFrame sejam do tipo MultiPolygon.
    """
    def convert(geom):
        if isinstance(geom, Polygon):
            return MultiPolygon([geom])
        return geom

    gdf['geometry'] = gdf['geometry'].apply(convert)
    return gdf

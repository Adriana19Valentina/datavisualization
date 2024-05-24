import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

atms_df = pd.read_csv('final_final_data.csv')
atms_df['geometry'] = atms_df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
atms_gdf = gpd.GeoDataFrame(atms_df, geometry='geometry', crs="EPSG:4326")
counties_gdf = gpd.read_file('ro_judete_poligon.shp')
atms_gdf = atms_gdf.to_crs(counties_gdf.crs)
atms_with_counties = gpd.sjoin(atms_gdf, counties_gdf, how="left", predicate='within', lsuffix='_atm', rsuffix='_county')
atms_with_counties = atms_with_counties.rename(columns={'name': 'county'})
result_df = atms_with_counties[['name_left', 'vicinity', 'latitude', 'longitude', 'county']]
result_df.to_csv('atms_with_counties.csv', index=False)

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

df = pd.read_csv("atms_romania.csv")

headers = df[df["name"] == "name"].index
df_cleaned = df.drop(headers)
df_cleaned = df_cleaned.drop_duplicates()

df = df_cleaned

df["geometry"] = df.apply(lambda row: Point(row["longitude"], row["latitude"]), axis=1)
geo_df = gpd.GeoDataFrame(df, geometry="geometry")

# Set the initial CRS for geo_df to WGS 84
geo_df.set_crs(epsg=4326, inplace=True)

# Assuming you have a shapefile for Romania's boundaries
romania = gpd.read_file("ro_frontiera_poligon.shp")


if geo_df.crs != romania.crs:
    print("here i am")
    geo_df = geo_df.to_crs(romania.crs)

# Perform spatial join to filter out only points within Romania
data_within_romania = gpd.sjoin(geo_df, romania, how="inner", op="within")

# Optionally, drop the geometry column if it's no longer needed
data_within_romania = data_within_romania.drop(columns=["geometry"])

# Save the cleaned, deduplicated, and spatially filtered data to a new CSV file
data_within_romania.to_csv("data_within_romania_3.csv", index=False)

# Print the first few rows of the final dataset to verify
print(data_within_romania.head())

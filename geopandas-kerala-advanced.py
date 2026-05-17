import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------
# Load and Reproject Shapefiles (UTM Zone 43N for Kerala)
# -------------------------------
districts = gpd.read_file(r"E:\Python\AGSRT\Data\district\district.shp").to_crs(epsg=32643)
roads = gpd.read_file(r"Data\kerala_highway\kerala_highway.shp").to_crs(epsg=32643)

# -------------------------------
# Explode Example (no visible change here, since all are POLYGONs)
# -------------------------------
districts_exploded = districts.explode(index_parts=True)
districts_exploded.plot(color="lightblue", edgecolor="black")
plt.title("Exploded districts (no change, all POLYGONs)")
plt.savefig("linkdn/exploded_districts.png", dpi=300, bbox_inches="tight")
plt.show()

# -------------------------------
# Clip Example: Roads clipped to Ernakulam
# -------------------------------
ernakulam = districts[districts['DISTRICT'] == 'Ernakulam']
road_clip = gpd.clip(roads, ernakulam)
ax = ernakulam.plot(color="lightblue", edgecolor="black")
road_clip.plot(ax=ax, color="red")
plt.title("Roads clipped to Ernakulam")
plt.savefig("linkdn/roads_clipped_ernakulam.png", dpi=300, bbox_inches="tight")
plt.show()

# -------------------------------
# Simplify Example
# -------------------------------
districts_simplified = districts.simplify(tolerance=1000)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
districts.plot(ax=ax1, color="lightblue", edgecolor="black")
ax1.set_title("Original boundaries")
districts_simplified.plot(ax=ax2, color="orange", edgecolor="black")
ax2.set_title("Simplified boundaries")
plt.savefig("linkdn/simplified_vs_original.png", dpi=300, bbox_inches="tight")
plt.show()

# -------------------------------
# Centroid Example with Labels
# -------------------------------
districts['centroid'] = districts.geometry.centroid
ax = districts.plot(color='lightgreen', edgecolor='black')
districts['centroid'].plot(ax=ax, color='red', markersize=6)
for idx, row in districts.iterrows():
    plt.text(row['centroid'].x, row['centroid'].y,
             row['DISTRICT'], fontsize=7, ha='center')
plt.title('District centroids with Labels')
plt.savefig("linkdn/district_centroids.png", dpi=300, bbox_inches="tight")
plt.show()

# -------------------------------
# Spatial Index Example
# -------------------------------
sindex = roads.sindex
ernakulam = districts[districts['DISTRICT'] == 'Ernakulam']
possible_matches_index = list(sindex.intersection(ernakulam.total_bounds))
possible_matches = roads.iloc[possible_matches_index]
roads_in_ernakulam = possible_matches[possible_matches.intersects(ernakulam.union_all())]
ax = ernakulam.plot(color="lightblue", edgecolor="black", figsize=(8, 8))
roads.plot(ax=ax, color="green")
roads_in_ernakulam.plot(ax=ax, color="red", linewidth=2)
plt.title("Roads intersecting Ernakulam district (Spatial Index)")
plt.savefig("linkdn/roads_spatial_index.png", dpi=300, bbox_inches="tight")
plt.show()

# -------------------------------
# Choropleth Mapping with Dummy Data
# -------------------------------
#Merging the dummy data with District data
data = pd.read_csv(r'Data/kerala_dummy_data.csv')
districts = districts.merge(data, on="DISTRICT")

print(districts.columns)

# Population Choropleth
ax = districts.plot(column="POPULATION", cmap="OrRd", legend=True, figsize=(10, 8))
plt.title("Kerala Districts by Population (Dummy Data)")
plt.savefig("linkdn/population_map.png", dpi=300, bbox_inches="tight")
plt.show()

# Literacy Choropleth
ax = districts.plot(column="LITERACY", cmap="Greens", legend=True, figsize=(10, 8))
plt.title("Kerala Districts by Literacy Rate (Dummy Data)")
plt.savefig("linkdn/literacy_map.png", dpi=300, bbox_inches="tight")
plt.show()

# Rainfall Choropleth
ax = districts.plot(column="RAINFALL", cmap="Blues", legend=True, figsize=(10, 8))
plt.title("Kerala Districts by Rainfall (Dummy Data)")
plt.savefig("linkdn/rainfall_map.png", dpi=300, bbox_inches="tight")
plt.show()

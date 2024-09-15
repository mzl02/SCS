import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import shape

# Load the South China Sea shapefile
shapefile_path = "/Users/zachlawrence/Documents/SCS/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"
world = gpd.read_file(shapefile_path)

# Define the South China Sea region boundary
bounds = {
    'minx': 100,
    'maxx': 130,
    'miny': -10,
    'maxy': 25
}

# Crop the world map to focus on South China Sea region
world_cropped = world.cx[bounds['minx']:bounds['maxx'], bounds['miny']:bounds['maxy']]

# Load the sample shipping lane data from JSON
shipping_lanes_json = '''{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "name": "Lane 1 - Singapore to Hong Kong",
        "traffic_density": "High",
        "type": "Major"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [104.0, 1.0],
          [106.5, 4.0],
          [109.0, 7.0],
          [115.0, 10.0],
          [121.0, 14.0],
          [122.0, 15.0],
          [114.0, 22.5]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Lane 2 - Shanghai to Singapore",
        "traffic_density": "High",
        "type": "Major"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [121.5, 31.0],
          [118.0, 29.0],
          [113.0, 23.0],
          [108.0, 12.0],
          [104.0, 1.0]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Lane 3 - Manila to Jakarta",
        "traffic_density": "Medium",
        "type": "Regional"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [121.0, 14.6],
          [115.0, 8.0],
          [110.0, 5.5],
          [106.8, -6.0]
        ]
      }
    },
    {
      "type": "Feature",
      "properties": {
        "name": "Lane 4 - Hong Kong to Taipei",
        "traffic_density": "Medium",
        "type": "Regional"
      },
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [114.0, 22.5],
          [116.0, 21.0],
          [119.0, 19.0],
          [121.5, 25.0]
        ]
      }
    }
  ]
}'''
# Convert JSON to a GeoDataFrame
shipping_lanes_data = json.loads(shipping_lanes_json)
features = shipping_lanes_data['features']
geometries = [shape(feature['geometry']) for feature in features]
shipping_lanes_gdf = gpd.GeoDataFrame(features, geometry=geometries)

# Plot the map and overlay shipping lanes
fig, ax = plt.subplots(figsize=(10, 8))
world_cropped.plot(ax=ax, color='lightgray', edgecolor='black')

# Plot shipping lanes on top of the map
shipping_lanes_gdf.plot(ax=ax, color='blue', linewidth=2)

# Add labels for shipping lanes
for _, lane in shipping_lanes_gdf.iterrows():
    centroid = lane.geometry.centroid
    ax.annotate(lane['properties']['name'], xy=(centroid.x, centroid.y), fontsize=8, ha='center', color='blue')

# Set the plot limits to zoom into the South China Sea area
ax.set_xlim(bounds['minx'], bounds['maxx'])
ax.set_ylim(bounds['miny'], bounds['maxy'])

# Add title
ax.set_title('South China Sea with Shipping Lanes', fontsize=15)

# Show the plot
plt.show()

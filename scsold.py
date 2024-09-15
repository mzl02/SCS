import geopandas as gpd
import matplotlib.pyplot as plt

# Update this path to point to the location of your shapefile
shapefile_path = "/Users/zachlawrence/Documents/SCS/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"

# Load the shapefile
world = gpd.read_file(shapefile_path)

# Inspect the columns to find the correct one for country names
print(world.columns)  # Check the correct column name for countries

# Define the South China Sea region boundary (latitude and longitude)
bounds = {
    'minx': 100,  # Minimum longitude
    'maxx': 130,  # Maximum longitude
    'miny': -10,  # Minimum latitude
    'maxy': 25    # Maximum latitude
}

# Crop the world data to the specified bounds
world_cropped = world.cx[bounds['minx']:bounds['maxx'], bounds['miny']:bounds['maxy']]

# Plot the world map, then zoom into the South China Sea region
fig, ax = plt.subplots(figsize=(10, 8))

# Plot only the landmasses within the defined boundaries
world_cropped.plot(ax=ax, color='lightgray', edgecolor='black')

# Set the plot limits to zoom into the South China Sea area
ax.set_xlim(bounds['minx'], bounds['maxx'])
ax.set_ylim(bounds['miny'], bounds['maxy'])

# Add title and labels
ax.set_title('South China Sea and Surrounding Country', fontsize=15)
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Replace 'name' with the correct column for country names (e.g., 'ADMIN' or 'NAME')
for _, country in world_cropped.iterrows():
    # Get the centroid of the country
    centroid = country.geometry.centroid
    # Annotate the country name at its centroid (replace 'ADMIN' with the correct column)
    ax.annotate(country['ADMIN'], xy=(centroid.x, centroid.y), fontsize=8, ha='center')

# Show the plot
plt.show()

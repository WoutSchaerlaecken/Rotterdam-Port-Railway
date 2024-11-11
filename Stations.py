import matplotlib.pyplot as plt

class Station:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Station(name={self.name}, latitude={self.latitude}, longitude={self.longitude})"

# Example stations
stations = [
    Station("Central Station", 51.925, 4.468),
    Station("Schiedam Centrum", 51.922, 4.411),
    Station("The Hague Central", 52.080, 4.324),
    Station("Naaldwijk", 51.999, 4.207),
    Station("Maasvlakte", 51.954, 4.019),
    Station("Europort West", 51.945, 4.115),
    Station("Europort East", 51.919, 4.192),
    Station("Botlek", 51.883, 4.289),
    Station("Vonderlingenplaat", 51.888, 4.354),
    Station("Waalhaven", 51.888, 4.423)
]

# Print all stations
#for station in stations:
    #print(station)

    

# Extract latitude and longitude from stations
latitudes = [station.latitude for station in stations]
longitudes = [station.longitude for station in stations]
names = [station.name for station in stations]

# Create a scatter plot
plt.figure(figsize=(10, 8))
plt.scatter(longitudes, latitudes, marker='o', color='b')

# Annotate each station
for i, name in enumerate(names):
    plt.annotate(name, (longitudes[i], latitudes[i]), textcoords="offset points", xytext=(0,10), ha='center')

# Set labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Station Locations')

# Show plot
plt.grid(True)
plt.show()

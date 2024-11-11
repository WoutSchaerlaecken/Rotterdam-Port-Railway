import networkx as nx
from geopy.distance import geodesic
import pandas as pd
import matplotlib.pyplot as plt

# Define a class for stations
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

# Define a class for connections
class Connection:
    def __init__(self, station1, station2):
        self.station1 = station1
        self.station2 = station2
        self.distance = self.calculate_distance()

    def calculate_distance(self):
        coords_1 = (self.station1.latitude, self.station1.longitude)
        coords_2 = (self.station2.latitude, self.station2.longitude)
        return geodesic(coords_1, coords_2).kilometers

    def __repr__(self):
        return f"Connection({self.station1.name} - {self.station2.name}, distance={self.distance:.2f} km)"

def find_station_by_name(name, stations):
    for station in stations:
        if station.name == name:
            return station
    raise ValueError(f"Station with name {name} not found")

# Example connections using station names
connections = [
    Connection(find_station_by_name("Central Station", stations), find_station_by_name("Schiedam Centrum", stations)),
    Connection(find_station_by_name("Schiedam Centrum", stations), find_station_by_name("Waalhaven", stations)),
    Connection(find_station_by_name("Maasvlakte", stations), find_station_by_name("Europort West", stations)),
    Connection(find_station_by_name("Europort West", stations), find_station_by_name("Europort East", stations)),
    Connection(find_station_by_name("Europort East", stations), find_station_by_name("Botlek", stations)),
    Connection(find_station_by_name("Botlek", stations), find_station_by_name("Vonderlingenplaat", stations)),
    Connection(find_station_by_name("Vonderlingenplaat", stations), find_station_by_name("Waalhaven", stations)),
    Connection(find_station_by_name("The Hague Central", stations), find_station_by_name("Naaldwijk", stations)),
    Connection(find_station_by_name("Naaldwijk", stations), find_station_by_name("Maasvlakte", stations)),
    Connection(find_station_by_name("The Hague Central", stations), find_station_by_name("Central Station", stations))
]

class MetroLine:
    def __init__(self, name, connections, average_speed):
        self.name = name
        self.connections = connections
        self.average_speed = average_speed

    def total_distance(self):
        return sum(connection.distance for connection in self.connections)

    def __repr__(self):
        return f"MetroLine(name={self.name}, connections={len(self.connections)}, total_distance={self.total_distance():.2f} km, average_speed={self.average_speed} km/h)"

# metro lines with different average speeds
metro_lines = [
    MetroLine("Line 1", [connections[0],connections[1]], 55),
    MetroLine("Line 2", [connections[2], connections[3], connections[4], connections[5], connections[6]], 55),
    MetroLine("Line 3", [connections[7], connections[8]], 55),
    MetroLine("Line 4", [connections[9]], 55)
]

# Create a graph representation of the metro network
G = nx.Graph()
for connection in connections:
    G.add_edge(connection.station1.name, connection.station2.name, weight=connection.distance)

# Define a function to calculate travel time between stations
def calculate_travel_time(distance, average_velocity, average_stopping_time, number_of_stops):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    return travel_time + total_stopping_time

# Example parameters
average_stopping_time = 1/60  # minutes

# Create a DataFrame to store travel times
travel_times = pd.DataFrame(index=[station.name for station in stations], columns=[station.name for station in stations])

# Calculate travel times between each pair of stations
for station1 in stations:
    for station2 in stations:
        if station1 != station2:
            # Find the shortest path between the stations
            path = nx.shortest_path(G, source=station1.name, target=station2.name, weight='weight')
            number_of_stops = len(path) - 2 
            distance = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))
            
            # Calculate the average velocity for the path
            total_time = 0
            for i in range(len(path) - 1):
                for line in metro_lines:
                    for connection in line.connections:
                        if (connection.station1.name == path[i] and connection.station2.name == path[i+1]) or (connection.station2.name == path[i] and connection.station1.name == path[i+1]):
                            segment_distance = G[path[i]][path[i+1]]['weight']
                            segment_time = segment_distance / line.average_speed
                            total_time += segment_time
                            break
            
            average_velocity = distance / total_time
            travel_time = round((calculate_travel_time(distance, average_velocity, average_stopping_time, number_of_stops)) * 60, 2)
            travel_times.at[station1.name, station2.name] = travel_time
        else:
            travel_times.at[station1.name, station2.name] = 0  # Travel time to the same station is 0

# Print the travel times table
print(travel_times)

# Extract latitude and longitude from stations
latitudes = [station.latitude for station in stations]
longitudes = [station.longitude for station in stations]
names = [station.name for station in stations]

# Create a scatter plot
plt.figure(figsize=(10, 8))
plt.scatter(longitudes, latitudes, marker='o', color='b')

# Annotate each station
for i, name in enumerate(names):
    plt.annotate(name, (longitudes[i], latitudes[i]), textcoords="offset points", xytext=(0, 10), ha='center')

# Plot metro lines
for line in metro_lines:
    line_latitudes = [connection.station1.latitude for connection in line.connections] + [line.connections[-1].station2.latitude]
    line_longitudes = [connection.station1.longitude for connection in line.connections] + [line.connections[-1].station2.longitude]
    plt.plot(line_longitudes, line_latitudes, marker='o', label=line.name)

plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Station Locations and Metro Lines')
plt.legend()
plt.grid(True)
plt.show()

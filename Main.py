import networkx as nx
from geopy.distance import geodesic
import pandas as pd
import matplotlib.pyplot as plt

from Inputs import stations, connections, metro_lines, average_velocity, average_stopping_time, start_stations, end_stations, average_waiting_time, Configuration
from functions import calculate_travel_time_with_waiting, G, get_number_of_switches

# Print distance between each pair of stations
#for connection in connections:
    #print(f"{connection.station1.name} to {connection.station2.name}: {connection.distance:.2f} km")

# Create DataFrames to store travel times and distances between stations
travel_times = pd.DataFrame(index=[station.name for station in stations], columns=[station.name for station in stations])
distances = pd.DataFrame(index=[station.name for station in stations], columns=[station.name for station in stations])

# Calculate travel times between each pair of stations
for station1 in stations:
    for station2 in stations:
        if station1 != station2:
            # Find the shortest path between the stations
            path = nx.shortest_path(G, source=station1.name, target=station2.name, weight='weight')
            number_of_stops = len(path) - 2 
            distance = sum(G[path[i]][path[i+1]]['weight'] for i in range(len(path) - 1))
            distances.at[station1.name, station2.name] = round(distance, 2)
            number_of_switches = get_number_of_switches(station1.name, station2.name)
            travel_time = round((calculate_travel_time_with_waiting(distance, average_velocity, average_stopping_time, number_of_stops, number_of_switches, average_waiting_time)) * 60, 2)
            travel_times.at[station1.name, station2.name] = travel_time
        else:
            travel_times.at[station1.name, station2.name] = 0  # Travel time to the same station is 0
            distances.at[station1.name, station2.name] = 0

# Create a DataFrame to store travel times for the selected stations to port stations
filtered_travel_times = travel_times.loc[start_stations, end_stations]
filtered_distances = distances.loc[start_stations, end_stations]

#store data in a text file
output_filename = f'Output_Files/Configuration_{Configuration}_filtered_travel_times_and_distances.txt'
with open(output_filename, 'w') as f:
    f.write(f"Configuration {Configuration}:\n")
    f.write("\n")
    f.write("Filtered Travel Times (minutes) from selected stations to port stations:\n")
    f.write(filtered_travel_times.to_string())
    f.write("\n\nFiltered Distances (km) from selected stations to port stations:\n")
    f.write(filtered_distances.to_string())

#Print the travel distances and times
#print("Filtered Travel times (minutes) from selected stations to port stations:")
print(filtered_travel_times)
print(filtered_distances)
#print(distances)


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

# Set labels and title
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title(f'Configuration {Configuration}: Station Locations and Metro Lines')
plt.legend()

# Show plot
plt.grid(True)
plt.savefig(f'Output_Files/Configuration_{Configuration}_station_locations_and_metro_lines.png')
#plt.show()
# Load the background image
#bg_image = plt.imread('Map2.png')

# Plot the background image
#plt.imshow(bg_image, extent=[min(longitudes) - 0.02, max(longitudes) + 0.04, min(latitudes) - 0.08, max(latitudes) +0.05], aspect='auto')

# Show plot
plt.show()

# Save the plot to the Output Files folder

"""This file contains the functions that are used to simulate the metro system."""


import networkx as nx
from Inputs import connections, metro_lines, stations

#Calculate the travel time between two stations
def calculate_travel_time(distance, average_velocity, average_stopping_time, number_of_stops):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    return travel_time + total_stopping_time


def calculate_travel_time_with_waiting(distance, average_velocity, average_stopping_time, number_of_stops, number_of_switches, average_waiting_time):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    total_waiting_time = number_of_switches * average_waiting_time
    return travel_time + total_stopping_time + total_waiting_time


# Create a graph to represent the metro system
G = nx.Graph()
for connection in connections:
    G.add_edge(connection.station1.name, connection.station2.name, weight=connection.distance)


# Find the station object by its name
def find_station_by_name(name, stations):
    for station in stations:
        if station.name == name:
            return station
    raise ValueError(f"Station with name {name} not found")

# Find the number of line changes between two stations
def get_number_of_switches(station1_name, station2_name):
    if station1_name == station2_name:
        return 0  # No line changes to the same station

    station1 = find_station_by_name(station1_name, stations)
    station2 = find_station_by_name(station2_name, stations)

    # Find the shortest path between the stations
    path = nx.shortest_path(G, source=station1.name, target=station2.name, weight='weight')

    # Determine the line of the starting and ending stations
    start_line = None
    end_line = None
    for line in metro_lines:
        if any(connection.station1.name == path[0] and connection.station2.name == path[1] for connection in line.connections):
            start_line = line
        if any(connection.station1.name == path[-2] and connection.station2.name == path[-1] for connection in line.connections):
            end_line = line

    # Check if the start and end stations are on different lines
    if start_line != end_line:
        return 1
    else:
        return 0
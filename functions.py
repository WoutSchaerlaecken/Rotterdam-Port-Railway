"""This file contains the functions that are used to simulate the metro system."""


import networkx as nx
from Inputs import connections, metro_lines


def calculate_travel_time(distance, average_velocity, average_stopping_time, number_of_stops):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    return travel_time + total_stopping_time


G = nx.Graph()
for connection in connections:
    G.add_edge(connection.station1.name, connection.station2.name, weight=connection.distance)


def number_of_line_changes(path):
    number_of_switches = 0
    for i in range(len(path) - 1):
        current_station = path[i]
        next_station = path[i + 1]
        current_line = None
        next_line = None
        for line in metro_lines:
            if any(connection.station1.name == current_station and connection.station2.name == next_station for connection in line.connections):
                current_line = line
            if any(connection.station1.name == next_station and connection.station2.name == path[i+1] for connection in line.connections):
                next_line = line
        if current_line != next_line:
            number_of_switches += 1
    return number_of_switches

def calculate_travel_time_with_waiting(distance, average_velocity, average_stopping_time, number_of_stops, number_of_switches, average_waiting_time):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    total_waiting_time = number_of_switches * average_waiting_time
    return travel_time + total_stopping_time + total_waiting_time
"""This file contains the functions that are used to simulate the metro system."""


import networkx as nx
from Inputs import connections


def calculate_travel_time(distance, average_velocity, average_stopping_time, number_of_stops):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    return travel_time + total_stopping_time


G = nx.Graph()
for connection in connections:
    G.add_edge(connection.station1.name, connection.station2.name, weight=connection.distance)
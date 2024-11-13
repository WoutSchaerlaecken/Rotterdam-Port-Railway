"""This file contains the functions that are used to simulate the metro system."""

def calculate_travel_time(distance, average_velocity, average_stopping_time, number_of_stops):
    travel_time = distance / average_velocity
    total_stopping_time = number_of_stops * average_stopping_time
    return travel_time + total_stopping_time

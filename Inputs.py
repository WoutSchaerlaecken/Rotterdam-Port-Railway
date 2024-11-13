"""---This file will be used to input the stations, their locations, the lines---""" 
"""--------and other information required to simulate the metro system.----------"""

from metro_classes import Station, Connection, find_station_by_name, MetroLine



#Define average speed and stopping time
average_velocity = 70  # km/h
average_stopping_time = 1/60  # minutes


# Create stations with their names and coordinates
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

# Create connections between stations
connections = [
    Connection(find_station_by_name("Central Station", stations), find_station_by_name("Schiedam Centrum", stations)),
    Connection(find_station_by_name("Schiedam Centrum", stations), find_station_by_name("Europort East", stations)),
    Connection(find_station_by_name("Maasvlakte", stations), find_station_by_name("Europort West", stations)),
    Connection(find_station_by_name("Europort West", stations), find_station_by_name("Europort East", stations)),
    Connection(find_station_by_name("Europort East", stations), find_station_by_name("Botlek", stations)),
    Connection(find_station_by_name("Botlek", stations), find_station_by_name("Vonderlingenplaat", stations)),
    Connection(find_station_by_name("Vonderlingenplaat", stations), find_station_by_name("Waalhaven", stations)),
    Connection(find_station_by_name("The Hague Central", stations), find_station_by_name("Naaldwijk", stations)),
    Connection(find_station_by_name("Naaldwijk", stations), find_station_by_name("Europort East", stations)),
]

# Define metro lines 
metro_lines = [
    MetroLine("Line 1", [connections[0], connections[1]]),
    MetroLine("Line 2", [connections[2], connections[3], connections[4], connections[5], connections[6]]),
    MetroLine("Line 3", [connections[7], connections[8]]),
]
# metro_classes.py

from geopy.distance import geodesic

class Station:
    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Station(name={self.name}, latitude={self.latitude}, longitude={self.longitude})"

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

class MetroLine:
    def __init__(self, name, connections):
        self.name = name
        self.connections = connections

    def total_distance(self):
        return sum(connection.distance for connection in self.connections)

    def __repr__(self):
        return f"MetroLine(name={self.name}, connections={len(self.connections)}, total_distance={self.total_distance():.2f} km)"
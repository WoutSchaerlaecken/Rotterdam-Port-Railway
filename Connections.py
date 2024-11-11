# Connections.py

class Connection:
    def __init__(self, station1, station2, distance):
        self.station1 = station1
        self.station2 = station2
        self.distance = distance

    def __repr__(self):
        return f"Connection({self.station1}, {self.station2}, {self.distance} km)"

class Connections:
    def __init__(self):
        self.connections = []

    def add_connection(self, station1, station2, distance):
        connection = Connection(station1, station2, distance)
        self.connections.append(connection)

    def get_connections(self):
        return self.connections

# Example usage
if __name__ == "__main__":
    connections = Connections()
    connections.add_connection("StationA", "StationB", 5)
    connections.add_connection("StationB", "StationC", 10)
    for connection in connections.get_connections():
        print(connection)
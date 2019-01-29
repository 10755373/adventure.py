from inventory import Inventory

class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description):
        """
        Initializes a Room
        """
        self.id = id
        self.name = name
        self.description = description
        self.inventory = Inventory()
        self.connections = {}

    def add_route(self, direction, room):
        """
        Adds a given direction and the connected room to our room object.
        """
        self.connections[direction] = room

    def is_connected(self, direction, inventory):
        """
        Checks whether the given direction has a connection from a room.
        """
        if direction in self.connections:
            heading_room = self.connections[direction]
            if "/" in heading_room:
                destination = heading_room.split("/")
                room = destination[0]
                condition = destination[1]
                for item in inventory:
                    if item.name == condition:
                        return(int(heading_room))
                    else:
                        return False
            else:
                return(int(heading_room))
        else:
            return False

    def __str__(self):
        return f"{self.description}"
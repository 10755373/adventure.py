class Item(object):
    """
    Representation of item object in adventure
    """

    def __init__(self, name, description, initial_room_id):

        self.name = name
        self.description = description
        self. initial_room_id = initial_room_id

    def __str__(self):
        return f"{self.name}: {self.description}"
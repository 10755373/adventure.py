from room import Room
import sys
from items import Item
from inventory import Inventory


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """
    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.current_room = self.rooms[1]
        self.items = self.load_items(f"data/{game}Items.txt")
        self.synonyms = self.load_synonyms(f"data/SmallSynonyms.txt")

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a dictionary of 'id' : Room objects.
        """
        # First we parse all the data we need to create the rooms with.
        # All parsed lines of data are saved to rooms_data.
        self.rooms_data = []
        with open(filename, "r") as f:
            self.room_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    self.room_data.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    self.rooms_data.append(self.room_data)
                    self.room_data = []
        # Append a final time, because the files do not end on a blank newline.
        self.rooms_data.append(self.room_data)

        # Create room objects for each set of data we just parsed.
        rooms = {}
        for room_data in self.rooms_data:
            id = int(room_data[0])
            name = room_data[1]
            description = room_data[2]

            # Initialize a room object and put it in a dictionary with its
            # id as key.
            room = Room(id, name, description)
            rooms[id] = room

        # Add routes to each room we've created with the data from each set
        # we have parsed earlier.
        for room_data in self.rooms_data:
            id = int(room_data[0])
            # We split to connections into a direction and a room_id.
            connections = room_data[4:]
            connections = [connection.split() for connection in connections]
            # Here we get the current room object that we'll add routes to.
            room = rooms[id]
            for connection, target_room_id in connections:
                # TODO add routes to a room (hint: use the add route method)
                connection = connections[0]
                target_room_id = connections[1]
                self.room_data[id].add_route(connection, target_room_id)
        return rooms

    def load_items(self, filename):
        """
        Load items from filename.
        Place them into the inventory of a room.
        """
        # Create playes inventory.
        self.player_inventory = Inventory()
        # Read file
        with open(filename, "r") as f:
            # make list and iterate over each part
            self.items_data = []
            for text in f:
                # split text
                text.split()
                if text.isupper():
                    name = text
                elif text.islower():
                    description = text
                elif text.isdigit():
                    initial_room_id = text
                    # look for same id and place item in that specific room
                    for room in self.room_data:
                        if initial_room_id == room.id:
                            room.inventory.add(Item(name, description, initial_room_id))

    def load_synonyms(self, filename):
        # make dictinary and put synonyms in it
        self.dict_synonyms = {}
        # read file
        with open(filename, "r") as f:
            # make list and iterate over seperate parts
            self.list_synonyms = []
            for line in f:
                lines = line.strip()
                lines_seperated = lines.split("=")
                # add parts to dictionary
                self.dict_synonyms[lines_seperated[0]] = lines_seperated[1]

    def game_over(self):
        """
        Check if the game is over.
        Returns a boolean.
        """
        if self.current_room == self.rooms[-1]:
            return True
        else:
            return False

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        inventory = self.player_inventory.inventory_list
        #Update the current room to a connected direction.
        if (self.current_room.is_connected(direction, inventory)) is False:
            print(f"Invalid command")
        else:
            heading_room = self.current_room.is_connected(direction, inventory)
            self.current_room = self.rooms[heading_room]
        while "FORCED" in self.current_room.connections():
            direction = "FORCED"
            heading_room = self.current_room.is_connected(direction, inventory)
            self.current_room = self.rooms[heading_room]
            if (self.game_over()) is False:
                return(self.current_room.description)
            else:
                return(self.game_over())
                break

    def take_item(self, item):
        if item in self.current_room.inventory.return_inventory(item):
            item = self.current_room.inventory.return_inventory(item)
            self.player_inventory.add(item)
            self.current_room.inventory.remove(item)
            print(f"{item.name} taken.")
        else:
            print(f"No such item.")

    def drop_item(self, item):
        if item in self.player_inventory.return_inventory(item):
            item = self.player_inventory.return_inventory(item)
            self.player_inventory.remove(item)
            self.current_room.inventory.add(item)
            print(f"{item.name} dropped.")
        else:
            print(f"No such item.")

    def help_command(self):
        """
        Returns help text
        """
        print(f"""
You can move by typing directions such as EAST/WEST/IN/OUT
QUIT quits the game.
HELP prints instructions for the game.
INVENTORY lists the item in your inventory.
LOOK lists the complete description of the room and its contents.
TAKE <item> take item from the room.
DROP <item> drop item from your inventory.
        """)

    def quit_command(self):
        """
        Exits game.
        """
        print("Thanks for playing!")
        sys.exit()

    def look_command(self):
        """
        prints description of room and items in inventory.
        """
        # print description
        print(self.current_room)
        # print inventory
        if self.current_room.inventory.check_inventory():
            print(self.current_room.inventory)

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")
        # let know which room player is currently in
        print(self.current_room)
        # keep track of visted rooms
        rooms_visited = []
        # add first room to list
        rooms_visited.append(1)
        # Prompt the user for commands until they've won the game.
        while not self.game_over():
            command = input("> ")
            # Check if the command is a movement or not.
            if command is not command.isupper():
                command.upper()
            if command in ["Q", "L", "I", "N", "S", "E", "W", "U", "D"]:
                command = self.dict_synonyms[command]
            if command in self.current_room.connections:
                self.move(command)
                if self.current_room in rooms_visited:
                    # print short description
                    print(self.current_room.name)
                    # print inventory
                    if self.current_room.inventory.check_inventory():
                        print(self.current_room.inventory)
                else:
                    if self.game_over():
                        pass
                    else:
                        # add room to list
                        rooms_visited.append(self.current_room.id)
                        # print full description
                        print(self.current_room.description)
                        # print inventory
                        if self.current_room.inventory.check_inventory():
                            print(self.current_room.inventory)
            # option to look in room (both uppercase as well as undercase letters)
            elif command == "LOOK" or "look":
                self.look_command()
            # option to get help (both uppercase as well as undercase letters)
            elif command == "HELP" or "help":
                self.help_command()
            # option to quit game (both uppercase as well as undercase letters)
            elif command == "QUIT" or "quit":
                self.quit_command()
            # have a look at player's inventory (both uppercase as well as undercase letters)
            elif command == "INVENTORY" or "inventory":
                if self.player_inventory.check_inventory() is True:
                    print(f"{self.player_inventory}")
                else:
                    print(f"Your inventory in empty.")
        else:
            print(f"Invalid command")

if __name__ == "__main__":
    adventure = Adventure("Crowther")
    adventure.play()

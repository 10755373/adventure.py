class Inventory(object):
    """
    Representation of inventory objects in adventure
    """

    def __init__(self):
        # a list for the items in the inventory
        self.inventory_list = []

    def add(self, item):
        """
        Append item to the inventory_list
        """
        self.inventory_list.append(item)

    def remove(self, item):
        """
        Remove item from the inventory_list
        """
        self.inventory_list.remove(item)

    def check_inventory(self):
        """
        Check if inventory_list is empty or not
        """
        if len(self.inventory_list) > 0:
            return True
        else:
            return False

    def return_inventory(self, item):
        """
        Look if item in inventory_list
        """
        for objects in self.inventory_list:
            if item == objects.name:
                return item
        else:
            return False

    def __str__(self):
        if self.check_inventory() is True:
            for item in self.inventory_list:
                possessed_items = []
                possessed_items.append(f"{item}")
                for items in possessed_items:
                    return('\n'.join(possessed_items))
        else:
            return(f"Inventory is empty.")
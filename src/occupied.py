PERMANENT_OCCUPIED = 0
TEMPORARY_OCCUPIED = 1


class Occupied:
    """
    A class for occupied position in the grid

    Args:
        occupied_type - 0:permanent occupied , 1:temporary occupied
        direction -  valid direction for this occupied pos. right/left/up/down or None otherwise.

    """

    def __init__(self, occupied_type, direction, user_made=False):
        self.occupied_type = occupied_type
        self.direction = direction
        self.user_made = user_made

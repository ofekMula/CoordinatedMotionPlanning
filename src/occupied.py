class Occupied:
    """
    A class for occupied position in the grid

    Args:
        is_temp - 0:permanent occupied , 1:temporary occupied
        direction -  valid direction for this occupied pos. right/left/up/down or None otherwise.

    """
    def __init__(self, is_temp, direction):
        self.is_temp = is_temp
        self.direction = direction

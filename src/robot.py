import queue
class Robot:
    """
    A class for robot object

    Args:
        index - each robot has its own unique index (int)
        current_pos - the current position of the robot on the grid. (tuple)
        target_pos - target position for thr robot to be in the end.(tuple)

    """

    def __init__(self, index, current_pos, target_pos):
        self.index = index
        self.target_pos = target_pos
        self.current_pos = current_pos
        self.distance = 0
        self.prev_pos = None
        self.path = []
        self.way_blocked = list()
        self.last_move_direction = 'E'
        self.last_moves = list()

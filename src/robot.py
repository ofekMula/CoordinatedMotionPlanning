class Robot:
    """
    A class for robot object

    Args:
        index - each robot has its own unique index (int)
        start_pos - the position which the robot placed in initialization. (tuple)
        current_pos - the curreent position of the robot on the grid. (tuple)
        target_pos - target position for thr robot to be in the end.(tuple)

    """
    def __init__(self, index, start_pos, target_pos):
        self.index = index
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.current_pos = start_pos
        self.distance = 0



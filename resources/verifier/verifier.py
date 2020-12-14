import math
import itertools
import numpy as np
from typing import List


class Verifier:
    robots: np.ndarray = []
    objectives: np.ndarray = []
    obstacles: np.ndarray = []
    turns: int = None
    total_steps: int = None

    def __init__(self, robots: np.ndarray, objectives: np.ndarray, obstacles: np.ndarray):
        self.robots = robots
        self.objectives = objectives
        self.obstacles = obstacles
        self.turns = 0
        self.robot_steps = [0 for robot in robots]
        self.total_steps = 0

    def check_win_condition(self):
        return all(np.array_equal(self.robots[i], self.objectives[i]) for i in range(len(self.robots)))


    def check_intersection_with_robot(self, robot1: np.ndarray, robot2: np.ndarray, step1: np.ndarray, step2: np.ndarray) -> bool:
        return np.array_equal(robot1 + step1, robot2 + step2) \
               or ((np.array_equal(robot1 + step1, robot2) and not np.array_equal(step1, step2))
                   or (np.array_equal(robot2 + step2, robot1) and not np.array_equal(step1, step2)))

    def check_intersection_with_obstacle(self, robot: np.ndarray, obstacle: np.ndarray, step: np.ndarray):
        return np.array_equal(robot + step, obstacle)

    def verify_turn(self, turn: np.ndarray):
        N = len(self.robots)
        for i in range(N):
            # check that we move at most 1, in at most one axis
            if not all(-1 <= c <= 1 for c in turn[i]):
                print("Robot", i, "moves more than 1 unit")
                return False
            if not any(c == 0 for c in turn[i]):
                print("Robot", i, "moves more than 1 unit")
                return False
            for j in range(i+1, N):
                if self.check_intersection_with_robot(self.robots[i], self.robots[j], turn[i], turn[j]):
                    print("Robot", i, "collides with robot", j)
                    return False
            for obstacle in self.obstacles:
                if self.check_intersection_with_obstacle(self.robots[i], obstacle, turn[i]):
                    print("Robot", i, "collides with one of the obstacles")
                    return False
        return True

    def execute_turn(self, turn: np.ndarray):
        if not self.verify_turn(turn):
            return None

        self.turns += 1
        N = len(self.robots)
        for i in range(N):
            self.robots[i] += turn[i]
            if not np.array_equal(turn[i], np.array([0, 0])):
                self.total_steps += 1
                self.robot_steps[i] += 1

        if self.check_win_condition():
            return True

        return False

#test
if __name__ == "__main__":
    robots = np.array([[0,0], [2,2]])
    objectives = np.array([[2,2], [0,0]])
    obstacles = np.array([])
    v = Verifier(robots, objectives, obstacles)
    v.execute_turn(np.array([[0,0], [1,0]]))
    print(v.robots)


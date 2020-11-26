import numpy as np
import json

def direction_to_vector(d: str):
    if d == "W": return np.array([-1, 0])
    if d == "E": return np.array([1, 0])
    if d == "N": return np.array([0, 1])
    if d == "S": return np.array([0, -1])
    return None

def read_scene(s):
    f = open(s, 'r')
    data = json.load(f)
    obstacles = np.array(data['obstacles'])
    starts = np.array(data['starts'])
    targets = np.array(data['targets'])
    return [starts, targets, obstacles]


def read_sol(s, num_robots):
    f = open(s, 'r')
    data = json.load(f)
    steps = data['steps']
    turns = np.array([[np.array([0,0]) for i in range(num_robots)] for i in range(len(steps))])
    for i, step in enumerate(steps):
        for robot in step:
            j = int(robot)
            turns[i][j] += direction_to_vector(step[robot])
    return turns

if __name__ == "__main__":
    read_scene('C:\dev\coordinated_motion_planning\data\simple.json')

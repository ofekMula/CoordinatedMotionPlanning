import json

from robot import Robot


def read_scene(scene_path: str):
    with open(scene_path, 'r') as f:
        scene = json.load(f)
    starts, targets, obstacles = scene['starts'], scene['targets'], scene['obstacles']
    robots = [Robot(index, tuple(starts[index]), tuple(targets[index])) for index in range(len(starts))]
    obstacles = set(tuple(a) for a in obstacles)
    return robots, obstacles, scene['name']


DIRECTION_TO_VECTOR = {'up': (0, 1), 'right': (1, 0), 'down': (0, -1), 'left': (-1, 0), 'halt': (0, 0)}
STEP_DIRECTION = {'up': 'N', 'right': 'E', 'down': 'S', 'left': 'W'}
STEP_DIRECTION_REVERSED = {'N': 'up', 'E': 'right', 'S': 'down', 'W': 'left', None: None}


def calc_next_pos(location, direction):
    return location[0] + DIRECTION_TO_VECTOR[direction][0], location[1] + DIRECTION_TO_VECTOR[direction][1]


def write_solution(steps, name, outfile):
    with open(outfile, 'w') as f:
        f.write(json.dumps({"instance": name, "steps": steps}, indent=4))

import json

from navie_solver import RIGHT, DOWN, LEFT, UP, HALT
from robot import Robot


def read_scene(scene_path: str):
    with open(scene_path, 'r') as f:
        scene = json.load(f)
    starts, targets, obstacles = scene['starts'], scene['targets'], scene['obstacles']
    robots = [Robot(index, tuple(starts[index]), tuple(targets[index])) for index in range(len(starts))]
    obstacles = set(tuple(a) for a in obstacles)
    return robots, obstacles, scene['name']


DIRECTION_TO_VECTOR = {UP: (0, 1), RIGHT: (1, 0), DOWN: (0, -1), LEFT: (-1, 0), HALT: (0, 0)}


def calc_next_pos(location, direction):
    return location[0] + DIRECTION_TO_VECTOR[direction][0], location[1] + DIRECTION_TO_VECTOR[direction][1]


def write_solution(steps, name, outfile):
    with open(outfile, 'w') as f:
        f.write(json.dumps({"instance": name, "steps": steps}, indent=4))

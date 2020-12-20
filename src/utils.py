import json
from robot import Robot

UP = 'N'
DOWN = 'S'
RIGHT = 'E'
LEFT = 'W'
HALT = 'halt'


def read_scene(scene_path: str):
    with open(scene_path, 'r') as f:
        scene = json.load(f)
    starts, targets, obstacles = scene['starts'], scene['targets'], scene['obstacles']
    robots = [Robot(index, tuple(starts[index]), tuple(targets[index])) for index in range(len(starts))]
    obstacles = set(tuple(a) for a in obstacles)
    return robots, obstacles, scene['name']


DIRECTION_TO_VECTOR = {UP: (0, 1), RIGHT: (1, 0), DOWN: (0, -1), LEFT: (-1, 0), HALT: (0, 0)}
VECTOR_TO_DIRECTION = { (0, 1):UP, (1, 0):RIGHT, (0, -1):DOWN, (-1, 0):LEFT,  (0, 0):HALT}
OPPOSING_DIRECTION ={UP:DOWN, RIGHT:LEFT, DOWN:UP, LEFT:RIGHT}
UPRIGHT_DIRECTION ={UP:LEFT, RIGHT:DOWN, DOWN:RIGHT, LEFT:UP}


def calc_next_pos(location, direction):
    return location[0] + DIRECTION_TO_VECTOR[direction][0], location[1] + DIRECTION_TO_VECTOR[direction][1]


def write_solution(steps, name, outfile):
    with open(outfile, 'w') as f:
        f.write(json.dumps({"instance": name, "steps": steps}, indent=4))


def write_metadata(metadata):
    with open('../tests/actual_metadata.json', 'w') as f:
        f.write(json.dumps(metadata, indent=4))

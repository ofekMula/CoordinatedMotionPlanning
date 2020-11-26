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
    name = data['name']
    f.close()
    return [starts, targets, obstacles], name

def write_solution(steps, name, outfile):
    x = {"instance": name, "steps": []}
    for step in steps:
        step_dict = {}
        for i, robot in enumerate(step):
            d = ""
            if np.array_equal(robot, np.array([1, 0])):
                d = "E"
            if np.array_equal(robot, np.array([0, 1])):
                d = "N"
            if np.array_equal(robot, np.array([-1, 0])):
                d = "W"
            if np.array_equal(robot, np.array([0, -1])):
                d = "S"
            if d:
                step_dict[str(i)] = d
        x["steps"].append(step_dict)
    res = json.dumps(x, indent=4)
    o = open(outfile, 'w')
    o.write(res)



if __name__ == "__main__":
    read_scene('scene1')

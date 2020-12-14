import numpy as np
import read_scene
import networkx as nx
import sys
from project_inputs.solvers.Robot import Robot


def update_graph(grid):
    """
    need to update the graph after we make a moves
    """
    return None

def move_robot(robot,invalid_positions):
    """
    need to calculate shortest path +
    update robot current pos +
    add move to data structure
    """
    return None

def sort_robots(robots):
    return sorted(robots, key=lambda robot: robot.distance)

def calculate_distance(robots):
    for robot in robots:
        target_pos = robot.target_pos
        start_pos = robot.start_pos
        robot.distance = (int)(abs(target_pos[0]-start_pos[0]) + abs(target_pos[1]-start_pos[1]))

def solve(infile: str, outfile: str):
    scene, name = read_scene.read_scene(infile)
    robots_num = len(scene[0])
    robots = []  # list of robots to hold data for each robot in the grid.
    obstacles = set(tuple(a) for a in scene[2])
    for robot_index in range(robots_num):
        robots.append(Robot(robot_index, tuple(scene[0][robot_index]), tuple(scene[1][robot_index])))

    invalid_positions = set(obstacle for obstacle in obstacles)
    invalid_positions.add(robot.current_pos for robot in robots)

    calculate_distance(robots)
    robots = sort_robots(robots)
    # Calculate scene bounding box
    all_points = [robot.start_pos for robot in robots] + [robot.target_pos for robot in robots] + list(obstacles)
    min_x = min(a[0] for a in all_points)
    max_x = max(a[0] for a in all_points)
    min_y = min(a[1] for a in all_points)
    max_y = max(a[1] for a in all_points)

    grid = [(x, y) for x in range(min_x-1, max_x+2) for y in range(min_y-1, max_y+2)]
    G = nx.Graph()

    flag= True
    moves=[]  # a data structure to hold all the moves for each robot
    while flag: #while not all robots finished
        for prior_index in range(len(robots)): #move each robot accordingly to its priority
            move_robot(robots[prior_index], invalid_positions)
            update_graph(grid)

    #after the algorithm finished, we should write the moves data structure to json file.







if __name__ == "__main__":
    if __name__ == "__main__":
        solve(infile='scene_2.json', outfile='scene_2_sol.json')
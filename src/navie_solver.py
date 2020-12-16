import networkx as nx
import utils
import os
import time
from logbook import Logger
import sys
from logbook_utils import ColoredStreamHandler
from occupied import Occupied

ColoredStreamHandler(sys.stdout).push_application()
log: Logger


def calc_robot_next_step(robot, invalid_positions):

    go_right = (robot.target_pos[0] - robot.current_pos[0]) > 0
    go_up = (robot.target_pos[1] - robot.current_pos[1]) > 0
    go_left = (robot.target_pos[0] - robot.current_pos[0]) < 0
    go_down = (robot.target_pos[1] - robot.current_pos[1]) < 0
    if go_right:
        right_pos = utils.calc_next_pos(robot.current_pos, 'right')
        if right_pos not in invalid_positions or (right_pos in invalid_positions and
                                                  invalid_positions[right_pos].direction == 'right'):
            return right_pos, utils.STEP_DIRECTION['right']
    if go_left:
        left_pos = utils.calc_next_pos(robot.current_pos, 'left')
        if left_pos not in invalid_positions or (left_pos in invalid_positions and
                                                 invalid_positions[left_pos].direction == 'left'):
            return left_pos, utils.STEP_DIRECTION['left']
    if go_up:
        up_pos = utils.calc_next_pos(robot.current_pos, 'up')
        if up_pos not in invalid_positions or (up_pos in invalid_positions and
                                               invalid_positions[up_pos].direction == 'up'):
            return up_pos, utils.STEP_DIRECTION['up']
    if go_down:
        down_pos = utils.calc_next_pos(robot.current_pos, 'down')
        if down_pos not in invalid_positions or (down_pos in invalid_positions and
                                                 invalid_positions[down_pos].direction == 'down'):
            return down_pos, utils.STEP_DIRECTION['down']

    return robot.current_pos, None


def sort_robots(robots):
    return sorted(robots, key=lambda robot: robot.distance)


def update_robots_distances(robots, graph):
    for robot in robots:
        target_pos = robot.target_pos
        current_pos = robot.current_pos
        # robot.distance = abs(target_pos[0] - current_pos[0]) + abs(target_pos[1] - current_pos[1])
        if nx.has_path(graph, current_pos, target_pos):
            sp = nx.shortest_path(graph, current_pos, target_pos)
            robot.distance = len(sp) - 1


def create_graph(robots, obstacles):
    all_points = [robot.current_pos for robot in robots] + [robot.target_pos for robot in robots] + list(obstacles)
    min_x = min(a[0] for a in all_points)
    max_x = max(a[0] for a in all_points)
    min_y = min(a[1] for a in all_points)
    max_y = max(a[1] for a in all_points)
    grid = [(x, y) for x in range(min_x - 1, max_x + 2) for y in range(min_y - 1, max_y + 2)]
    graph = nx.Graph()
    graph.add_nodes_from(grid)
    for u in graph.nodes:
        # Add valid edges
        for x in range(max(min_x - 1, u[0] - 1), min(max_x + 1, u[0] + 1)):
            if x == u[0]:
                for y in range(max(min_y - 1, u[1] - 1), min(max_y + 1, u[1] + 1)):
                    v = (x, y)
                    if v not in obstacles:
                        graph.add_edge(u, v)
            else:
                y = u[1]
                v = (x, y)
                if v not in obstacles:
                    graph.add_edge(u, v)
    return graph


def clean_invalid_position(invalid_positions):
    positions_to_clean = []
    for pos in invalid_positions:
        if invalid_positions[pos].direction is not None and invalid_positions[pos].is_temp == 1:
            positions_to_clean.append(pos)
    for pos in positions_to_clean:
        del invalid_positions[pos]


def move_robot(robot, robot_next_pos, invalid_positions, direction):
    is_temp = 0
    invalid_positions[robot.current_pos].direction = utils.STEP_DIRECTION_REVERSED[direction]
    robot.current_pos = robot_next_pos
    if robot.current_pos != robot.target_pos:
        is_temp = 1
    invalid_positions[robot.current_pos] = Occupied(is_temp, None)


def is_not_finished(robots):
    log.debug(f'Finished robots: {sum(robot.current_pos == robot.target_pos for robot in robots)}/{len(robots)}')
    return not all(robot.current_pos == robot.target_pos for robot in robots)


def is_not_stuck(steps):
    if len(steps) > 0 and len(steps[-1]) == 0:
        return False
    return True


def load_occupied_positions(robots, obstacles_pos):
    invalid_positions = dict()
    for obstacle in obstacles_pos:
        invalid_positions[obstacle] = Occupied(0, None)
    for robot in robots:
        invalid_positions[robot.current_pos] = (Occupied(1, None))
    return invalid_positions


def solve(infile: str, outfile: str):
    start_time = time.time()
    robots, obstacles, name = utils.read_scene(infile)
    global log
    log = Logger(os.path.split(file_name)[1])
    invalid_positions = load_occupied_positions(robots, obstacles)
    graph = create_graph(robots, obstacles)
    update_robots_distances(robots, graph)
    robots = sort_robots(robots)
    steps = []  # a data structure to hold all the moves for each robot
    step_number = 0
    while is_not_finished(robots) and is_not_stuck(steps):  # while not all robots finished
        steps.append(dict())  # each step holds dictionary <robot_index,robot_step>
        for robot in robots:  # move each robot accordingly to its priority
            robot_next_pos, robot_step = calc_robot_next_step(robot, invalid_positions)
            move_robot(robot, robot_next_pos, invalid_positions, robot_step)
            if robot_step:
                steps[step_number][str(robot.index)] = robot_step
                log.debug(f'step_number={step_number}, robot={robot.index}, move={robot_step}')
        clean_invalid_position(invalid_positions)
        step_number += 1

    # after the algorithm finished, we should write the moves data structure to json file.
    utils.write_solution(steps, name, outfile)
    if not is_not_finished(robots):
        log.info(f'Finished! {time.time() - start_time}s')
    else:
        log.warn(f'Stuck! {time.time() - start_time}s')


if __name__ == "__main__":
    for file_name in os.listdir('../tests/inputs/'):
        solve(infile=f'../tests/inputs/{file_name}', outfile=f'../tests/outputs/{file_name}')
#    file_name = 'simple_election.json'
#   solve(infile=f'../tests/inputs/{file_name}', outfile=f'../tests/outputs/{file_name}')

import networkx as nx
import utils
import os
import time
from logbook import Logger, INFO
import sys
from logbook_utils import ColoredStreamHandler
from occupied import Occupied, PERMANENT_OCCUPIED, TEMPORARY_OCCUPIED

UP = 'N'
DOWN = 'S'
RIGHT = 'E'
LEFT = 'W'
HALT = 'halt'

ColoredStreamHandler(sys.stdout).push_application()
log: Logger


def calc_robot_next_step(robot, invalid_positions):
    go_right = (robot.target_pos[0] - robot.current_pos[0]) > 0
    go_up = (robot.target_pos[1] - robot.current_pos[1]) > 0
    go_left = (robot.target_pos[0] - robot.current_pos[0]) < 0
    go_down = (robot.target_pos[1] - robot.current_pos[1]) < 0
    for go_condition, go_direction in zip([go_right, go_left, go_up, go_down], [RIGHT, LEFT, UP, DOWN]):
        if go_condition:
            next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
            if next_pos not in invalid_positions or invalid_positions[next_pos].direction == go_direction:
                return next_pos, go_direction
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
        if invalid_positions[pos].direction and invalid_positions[pos].occupied_type == TEMPORARY_OCCUPIED:
            positions_to_clean.append(pos)
    for pos in positions_to_clean:
        del invalid_positions[pos]


def move_robot(robot, robot_next_pos, invalid_positions, direction):
    # The order of these lines are important
    invalid_positions[robot.current_pos].direction = direction
    robot.current_pos = robot_next_pos
    occupied_type = PERMANENT_OCCUPIED if robot.current_pos == robot.target_pos else TEMPORARY_OCCUPIED
    invalid_positions[robot.current_pos] = Occupied(occupied_type, None)


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
        invalid_positions[obstacle] = Occupied(PERMANENT_OCCUPIED, None)
    for robot in robots:
        invalid_positions[robot.current_pos] = (Occupied(TEMPORARY_OCCUPIED, None))
    return invalid_positions


def solve(infile: str, outfile: str):
    global log
    log = Logger(os.path.split(infile)[1], level=INFO)
    log.info('Started!')
    start_time = time.time()

    robots, obstacles, name = utils.read_scene(infile)
    invalid_positions = load_occupied_positions(robots, obstacles)
    graph = create_graph(robots, obstacles)
    update_robots_distances(robots, graph)
    robots = sort_robots(robots)
    steps = []  # a data structure to hold all the moves for each robot
    step_number = 0
    while is_not_finished(robots) and is_not_stuck(steps):  # while not all robots finished
        steps.append(dict())  # each step holds dictionary <robot_index,next_direction>
        for robot in robots:  # move each robot accordingly to its priority
            next_pos, next_direction = calc_robot_next_step(robot, invalid_positions)
            move_robot(robot, next_pos, invalid_positions, next_direction)
            if next_direction:
                steps[step_number][str(robot.index)] = next_direction
                log.debug(f'step_number={step_number}, robot={robot.index}, move={next_direction}')
        clean_invalid_position(invalid_positions)
        step_number += 1

    # after the algorithm finished, we should write the moves data structure to json file.
    utils.write_solution(steps, name, outfile)
    if not is_not_finished(robots):
        log.info(f'Finished! {time.time() - start_time}s')
    else:
        log.warn(f'Stuck! {time.time() - start_time}s')


def main():
    for file_name in os.listdir('../tests/inputs/'):
        solve(infile=f'../tests/inputs/{file_name}', outfile=f'../tests/outputs/{file_name}')
    # file_name = 'simple_election.json'
    # solve(infile=f'../tests/inputs/{file_name}', outfile=f'../tests/outputs/{file_name}')


if __name__ == "__main__":
    main()

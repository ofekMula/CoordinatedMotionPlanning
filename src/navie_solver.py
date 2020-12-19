import networkx as nx
import utils
import os
import time
from logbook import Logger, INFO
import sys
from logbook_utils import ColoredStreamHandler
from occupied import Occupied, PERMANENT_OCCUPIED, TEMPORARY_OCCUPIED
from utils import RIGHT, DOWN, LEFT, UP

ColoredStreamHandler(sys.stdout).push_application()
log: Logger


def calc_robot_next_step(robot, invalid_positions, stuck):
    go_right = (robot.target_pos[0] - robot.current_pos[0]) > 0
    go_up = (robot.target_pos[1] - robot.current_pos[1]) > 0
    go_left = (robot.target_pos[0] - robot.current_pos[0]) < 0
    go_down = (robot.target_pos[1] - robot.current_pos[1]) < 0
    try_up = stuck and go_right
    try_left = stuck and go_up
    try_down = stuck and go_left
    try_right = stuck and go_down
    stay = False
    for go_condition, go_direction in zip([go_right, go_up, go_left, go_down], [RIGHT, UP, LEFT, DOWN]):
        if go_condition:
            next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
            if next_pos not in invalid_positions or invalid_positions[next_pos].direction == go_direction:
                if next_pos != robot.prev_pos:
                    return next_pos, go_direction
            if next_pos in invalid_positions and invalid_positions[next_pos].direction is not None:
                stay = True
    if not stay:
        for go_condition, go_direction in zip([try_up, try_left, try_down, try_right], [UP, LEFT, DOWN, RIGHT]):
            if go_condition:
                next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
                if next_pos not in invalid_positions or invalid_positions[next_pos].direction == go_direction:
                    if next_pos != robot.prev_pos:
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
    return sum(map(lambda r: r.distance, robots))


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
    robot.prev_pos = robot.current_pos
    robot.current_pos = robot_next_pos
    occupied_type = PERMANENT_OCCUPIED if robot.current_pos == robot.target_pos else TEMPORARY_OCCUPIED
    invalid_positions[robot.current_pos] = Occupied(occupied_type, None)


def is_not_finished(robots):
    log.debug(f'Finished robots: {sum(robot.current_pos == robot.target_pos for robot in robots)}/{len(robots)}')
    return not all(robot.current_pos == robot.target_pos for robot in robots)


def is_not_stuck(steps):
    if len(steps) > 0 and len(steps[-1]) == 0:
        return False
    if len(steps) > 100:
        return False
    return True


def load_occupied_positions(robots, obstacles_pos):
    invalid_positions = dict()
    for obstacle in obstacles_pos:
        invalid_positions[obstacle] = Occupied(PERMANENT_OCCUPIED, None)
    for robot in robots:
        invalid_positions[robot.current_pos] = (Occupied(TEMPORARY_OCCUPIED, None))
    return invalid_positions


def turn(robot, invalid_positions, steps, step_number, total_moves, stuck_robots, stuck):
    next_pos, next_direction = calc_robot_next_step(robot, invalid_positions, stuck)
    if next_direction:
        move_robot(robot, next_pos, invalid_positions, next_direction)
        steps[step_number][str(robot.index)] = next_direction
        log.debug(f'step_number={step_number}, robot={robot.index}, move={next_direction}')
        total_moves += 1
    elif not stuck:
        stuck_robots.append(robot)
    return total_moves


def solve(infile: str, outfile: str):
    global log
    log = Logger(os.path.split(infile)[1], level=INFO)
    start_time = time.time()

    robots, obstacles, name = utils.read_scene(infile)
    invalid_positions = load_occupied_positions(robots, obstacles)
    graph = create_graph(robots, obstacles)
    remained_distance = update_robots_distances(robots, graph)
    log.info(f'Started! {remained_distance} distance')
    robots = sort_robots(robots)
    steps = []  # a data structure to hold all the moves for each robot
    step_number = 0
    total_moves = 0
    while is_not_finished(robots) and is_not_stuck(steps):  # while not all robots finished
        steps.append(dict())  # each step holds dictionary <robot_index,next_direction>
        stuck_robots = []
        for robot in robots:  # move each robot accordingly to its priority
            total_moves = turn(robot, invalid_positions, steps, step_number, total_moves, stuck_robots, False)
        for robot in stuck_robots:  # move each robot accordingly to its priority
            total_moves = turn(robot, invalid_positions, steps, step_number, total_moves, stuck_robots, True)
        robots = [r for r in robots if r not in stuck_robots] + stuck_robots
        clean_invalid_position(invalid_positions)
        step_number += 1

    # after the algorithm finished, we should write the moves data structure to json file.
    utils.write_solution(steps, name, outfile)

    remained_distance = update_robots_distances(robots, graph)
    total_time = time.time() - start_time
    if not is_not_finished(robots):
        log.info(f'Finished! {total_time}s, {step_number} steps, {total_moves} moves, {remained_distance} distance')
        return {'succeed': True, 'total_time': total_time, 'number_of_steps': step_number,
                'number_of_moves': total_moves, 'remained_distance': remained_distance}
    else:
        log.warn(f'Stuck! {total_time}s, {step_number} steps, {total_moves} moves, {remained_distance} distance')
        return {'succeed': False, 'total_time': total_time, 'number_of_steps': step_number,
                'number_of_moves': total_moves, 'remained_distance': remained_distance}


def main():
    metadata = dict()
    for file_name in os.listdir('../tests/inputs/'):
        if file_name.startswith('large'):
            continue
        metadata[file_name] = solve(infile=f'../tests/inputs/{file_name}', outfile=f'../tests/outputs/{file_name}')
    utils.write_metadata(metadata)
    # file_name = 'simple_election.json'
    # solve(infile=f'../tests/inputs/{file_name}', outfile=f'../tests/outputs/{file_name}')


if __name__ == "__main__":
    main()

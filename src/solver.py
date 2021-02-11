import networkx as nx
import tqdm

import utils
import os
import time
from logbook import Logger, INFO, WARNING, ERROR, DEBUG
import sys
from logbook_utils import ColoredStreamHandler
from occupied import Occupied, PERMANENT_OCCUPIED, TEMPORARY_OCCUPIED
from utils import RIGHT, DOWN, LEFT, UP

ColoredStreamHandler(sys.stdout).push_application()
log = Logger('Base')
root_log = log


def get_all_blocked_directions(robot, blocked_permanent):
    blocked_directions = set()
    for way in robot.way_blocked:
        blocked_directions.add(way[0])
    for direction in blocked_permanent:
        blocked_directions.add(direction)
    return blocked_directions


def is_next_pos_in_last_moves(robot, next_pos):
    for pos in robot.last_moves:
        if next_pos == pos[0]:
            return True
    return False


def calc_sp(robot, invalid_positions):
    grid = create_grid({robot}, invalid_positions)
    g = create_graph(grid, invalid_positions)  # build a new graph.
    sp = calc_stuck_robot_next_steps(robot, g)  # find its shortest path
    if len(sp) > 1:
        next_pos = sp[1]
        go_direction = utils.VECTOR_TO_DIRECTION[subtract_pos(robot.current_pos, next_pos)]
        robot.path = sp[2:]
        return next_pos, go_direction
    return robot.current_pos, None


def create_graph(grid, invalid_positions):
    min_x = min(a[0] for a in grid)
    max_x = max(a[0] for a in grid)
    min_y = min(a[1] for a in grid)
    max_y = max(a[1] for a in grid)
    graph = nx.Graph()
    graph.add_nodes_from(grid)
    for u in graph.nodes:
        # Add valid edges
        for x in range(max(min_x, u[0] - 1), min(max_x, u[0] + 1)):
            if x == u[0]:
                for y in range(max(min_y, u[1] - 1), min(max_y, u[1] + 1)):
                    v = (x, y)
                    go_direction = utils.VECTOR_TO_DIRECTION[subtract_pos(u, v)]
                    if v not in invalid_positions:
                        graph.add_edge(u, v)
                    elif invalid_positions[v].direction == go_direction:
                        graph.add_edge(u, v)
            else:
                y = u[1]
                v = (x, y)
                go_direction = utils.VECTOR_TO_DIRECTION[subtract_pos(u, v)]
                if v not in invalid_positions:
                    graph.add_edge(u, v)
                elif invalid_positions[v].direction == go_direction:
                    graph.add_edge(u, v)
    return graph


def calc_stuck_robot_next_steps(robot, graph):
    sp = []
    if robot.current_pos not in graph or robot.target_pos not in graph:
        return []
    if nx.has_path(graph, robot.current_pos, robot.target_pos):
        # nx.algorithms.shortest_paths.all_pairs_shortest_path()
        # sp = nx.shortest_path(graph, robot.current_pos, robot.target_pos)
        sp = nx.astar_path(graph, robot.current_pos, robot.target_pos)
    return sp


def valid_path(robot, invalid_positions):
    next_pos = robot.path[0]
    if subtract_pos(robot.current_pos, next_pos) not in utils.VECTOR_TO_DIRECTION:
        return False
    direction = utils.VECTOR_TO_DIRECTION[subtract_pos(robot.current_pos, next_pos)]
    if next_pos != robot.current_pos and (
            next_pos not in invalid_positions or invalid_positions[next_pos].direction == direction):
        return True
    return False


def is_step_valid(robot, go_direction, invalid_positions):
    next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
    if next_pos in invalid_positions and invalid_positions[next_pos].direction != go_direction:
        return False
    if next_pos in robot.self_block:
        return False
    return True


def is_blocked_permanent(current_pos, go_direction, invalid_positions):
    next_pos = utils.calc_next_pos(current_pos, go_direction)
    return next_pos in invalid_positions and invalid_positions[next_pos].occupied_type == PERMANENT_OCCUPIED
    # if is_step_valid(current_pos, go_direction, invalid_positions):
    #     return False
    # if next_pos in invalid_positions and invalid_positions[next_pos].occupied_type == PERMANENT_OCCUPIED:
    #     return True
    # return is_blocked_permanent(next_pos, go_direction, invalid_positions)


# def is_only_one_direction_valid(robot, invalid_positions):
#     blocked_directions = list(filter(lambda direction:
#                                      not is_step_valid(robot.current_pos, direction, invalid_positions),
#                                      utils.OPPOSING_DIRECTION.keys()))
#     blocked_permanent = list(filter(lambda direction:
#                                     is_blocked_permanent(robot.current_pos, direction, invalid_positions),
#                                     blocked_directions))
#     if len(blocked_permanent) >= 2 and len(blocked_directions) >= 3:
#         return True
#     return False


def update_robot_if_way_blocked(robot, next_pos, go_direction, invalid_positions, step_number):
    counter_clockwise = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
    direction1 = counter_clockwise[go_direction]
    cur_pos_direction1 = next_pos
    next_pos_direction1 = utils.calc_next_pos(cur_pos_direction1, direction1)
    while next_pos_direction1 in invalid_positions and \
            invalid_positions[next_pos_direction1].occupied_type \
            == PERMANENT_OCCUPIED:
        cur_pos_direction1 = next_pos_direction1
        next_pos_direction1 = utils.calc_next_pos(cur_pos_direction1, direction1)

    direction2 = utils.OPPOSING_DIRECTION[counter_clockwise[go_direction]]
    cur_pos_direction2 = next_pos
    next_pos_direction2 = utils.calc_next_pos(cur_pos_direction2, direction2)
    while next_pos_direction2 in invalid_positions and invalid_positions[next_pos_direction2].occupied_type \
            == PERMANENT_OCCUPIED:
        cur_pos_direction2 = next_pos_direction2
        next_pos_direction2 = utils.calc_next_pos(cur_pos_direction2, direction2)

    if cur_pos_direction1 != cur_pos_direction2:
        if [go_direction, (cur_pos_direction1, cur_pos_direction2)] not in robot.way_blocked:
            log.info(
                f'step {step_number} robot {robot.index} {[go_direction, (cur_pos_direction1, cur_pos_direction2)]}')
            robot.way_blocked.append([go_direction, (cur_pos_direction1, cur_pos_direction2)])
            robot.prev_pos = None


def is_way_not_blocked(robot, next_pos, go_direction):
    blocked_ways = filter(lambda ways: ways[0] == go_direction, robot.way_blocked)
    for blocked_way in blocked_ways:
        blocked_way_start = blocked_way[1][0]
        blocked_way_end = blocked_way[1][1]
        if blocked_way_start[0] == blocked_way_end[0]:
            static = blocked_way_start[0]
            dynamic_min = min(blocked_way_start[1], blocked_way_end[1])
            dynamic_max = max(blocked_way_start[1], blocked_way_end[1])
            if abs(static - robot.current_pos[0]) > abs(static - next_pos[0]) and \
                    dynamic_min <= next_pos[1] <= dynamic_max:
                log.info(
                    f'Cannot move robot {robot.index} in direction {go_direction} from {robot.current_pos} to {next_pos} because {blocked_way}')
                return False
        else:
            static = blocked_way_start[1]
            dynamic_min = min(blocked_way_start[0], blocked_way_end[0])
            dynamic_max = max(blocked_way_start[0], blocked_way_end[0])
            if abs(static - robot.current_pos[1]) > abs(static - next_pos[1]) and \
                    dynamic_min <= next_pos[0] <= dynamic_max:
                log.info(
                    f'Cannot move robot {robot.index} in direction {go_direction} from {robot.current_pos} to {next_pos} because {blocked_way}')
                return False
    return True


def calc_robot_next_step(robot, invalid_positions, stuck, stuck_robots, step_number, robots_dsts):
    valid_directions = list(filter(lambda direction: is_step_valid(robot, direction, invalid_positions),
                                   utils.OPPOSING_DIRECTION.keys()))
    blocked_directions = filter(lambda direction: direction not in valid_directions,
                                utils.OPPOSING_DIRECTION.keys())
    blocked_permanent = list(filter(lambda direction:
                                    is_blocked_permanent(robot.current_pos, direction, invalid_positions),
                                    blocked_directions))
    if len(blocked_permanent) == 3 and robot.current_pos not in robots_dsts:
        invalid_positions[robot.current_pos] = Occupied(PERMANENT_OCCUPIED, None)
        log.info(
            f'step {step_number} robot {robot.index} pos {robot.current_pos} is blocked because {blocked_permanent}')
    elif len(blocked_permanent) == 3 and robot.current_pos in robots_dsts:
        robot.self_block.append(robot.current_pos)
        log.info(
            f'step {step_number} robot self block {robot.index} pos {robot.current_pos} is blocked because {blocked_permanent}')

    go_right = (robot.target_pos[0] - robot.current_pos[0]) > 0
    go_up = (robot.target_pos[1] - robot.current_pos[1]) > 0
    go_left = (robot.target_pos[0] - robot.current_pos[0]) < 0
    go_down = (robot.target_pos[1] - robot.current_pos[1]) < 0
    try_up = stuck and go_right
    try_left = stuck and go_up
    try_down = stuck and go_left
    try_right = stuck and go_down
    directions_to_check = []
    stay = False
    condition_direction_mapping = {RIGHT: go_right, UP: go_up, DOWN: go_down, LEFT: go_left}

    # if robot.last_move_direction in blocked_permanent \
    #         and ((abs(robot.current_pos[0] - robot.target_pos[0]) <= 1
    #               and abs(robot.current_pos[1] - robot.target_pos[1]) > 1)
    #              or (abs(robot.current_pos[1] - robot.target_pos[1]) <= 1 and abs(
    #             robot.current_pos[0] - robot.target_pos[0]) > 1)):
    #     update_robot_if_way_blocked(robot, robot.current_pos, robot.last_move_direction, invalid_positions, step_number)

    if len(robot.path) > 0:  # using the shortest path we calculated before for this robot
        if valid_path(robot, invalid_positions):
            next_pos = robot.path[0]
            go_direction = utils.VECTOR_TO_DIRECTION[subtract_pos(robot.current_pos, next_pos)]
            robot.path = robot.path[1:]
            return next_pos, go_direction
        else:
            robot.path = []

    for go_condition, go_direction in zip(
            [condition_direction_mapping[robot.last_move_direction], go_right, go_up, go_left, go_down],
            [robot.last_move_direction, RIGHT, UP, LEFT, DOWN]):
        if go_condition:
            next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
            if is_step_valid(robot, go_direction, invalid_positions):
                if next_pos != robot.prev_pos and is_way_not_blocked(robot, next_pos, go_direction):
                    return next_pos, go_direction
            if next_pos in invalid_positions and invalid_positions[next_pos].direction is not None:
                stay = True
            if (next_pos in invalid_positions and invalid_positions[next_pos].occupied_type == PERMANENT_OCCUPIED) or \
                    next_pos in robot.self_block:
                update_robot_if_way_blocked(robot, next_pos, go_direction, invalid_positions, step_number)

    if not stay:
        for go_condition, go_direction in zip([try_up, try_left, try_down, try_right], [UP, LEFT, DOWN, RIGHT]):
            if go_condition:
                directions_to_check.append(go_direction)
                next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
                if is_step_valid(robot, go_direction, invalid_positions):
                    if is_way_not_blocked(robot, next_pos, go_direction):
                        if next_pos != robot.prev_pos:
                            return next_pos, go_direction
                        if abs_distance(next_pos, robot.target_pos) > abs_distance(robot.current_pos, robot.target_pos) \
                                and robot.get_backs[next_pos] < 3:
                            if len(valid_directions) > 1:
                                robot.get_backs[next_pos] += 1
                            return next_pos, go_direction

        for direction in directions_to_check:
            go_direction = utils.OPPOSING_DIRECTION[direction]
            next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
            if is_step_valid(robot, go_direction, invalid_positions):
                if is_way_not_blocked(robot, next_pos, go_direction):
                    if next_pos != robot.prev_pos:
                        return next_pos, go_direction
                    if abs_distance(next_pos, robot.target_pos) > abs_distance(robot.current_pos, robot.target_pos) \
                            and robot.get_backs[next_pos] < 3:
                        if len(valid_directions) > 1:
                            robot.get_backs[next_pos] += 1
                        return next_pos, go_direction

            if len(valid_directions) == 1:
                return utils.calc_next_pos(robot.current_pos, valid_directions[0]), valid_directions[0]

            if len(valid_directions) == 2:
                for go_direction in valid_directions:
                    next_pos = utils.calc_next_pos(robot.current_pos, go_direction)
                    if is_way_not_blocked(robot, next_pos, go_direction):
                        return next_pos, go_direction

        if len(valid_directions) == 1:
            return utils.calc_next_pos(robot.current_pos, valid_directions[0]), valid_directions[0]

        # cur_blocked_directions = get_all_blocked_directions(robot, blocked_permanent)
        # if len(cur_blocked_directions) >= 3 and len(valid_directions) > 0:
        #     log.warn(f'Calc SP for robot {robot.index}, step_number={step_number}')
        #     next_pos, go_direction = calc_sp(robot, invalid_positions)
        #     return next_pos, go_direction
    if stuck:
        log.info(
            f'Step {step_number} robot {robot.index} stuck. current {robot.current_pos} target {robot.target_pos}. directions {valid_directions} are valid')

    return robot.current_pos, None


def sort_robots(robots):
    return sorted(robots, key=lambda robot: robot.distance)


def abs_distance(current_pos, target_pos):
    return abs(target_pos[0] - current_pos[0]) + abs(target_pos[1] - current_pos[1])


def update_robots_distances(robots, graph):
    for robot in robots:
        target_pos = robot.target_pos
        current_pos = robot.current_pos
        # robot.distance = abs(target_pos[0] - current_pos[0]) + abs(target_pos[1] - current_pos[1])
        if current_pos in graph and target_pos in graph:
            if nx.has_path(graph, current_pos, target_pos):
                sp = nx.shortest_path(graph, current_pos, target_pos)
                robot.distance = len(sp) - 1
    return sum(map(lambda r: r.distance, robots))


def create_grid(robots, obstacles):
    all_points = [robot.current_pos for robot in robots] + [robot.target_pos for robot in robots] + list(obstacles)
    min_x = min(a[0] for a in all_points) - 1
    max_x = max(a[0] for a in all_points) + 1
    min_y = min(a[1] for a in all_points) - 1
    max_y = max(a[1] for a in all_points) + 1
    grid = [(x, y) for x in range(min_x - 1, max_x + 2) for y in range(min_y - 1, max_y + 2)]
    return grid


def clean_invalid_position(invalid_positions):
    positions_to_clean = []
    for pos in invalid_positions:
        if invalid_positions[pos].direction and invalid_positions[pos].occupied_type == TEMPORARY_OCCUPIED:
            positions_to_clean.append(pos)
    for pos in positions_to_clean:
        del invalid_positions[pos]


def move_robot(robot, robot_next_pos, invalid_positions, direction):
    # The order of these lines are important
    if invalid_positions[robot.current_pos].occupied_type != PERMANENT_OCCUPIED:
        # If the cell was not blocked
        invalid_positions[robot.current_pos].direction = direction
    robot.prev_pos = robot.current_pos
    robot.current_pos = robot_next_pos
    occupied_type = PERMANENT_OCCUPIED if robot.current_pos == robot.target_pos else TEMPORARY_OCCUPIED
    invalid_positions[robot.current_pos] = Occupied(occupied_type, None)
    robot.last_move_direction = direction


def is_not_finished(robots):
    # log.debug(f'Finished robots: {sum(robot.current_pos == robot.target_pos for robot in robots)}/{len(robots)}')
    return not all(robot.current_pos == robot.target_pos for robot in robots)


def is_not_stuck(steps):
    if len(steps) > 0 and len(steps[-1]) == 0:
        return False
    if len(steps) > 200:
        return False
    return True


def load_occupied_positions(robots, obstacles_pos):
    invalid_positions = dict()
    for obstacle in obstacles_pos:
        invalid_positions[obstacle] = Occupied(PERMANENT_OCCUPIED, None)
    for robot in robots:
        invalid_positions[robot.current_pos] = (Occupied(TEMPORARY_OCCUPIED, None))
    return invalid_positions


def turn(robot, invalid_positions, steps, step_number, total_moves, stuck_robots, stuck, robots_dsts):
    next_pos, next_direction = calc_robot_next_step(robot, invalid_positions, stuck, stuck_robots, step_number,
                                                    robots_dsts)
    if next_direction:
        robot.stuck_count = 0
        if step_number > 90:
            log.debug(
                f'step_number={step_number}, robot={robot.index}, move={next_direction} from {robot.current_pos} to {next_pos} dest {robot.target_pos}')
        move_robot(robot, next_pos, invalid_positions, next_direction)
        steps[step_number][str(robot.index)] = next_direction
        total_moves += 1
        robot.last_moves.append((next_pos, next_direction))
        if len(robot.last_moves) >= 4:
            robot.last_moves = robot.last_moves[1:]
    elif not stuck:
        stuck_robots.append(robot)
    else:
        robot.stuck_count += 1
    return total_moves


def subtract_pos(current_pos, next_pos):
    return next_pos[0] - current_pos[0], next_pos[1] - current_pos[1]


def solve(infile: str, outfile: str, level=ERROR):
    global log
    log = Logger(os.path.split(infile)[1], level=level)
    start_time = time.time()

    robots, obstacles, name = utils.read_scene(infile)
    invalid_positions = load_occupied_positions(robots, obstacles)
    grid = create_grid(robots, invalid_positions)
    graph = create_graph(grid, invalid_positions)
    remained_distance = update_robots_distances(robots, graph)
    start_distance = remained_distance
    log.info(f'Started! {remained_distance} distance')
    robots = sort_robots(robots)
    robots_dsts = list(map(lambda robot: robot.target_pos, robots))
    steps = []  # a data structure to hold all the moves for each robot
    step_number = 0
    total_moves = 0
    while is_not_finished(robots) and is_not_stuck(steps):  # while not all robots finished
        steps.append(dict())  # each step holds dictionary <robot_index,next_direction>
        stuck_robots = []
        for robot in robots:  # move each robot accordingly to its priority
            if robot.current_pos != robot.target_pos:
                total_moves = turn(robot, invalid_positions, steps, step_number, total_moves, stuck_robots, False,
                                   robots_dsts)
        for robot in stuck_robots:  # move each robot accordingly to its priority
            if robot.current_pos != robot.target_pos:
                total_moves = turn(robot, invalid_positions, steps, step_number, total_moves, stuck_robots, True,
                                   robots_dsts)
        robots = [r for r in robots if r not in stuck_robots] + stuck_robots
        clean_invalid_position(invalid_positions)
        step_number += 1

    # after the algorithm finished, we should write the moves data structure to json file.
    utils.write_solution(steps, name, outfile)

    remained_distance = update_robots_distances(robots, graph)
    total_time = time.time() - start_time
    if not is_not_finished(robots):
        log.info(f'Finished! {total_time}s, {step_number} steps, {total_moves} moves, {remained_distance} distance')
        root_log.warn('Success!')
        return {'succeed': True, 'total_time': total_time, 'number_of_steps': step_number,
                'number_of_moves': total_moves, 'remained_distance': remained_distance,
                'start_distance': start_distance}
    else:
        log.info(f'Stuck! {total_time}s, {step_number} steps, {total_moves} moves, {remained_distance} distance')
        return {'succeed': False, 'total_time': total_time, 'number_of_steps': step_number,
                'number_of_moves': total_moves, 'remained_distance': remained_distance,
                'start_distance': start_distance}


def main(custom_file=None, dirs=tuple(), do_all=False):
    start_time = time.time()
    metadata = utils.load_metadata()
    for path in dirs:
        files = [file_name for file_name in os.listdir(path) if
                 file_name.endswith('.json') and (
                         file_name not in metadata.keys() or custom_file == file_name or do_all)]
        for file_name in tqdm.tqdm(sorted(files, key=lambda n: os.path.getsize(f'{path}/{n}'))):
            if custom_file and file_name != custom_file:
                continue
            root_log.info(f'Solving {file_name}')
            metadata[file_name] = solve(f'{path}/{file_name}', f'{path.replace("/inputs", "/outputs")}/{file_name}',
                                        DEBUG if custom_file else ERROR)
            utils.write_metadata(metadata)
    log.error(f'Total time: {time.time() - start_time}s')
    log.error(f'Total Success: {len([m for m in metadata.values() if m["succeed"]])}')
    log.error(f'Total Failed: {len([m for m in metadata.values() if not m["succeed"]])}')


if __name__ == "__main__":
    main('small_free_001_10x10_40_40.instance.json',
         ['../tests/inputs', '../tests/inputs/all/manual', '../tests/inputs/all/uniform', '../tests/inputs/all/images'])
    # main(None, ['../tests/inputs'], do_all=True)
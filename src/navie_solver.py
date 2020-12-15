import utils


def calc_robot_next_step(robot, invalid_positions):
    """
    need to calculate shortest path +
    update robot current pos +
    add move to data structure
    """
    go_right = (robot.target_pos[0] - robot.current_pos[0]) > 0
    go_up = (robot.target_pos[1] - robot.current_pos[1]) > 0
    go_left = (robot.target_pos[0] - robot.current_pos[0]) < 0
    go_down = (robot.target_pos[1] - robot.current_pos[1]) < 0
    if go_right:
        right_pos = utils.calc_next_pos(robot.current_pos, 'right')
        if right_pos not in invalid_positions:
            return right_pos, utils.STEP_DIRECTION['right']
    if go_left:
        left_pos = utils.calc_next_pos(robot.current_pos, 'left')
        if left_pos not in invalid_positions:
            return left_pos, utils.STEP_DIRECTION['left']
    if go_up:
        up_pos = utils.calc_next_pos(robot.current_pos, 'up')
        if up_pos not in invalid_positions:
            return up_pos, utils.STEP_DIRECTION['up']
    if go_down:
        down_pos = utils.calc_next_pos(robot.current_pos, 'down')
        if down_pos not in invalid_positions:
            return down_pos, utils.STEP_DIRECTION['down']
    return robot.current_pos, None


def sort_robots(robots):
    return sorted(robots, key=lambda robot: robot.distance)


def update_robots_distances(robots):
    for robot in robots:
        target_pos = robot.target_pos
        current_pos = robot.current_pos
        robot.distance = abs(target_pos[0] - current_pos[0]) + abs(target_pos[1] - current_pos[1])


def move_robot(robot, robot_next_pos, invalid_positions):
    invalid_positions.remove(robot.current_pos)
    robot.current_pos = robot_next_pos
    invalid_positions.add(robot.current_pos)


def is_not_finished(robots):
    return all(robot.current_pos == robot.target_pos for robot in robots)


def solve(infile: str, outfile: str):
    robots, obstacles, name = utils.read_scene(infile)
    invalid_positions = set(obstacles).union(set(robot.current_pos for robot in robots))

    update_robots_distances(robots)
    robots = sort_robots(robots)
    steps = []  # a data structure to hold all the moves for each robot
    step_number = 0
    while not is_not_finished(robots):  # while not all robots finished
        steps.append(dict())
        for robot in robots:  # move each robot accordingly to its priority
            robot_next_pos, robot_step = calc_robot_next_step(robot, invalid_positions)
            move_robot(robot, robot_next_pos, invalid_positions)
            if robot_step:
                steps[step_number][str(robot.index)] = robot_step
        step_number += 1

    # after the algorithm finished, we should write the moves data structure to json file.
    utils.write_solution(steps, name, outfile)


if __name__ == "__main__":
    solve(infile='../tests/inputs/scene_5.json', outfile='../tests/outputs/scene_5.json')


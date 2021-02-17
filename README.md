# CoordinatedMotionPlanning

### Motivation
As part of the annual competition for finding solutions to difficult optimization problems, the following challenge was set in this year:
Given a set of n axis-aligned unit-square robots in the plane,
A set S of n distinct start pixels (unit squares) of the integer grid, and a set T of 
n distinct target pixels of the integer grid .
During each unit of time, each robot can move (at unit speed) in a direction (north, south, east or west) to an adjacent pixel, provided the robot remains disjoint from all other robots during the motions.
The task is to compute a set of feasible trajectories for all n robots, with the trajectory for robot moving it from its current position to its target position.

![alt text](https://github.com/ofekMula/CoordinatedMotionPlanning/blob/master/decription.jpg)


The problem is motivated by questions of multi-object motion planning, such as robot navigation and air traffic control.
The version considered in the Challenge is known to be NP-complete

## High level algorithm :

Each round we choose for each robot what will be the best move for it.
The algorithm is based on the following building blocks:

1. Prioritization between robots (who moves in front of whom)

2. The robot is not allowed to move to the previous slot it was in except in very exceptional cases

3. Learning the board by the robots in motion

## Videos of our solutions:
https://www.youtube.com/watch?v=QF5qkH1iSA0&feature=youtu.be&ab_channel=%D7%90%D7%95%D7%A4%D7%99%D7%A8%D7%98%D7%99%D7%99%D7%91


## Credits
CG:SHOP2021 - the annual computational geometric competition:

https://cgshop.ibr.cs.tu-bs.de/competition/cg-shop-2021/#problem-description

Organized by: Sándor Fekete (TU Braunschweig),
Phillip Keldenich (TU Braunschweig),
Dominik Krupke (TU Braunschweig),
Joseph S. B. Mitchell (Stony Brook University)


import numpy as np
import read_scene
import networkx as nx
import sys


def solve(infile: str, outfile: str):
    scene, name = read_scene.read_scene(infile)
    if len(scene[0]) > 1:
        print("Scene with more than one robot")
        return
    robot = tuple(scene[0][0])
    objective = tuple(scene[1][0])
    obstacles = set(tuple(a) for a in scene[2])

    # Calculate scene bounding box
    all_points = [robot] + [objective] + list(obstacles)
    min_x = min(a[0] for a in all_points)
    max_x = max(a[0] for a in all_points)
    min_y = min(a[1] for a in all_points)
    max_y = max(a[1] for a in all_points)

    grid = [(x, y) for x in range(min_x-1, max_x+2) for y in range(min_y-1, max_y+2)]
    G = nx.Graph()
    G.add_nodes_from(grid)
    for u in G.nodes:
        # Add valid edges
        for x in range(max(min_x - 1, u[0]-1), min(max_x+1, u[0]+1)):
            if x == u[0]:
                for y in range(max(min_y - 1, u[1]-1), min(max_y+1, u[1]+1)):
                    v = (x, y)
                    if v not in obstacles:
                        G.add_edge(u, v)
            else:
                y = u[1]
                v = (x, y)
                if v not in obstacles:
                    G.add_edge(u, v)

    # Find shortest paths
    steps = []
    if nx.has_path(G, robot, objective):
        sp = nx.shortest_path(G, robot, objective)
        steps = [[np.array(sp[i]) - np.array(sp[i-1])] for i in range(1, len(sp))]
    if steps:
        read_scene.write_solution(steps, name, outfile)

if __name__ == "__main__":
    if __name__ == "__main__":
        solve(infile='scene_1.json', outfile='scene_1_sol.json')
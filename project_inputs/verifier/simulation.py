from verifier import Verifier
import sys
from gui.gui import GUI, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor
import read_scene
import numpy as np
from colour import Color

class Simulation:
    gui_robots = None
    gui_objectives = None
    gui_obstacles = None
    verifier: Verifier = None

    def __init__(self, gui_robots, gui_objectives, gui_obstacles, verifier):
        self.gui_robots = gui_robots
        self.gui_objectives = gui_objectives
        self.gui_obstacles = gui_obstacles
        self.verifier = verifier


show_paths = False
# colors = [QtCore.Qt.black, QtCore.Qt.red, QtCore.Qt.blue, QtCore.Qt.green, QtCore.Qt.yellow, QtCore.Qt.magenta, QtCore.Qt.cyan,
#           QtCore.Qt.darkRed, QtCore.Qt.darkBlue, QtCore.Qt.darkGreen, QtCore.Qt.darkYellow, QtCore.Qt.darkMagenta,
#           QtCore.Qt.darkCyan]  # 15 colors

simulation: Simulation = None

eps = 0.04

def unit_square(p):
    p1 = (p[0] + eps, p[1] + eps)
    p2 = (p[0] + 1 - eps, p[1] + eps)
    p3 = (p[0] + 1 - eps, p[1] + 1 -eps)
    p4 = (p[0] + eps, p[1] + 1 - eps)
    return [p1, p2, p3, p4]


def bounding_rect_center(points):
    min_x = min(a[0] for a in points)
    max_x = max(a[0] for a in points)
    min_y = min(a[1] for a in points)
    max_y = max(a[1] for a in points)
    return (max_x + min_x) / 2, (max_y + min_y) / 2


def draw_grid(size):
    for i in range(-size, size):
        gui.add_segment(-size, i, size, i, line_color=QtCore.Qt.lightGray)
        gui.add_segment(i, -size, i, size, line_color=QtCore.Qt.lightGray)


def set_up_scene():
    global simulation
    gui.clear_scene()
    gui.textEdits[0].clear()
    s = gui.get_field(0)
    scene = read_scene.read_scene(s)
    verifier = Verifier(*scene)

    gui_robots = []
    gui_objectives = []
    gui_obstacles = []
    points = []

    draw_grid(100)

    blue = Color("blue")
    colors = list(blue.range_to(Color("red"), len(scene[0])))
    colors = [QColor(color.get_hex()) for color in colors]

    for i, robot in enumerate(scene[0]):
        color = colors[i%len(colors)]
        gui_robots.append(gui.add_polygon(unit_square(robot), line_color=QtCore.Qt.transparent, fill_color=color))
        points.append(tuple(robot))

    for obstacle in scene[2]:
        color = QtCore.Qt.gray
        gui_obstacles.append(gui.add_polygon(unit_square(obstacle), line_color=QtCore.Qt.transparent, fill_color=color))
        points.append(tuple(obstacle))

    for i, objective in enumerate(scene[1]):
        color = colors[i % len(colors)]
        gui_objectives.append(
            gui.add_polygon(unit_square(objective), line_color=QColor(color), fill_color=QtCore.Qt.transparent))
        points.append(tuple(objective))

    simulation = Simulation(gui_robots, gui_objectives, gui_obstacles, verifier)
    center = bounding_rect_center(points)
    gui.graphicsView.translate(center[0], center[1])
    gui.graphicsView.centerOn(center[0], center[1])


def queue_turn_animation(turn):
    global simulation
    robots = simulation.verifier.robots
    gui_robots = simulation.gui_robots
    anims = []
    for i in range(len(turn)):
        anims.append(gui.linear_translation_animation(gui_robots[i], *(robots[i] - turn[i]), *robots[i], duration=500))
        if show_paths:
            gui.add_segment(*(robots[i] - turn[i] + np.array([0.5, 0.5])), *robots[i] + np.array([0.5, 0.5]), line_color=colors[i%len(colors)])
    gui.queue_animation(gui.parallel_animation(*anims))
    gui.queue_animation(gui.pause_animation(200))


def run_simulation():
    global simulation
    s = gui.get_field(1)
    turns = read_scene.read_sol(s, len(simulation.verifier.robots))
    for i, turn in enumerate(turns):
        t = simulation.verifier.execute_turn(turn)
        if t is not None:
            queue_turn_animation(turn)
            if t:
                print("All robots have reached their destinations")
                break
        else:
            print("Invalid commands on turn", i+1)
            break
    report = ""
    report += "Number of turns: " + str(simulation.verifier.turns) + "\n"
    report += "Total number of steps: " + str(simulation.verifier.total_steps) + "\n"
    report += "Step distribution: " + str(simulation.verifier.robot_steps) + "\n"
    gui.textEdits[0].setPlainText(report)
    print(report)

    gui.play_queue()


def getfile():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    if dlg.exec_():
        filenames = dlg.selectedFiles()
        return filenames[0]


def set_scene_field():
    s = getfile()
    if s:
        gui.set_field(0, s)


def set_solution_field():
    s = getfile()
    if s:
        gui.set_field(1, s)


if __name__ == "__main__":
    instance = ""
    solution = ""
    if len(sys.argv) > 1:
        instance = sys.argv[1]
    if len(sys.argv) > 2:
        solution = sys.argv[2]
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.set_program_name("CMP simulation")
    gui.set_logic(0, set_up_scene)
    gui.set_logic(1, run_simulation)
    gui.set_logic(2, set_scene_field)
    gui.set_logic(3, set_solution_field)
    gui.set_button_text(0, "Initialize")
    gui.set_button_text(1, "Run")
    gui.set_button_text(2, "...")
    gui.set_button_text(3, "...")
    gui.set_field(0, instance)
    gui.set_field(1, solution)
    gui.set_label(0, "Input file:")
    gui.set_label(1, "Solution file:")
    gui.set_animation_finished_action(lambda: None)
    gui.MainWindow.show()
    sys.exit(app.exec_())
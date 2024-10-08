import casadi as ca
import numpy as np
import matplotlib.pyplot as plt
from robot_base import RobotBase
from map_world import GlobalMap, LocalMap

if __name__ == "__main__":
    # Initialize the world
    global_map = GlobalMap()
    local_map = LocalMap()
    
    # Initialize the robot
    robot = RobotBase()
    
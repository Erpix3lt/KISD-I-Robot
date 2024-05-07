import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from robot_interface.robot_service import Robot_Service

mqtt = Robot_Service()
position = mqtt.get_pose()
print(position)

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interface.robot_service import Robot_Service
"""
This part is a blank canvas for quick tests and experimantation with the robot itself.
This is not using mockup functionality!!! All the events will be published via MQTT.
"""
mqtt = Robot_Service()
position = mqtt.get_pose()
print(position)

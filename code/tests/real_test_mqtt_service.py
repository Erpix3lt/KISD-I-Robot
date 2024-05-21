import os
import sys
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interface.robot_service import Robot_Service
"""
This part is a blank canvas for quick tests and experimantation with the robot itself.
This is not using mockup functionality!!! All the events will be published via MQTT.
"""
mqtt = Robot_Service() 

mqtt.move_pos('0')

for _ in range(5):
  time.sleep(5)
  print("going to pos: 1")
  mqtt.move_pos('1')
  time.sleep(5)
  print("going to pos: 2")
  mqtt.move_pos('2')

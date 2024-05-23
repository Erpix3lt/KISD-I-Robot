import os
import sys
import time
import ast
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from interface.robot_service import Robot_Service
"""
This part is a blank canvas for quick tests and experimantation with the robot itself.
This is not using mockup functionality!!! All the events will be published via MQTT.
"""
mqtt = Robot_Service() 

class TCPPosition:
    def __init__(self, x, y, z, ax, ay, az):
        self.x = x
        self.y = y
        self.z = z
        self.ax = ax
        self.ay = ay
        self.az = az

preclick = TCPPosition(
    x=0.083575, 
    y=-0.241124, 
    z=0.184729, 
    ax=-1.834565, 
    ay=-2.363311, 
    az=-0.149027
)

click = TCPPosition(
    x=0.083875, 
    y=-0.236864, 
    z=0.177355, 
    ax=-1.824339, 
    ay=-2.351765, 
    az=-0.179668
)



# def extract_joint_values(joint_string):
#     # Find the substring that contains the list
#     start_index = joint_string.find('[')
#     end_index = joint_string.find(']')
    
#     # Extract the substring
#     list_string = joint_string[start_index:end_index+1]
    
#     # Convert the string representation of the list to an actual list
#     joint_values = ast.literal_eval(list_string)
    
#     # Assign the values to respective variables
#     x, y, z, ax, ay, az = joint_values
    
#     return x, y, z, ax, ay, az
mqtt.looking_idle(10)
mqtt.move_towards_count()
mqtt.count(5)

# # mqtt.count(5)

# mqtt.looking_idle(20)








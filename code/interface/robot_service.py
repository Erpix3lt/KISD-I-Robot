from .mqtt_service import Mqtt_Service
import time
import random
import re
from .socket_service import Socket_Service

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

looking_1 = TCPPosition(
    x=-0.314818, 
    y=0.137848, 
    z=0.590017, 
    ax=0.129045, 
    ay=-1.532683, 
    az=-0.10951
)

looking_2 = TCPPosition(
    x=-0.288607, 
    y=0.135958, 
    z=0.581515, 
    ax=0.126539, 
    ay=-1.560673, 
    az=-0.099412
)

looking_3 = TCPPosition(
    x=-0.316104, 
    y=0.09796, 
    z=0.559518, 
    ax=-0.021045, 
    ay=-1.573314, 
    az=-0.246432
)

looking_4 = TCPPosition(
    x=-0.268339, 
    y=0.155232, 
    z=0.555648, 
    ax=0.205781, 
    ay=-1.582979, 
    az=-0.012414
)

looking_tiny_1 = TCPPosition(
    x=-0.215611, 
    y=0.130446, 
    z=0.428001, 
    ax=-2.270743, 
    ay=-0.174517, 
    az=2.030164
)

looking_tiny_2 = TCPPosition(
    x=-0.200955, 
    y=0.132689, 
    z=0.430012, 
    ax=-2.16538, 
    ay=-0.140816, 
    az=2.110851
)

class Robot_Service(Mqtt_Service):
    """
    Service class for controlling a robot using MQTT.
    Inherits from Mqtt_Service class.
    It provides all the detailed functionality for the UR3 arm. 
    Such as get_val, move_pos, move_to_tcp_pos etc..
    """
    def __init__(self) -> None:
        """
        Initialize MQTT service for controlling the robot.
        """
        self.socket_service = Socket_Service()
        print("Init socket service")
        super().__init__()

    def set_cmd(self, body:str ):
        """
        Send a command message to the robot via MQTT.

        Args:
            body (str): Command message body.

        """
        topic:str = "ur3/set/cmd"
        if self.client:
            try:
                self.client.publish(topic, body)
            except Exception as e:
                print("Error publishing MQTT message:", e)
                
    def get_val(self, timeout=0.5) -> str:
        """
        Retrieve a value from the robot via MQTT with a given timeout.

        Args:
            timeout (float): Timeout value in seconds.

        Returns:
            str: Value retrieved from the robot as a string, or None if timeout is reached.
        """
        return self.subscribe('ur3/get/val', timeout)
  
    def move_pos(self, pos:str):
        """
        Set the robot to the specified position.

        Args:
            pos (str): Position identifier.

        """
        body = "movePos:" + pos
        self.set_cmd(body)
        
    def move_j(self):
        """
        Move the robot.
        """        
        body = "movejPose"
        self.set_cmd(body)
        
    def get_pose(self) -> str:
        self.set_cmd('getPose')
        return self.get_val()
    
    def get_joints(self) -> str:
        self.set_cmd('getJoints')
        return self.get_val()
        
    def set_axis(self, axis: str, value: float):
        """
        Set individual axes values for x, y, z, ax, ay, az.

        Args:
            axes (str): The axes to be used ('x', 'y', 'z', 'ax', 'ay', or 'az').
            value (float): Point in space.

        """
        valid_axes = ["x", "y", "z", "ax", "ay", "az"]
        
        if axis not in valid_axes:
            print("Invalid axes argument. It should be one of 'x', 'y', 'z', 'ax', 'ay', or 'az'.")
            return
        
        body = axis + ":" + str(value)
        self.set_cmd(body)
        
    def move_to_tcp_pos(self, x: float, y: float, z: float, ax: float = None, ay: float = None, az: float = None, blend: float = None, time: float = None):
        """
        Move to the specified TCP (Tool Center Point) position.

        Args:
            x (float): X-coordinate.
            y (float): Y-coordinate.
            z (float): Z-coordinate.
            ax (float, optional): Rotation around X-axis.
            ay (float, optional): Rotation around Y-axis.
            az (float, optional): Rotation around Z-axis.
            blend (float, optional): Blend radius.
            time (float, optional): Time to reach the position.
        """
        # Prepare the base position string with x, y, z
        position = f"{x}, {y}, {z}"
        
        # Append optional rotation values if provided
        if ax is not None:
            position += f", {ax}"
        if ay is not None:
            position += f", {ay}"
        if az is not None:
            position += f", {az}"
        
        # Create the final command string
        cmd = f"pose: {position}"
        
        # Set the position command
        self.set_cmd(cmd)
        
        # Handle additional optional parameters
        if time is not None:
            self.set_cmd(f'time:{time}')
        if blend is not None:
            self.set_cmd(f'blend:{blend}')
        
        # Issue the move command
        self.set_cmd("movejPose")
        
    def extract_pose_values(self, pose_string):
        values = re.findall(r"[-+]?\d*\.\d+|\d+", pose_string)
        values = [float(value) for value in values]
        x, y, z, ax, ay, az = values[:6]
        return x, y, z, ax, ay, az
   
    def assert_has_reached_tcp_pos(self, x: float, y: float, z: float, threshold: float = 0.02):
        """
        Asserts the current tcp pos with a desired pos within a given threshold.

        Args:
            x (float): Desired x position.
            y (float): Desired y position.
            z (float): Desired z position.
            threshold (float): Allowable threshold for position comparison.

        Returns:
            bool: True if the pos is within the threshold of the desired pos. False otherwise.
        """
        try:
            currentPosition = self.get_pose()
            if currentPosition is not None:
                curr_x, curr_y, curr_z, curr_ax, curr_ay, curr_az = self.extract_pose_values(currentPosition)
                print("Current Difference:", x - curr_x, y - curr_y, z - curr_z) 
                # Compare each coordinate with the threshold
                if abs(curr_x - x) <= threshold and abs(curr_y - y) <= threshold and abs(curr_z - z) <= threshold:
                    return True
                else:
                    return False
            else: 
                print("CURRENT WAS NONE:")
                return False
        except Exception as e:
            print("Error asserting the current tcp values:", e)
            return False
        
    def interpret(self):
        self.set_cmd("interpret")

    ########################
    # Abstract functions   #
    ########################
    
    def move_towards_count(self):
        self.socket_service.movejPose(preclick.x, preclick.y, preclick.z, preclick.ax, preclick.ay, preclick.az,)
        #while not self.assert_has_reached_tcp_pos(preclick.x, preclick.y, preclick.z):
            

    def count(self, n: int):
        for _ in range(n):
            self.socket_service.movejPose(click.x, click.y, click.z, click.ax, click.ay, click.az)
            self.socket_service.movejPose(preclick.x, preclick.y, preclick.z, preclick.ax, preclick.ay, preclick.az)

            
    def looking_idle(self, duration: int):
        """
        Move to the looking_tiny_2 position with minimal randomness for the specified duration.
        
        Args:
            duration (int): Total time to keep moving through the positions.
            wait_in_seconds (float): Wait time between moves.
            time_per_move (float): Time to reach each position.
        """
        idle_1 = TCPPosition(
            x=-0.422448, 
            y=-0.125552, 
            z=0.413353, 
            ax=-1.15982, 
            ay=-1.402881, 
            az=0.802694
        )
        
        idle_2 = TCPPosition(
            x=-0.42805,
            y=-0.104786,
            z=0.413398, 
            ax=-1.189674, 
            ay=-1.369338,
            az=0.768508
        )       
        
        idle_3 = TCPPosition(
            x=-0.422779,
            y=--0.099871,
            z=0.468245, 
            ax=-1.232925,
            ay=-1.247152,
            az=0.925764
        ) 
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            self.socket_service.movejPose(idle_1.x, idle_1.y, idle_1.z, idle_1.ax, idle_1.ay, idle_1.az)
            time.sleep(.8)

            self.socket_service.movejPose(idle_2.x, idle_2.y, idle_2.z, idle_2.ax, idle_2.ay, idle_2.az)
            time.sleep(.8)

            self.socket_service.movejPose(idle_3.x, idle_3.y, idle_3.z, idle_3.ax, idle_3.ay, idle_3.az)
            time.sleep(.8)

            self.socket_service.movejPose(idle_2.x, idle_2.y, idle_2.z, idle_2.ax, idle_2.ay, idle_2.az)
            time.sleep(.8)
            print("IDLING")

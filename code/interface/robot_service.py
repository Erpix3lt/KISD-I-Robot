from .mqtt_service import Mqtt_Service
import time
import random

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
                
    def get_val(self, timeout=8) -> str:
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

        
    def assert_has_reached_tcp_pos(self, x: float, y: float, z: float, ax: float = None, ay: float = None, az: float = None,):
        """
        Asserts the current tcp pos with a desired pos

        Args:
            Provide desired pos values

        Returns:
            True if the pos is equal to the desired pos. False if it is unequal or it failed.
        """
        try:
            x_str = str(x)
            y_str = str(y)
            z_str = str(z)
            ax_str = str(ax)
            ay_str = str(ay)
            az_str = str(az)
            
            pose_string = f"pose:p[{x_str}, {y_str}, {z_str}, {ax_str}, {ay_str}, {az_str}]"
            currentPosition = self.get_pose()

            if currentPosition == pose_string:
                return True
            else:
                return False
        except Exception as e:
            print("Error asserting the current tcp values:", e)
            return False

    ########################
    # Abstract functions   #
    ########################
    
    def move_towards_count(self):
        self.move_to_tcp_pos(preclick.x, preclick.y, preclick.z, preclick.ax, preclick.ay, preclick.az, time=0.3)
        time.sleep(2)

    def count(self, n: int, wait_in_seconds: float = 2, time_per_move = 0.2):
        for _ in range(n):
            self.move_to_tcp_pos(click.x, click.y, click.z, click.ax, click.ay, click.az, time=time_per_move)
            self.move_to_tcp_pos(preclick.x, preclick.y, preclick.z, preclick.ax, preclick.ay, preclick.az, time=time_per_move)
            time.sleep(wait_in_seconds)
            print("CLICKING")
            
    def looking_idle(self, duration: int, wait_in_seconds: float = 0.8, time_per_move: float = 1.8):
        """
        Move to the looking_tiny_2 position with minimal randomness for the specified duration.
        
        Args:
            duration (int): Total time to keep moving through the positions.
            wait_in_seconds (float): Wait time between moves.
            time_per_move (float): Time to reach each position.
        """
        looking_tiny_2 = TCPPosition(
            x=-0.200955, 
            y=0.132689, 
            z=0.430012, 
            ax=-2.16538, 
            ay=-0.140816, 
            az=2.110851
        )
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            rand_x = looking_tiny_2.x + random.uniform(-0.01, 0.01)
            rand_y = looking_tiny_2.y + random.uniform(-0.01, 0.01)
            rand_z = looking_tiny_2.z + random.uniform(-0.01, 0.01)
            
            # Optional: Add randomness to rotations as well
            rand_ax = looking_tiny_2.ax + random.uniform(-0.01, 0.01)
            rand_ay = looking_tiny_2.ay + random.uniform(-0.01, 0.01)
            rand_az = looking_tiny_2.az + random.uniform(-0.01, 0.01)
            
            self.move_to_tcp_pos(rand_x, rand_y, rand_z, rand_ax, rand_ay, rand_az, time=time_per_move)
            time.sleep(wait_in_seconds)
            print("IDLING")

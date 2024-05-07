from .mqtt_service import Mqtt_Service

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
                
    def get_val(self, timeout=5) -> str:
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
        Move the robot to the specified position.

        Args:
            pos (str): Position identifier.

        """
        body = "movePos:" + pos
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
        self.set_axis("x", x)
        self.set_axis("y", y)
        self.set_axis("z", z)
        
        if ax is not None:
            self.set_axis("ax", ax)
        if ay is not None:
            self.set_axis("ay", ay)
        if az is not None:
            self.set_axis("az", az)
           
        if time is not None:
            self.set_cmd('time:' + str(time))
            
        if blend is not None:
            self.set_cmd('blend:' + str(time))
            
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


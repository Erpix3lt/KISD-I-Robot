import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import time

class Mqtt_Service: 
    """
    MQTT service class for sending commands to a Universal Robots UR3 robot arm.
    """
    def __init__(self) -> None:
        """
        Initialize MQTT service with environment variables.
        """
        load_dotenv() 
        self.host = os.getenv("MQTT_HOST")
        self.user = os.getenv("MQTT_USER")
        self.password = os.getenv("MQTT_PASSWORD")
        self.port = int(os.getenv("MQTT_PORT", 1883))
  
    def establish_connection(self):
        """
        Establish a connection to the MQTT broker.

        Returns:
            mqtt.Client: MQTT client object if connection is successful, None otherwise.
        """
        try:
            client = mqtt.Client(protocol=mqtt.MQTTv5)
            client.username_pw_set(username=self.user, password=self.password)
            client.connect(self.host, port=self.port)
            return client
        except Exception as e:
            print("Error establishing MQTT connection:", e)
            return None
  
    def disconnect_connection(self, client):
        """
        Disconnect the MQTT client from the broker.

        Args:
            client (mqtt.Client): MQTT client object.
        """
        try:
            client.disconnect()
        except Exception as e:
            print("Error disconnecting MQTT connection:", e)

    def send_command(self, body:str ):
        """
        Send a command message to the robot via MQTT.

        Args:
            body (str): Command message body.

        """
        topic:str = "ur3/set/cmd"
        client = self.establish_connection()
        if client:
            try:
                client.publish(topic, body)
            except Exception as e:
                print("Error publishing MQTT message:", e)
            finally:
                self.disconnect_connection(client)
                
    def get_value(self, body: str, timeout: float = 2) -> str:
        """
        Retrieve a value from the robot via MQTT with a timeout.

        Args:
            body (str): Body of the request.
            timeout (float): Timeout value in seconds.

        Returns:
            str: Value retrieved from the robot as a string, or None if timeout is reached.
        """
        topic = "ur3/get/val"
        value = None

        client = self.establish_connection()
        if client:
            try:
                client.subscribe(topic)
                client.publish(topic, body)
                value = self.wait_for_response(timeout)
            except Exception as e:
                print("Error retrieving value from MQTT:", e)
            finally:
                self.disconnect_connection(client)
        return value

    def move_to_pos(self, pos:str):
        """
        Move the robot to the specified position.

        Args:
            pos (str): Position identifier.

        """
        body = "movePos:" + pos
        self.send_command(body)
        
    def get_Pose(self) -> str:
        return self.get_value("getPose")
    
    def get_Joints(self) -> str:
        return self.get_value("getJoints")
        
    def set_individual_axes(self, axes: str, value: float):
        """
        Set individual axes values for x, y, z, ax, ay, az.

        Args:
            axes (str): The axes to be used ('x', 'y', 'z', 'ax', 'ay', 'az').
            value (float): Point in space.

        """
        valid_axes = ["x", "y", "z", "ax", "ay", "az"]
        
        if axes not in valid_axes:
            print("Invalid axes argument. It should be one of 'x', 'y', 'z', 'ax', 'ay', or 'az'.")
            return
        
        body = axes + ":" + str(value)
        self.send_command(body)
        
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
        self.set_individual_axes("x", x)
        self.set_individual_axes("y", y)
        self.set_individual_axes("z", z)
        
        if ax is not None:
            self.set_individual_axes("ax", ax)
        if ay is not None:
            self.set_individual_axes("ay", ay)
        if az is not None:
            self.set_individual_axes("az", az)
           
        if time is not None:
            self.send_command('time:' + str(time))
            
        if blend is not None:
            self.send_command('blend:' + str(time))
            
        self.send_command("moveJ")
        
    def wait_for_response(self, timeout: float) -> str:
        """
        Wait for a response from MQTT with a timeout.

        Args:
            timeout (float): Timeout value in seconds.

        Returns:
            str: Value retrieved from MQTT as a string, or None if timeout is reached.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            if hasattr(self, 'response'):
                return str(self.response)
        else:
            print("Timeout reached. No response received.")
            return None
        
    def assert_has_reach_tcp_pos(self, x: float, y: float, z: float, ax: float = None, ay: float = None, az: float = None,):
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

            currentPosition = self.get_Pose()

            if currentPosition == pose_string:
                return True
            else:
                return False
        except Exception as e:
            print("Error asserting the current tcp values:", e)
        finally:
            return False

        
        


import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv
import time

class Mqtt_Service: 
    """
    MQTT service class for sending commands to a Universal Robots UR3 robot arm.
    It is housing all the basic funtionality to communicate via MQTT, such as connect, disconnect
    subscibe and the on_message callback.
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
        self.client = self.connect()
        self.subscribed_value = None
        
    def subscribe(self, topic: str, timeout=5):
        """
        Private function retrieving a value by listening to the given topic.

        Args:
            topic (str): MQTT topic to subscribe to.
            timeout (float): Timeout value in seconds.

        Returns:
            str: Value retrieved from the robot as a string, or None if timeout is reached.
        """
        try:
            self.client.subscribe(topic)
            self.client.on_message = self.on_message
            self.client.loop_start()
            time.sleep(timeout)
            self.client.loop_stop()
            return self.subscribed_value
        except Exception as e:
            print("Error subscribing to MQTT topic:", e)
            return None

    def on_message(self, client, userdata, message):
        """
        Private callback function to handle incoming MQTT messages.
        """
        try:
            self.subscribed_value = str(message.payload.decode("utf-8"))
        except Exception as e:
            print("Error handling MQTT message:", e)

  
    def connect(self):
        """
        Establish a connection to the MQTT broker.

        Returns:
            mqtt.Client: MQTT client object if connection is successful, None otherwise.
        """
        try:
            self.client = mqtt.Client(protocol=mqtt.MQTTv5)
            self.client.username_pw_set(username=self.user, password=self.password)
            self.client.connect(self.host, port=self.port)
            return self.client
        except Exception as e:
            print("Error establishing MQTT connection:", e)
            return None
  
    def disconnect(self):
        """
        Disconnect the MQTT client from the broker.

        Args:
            client (mqtt.Client): MQTT client object.
        """
        try:
            self.client.disconnect()
        except Exception as e:
            print("Error disconnecting MQTT connection:", e)
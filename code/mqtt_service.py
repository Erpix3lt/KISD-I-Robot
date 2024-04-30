import paho.mqtt.client as mqtt

class Mqtt_Service: 

  def __init__(self) -> None:
    # MQTT broker credentials
    self.host = "192.168.0.165"
    self.user = ""
    self.password = ""
    self.port = 1883
  
  def establish_connection(self):
      try:
          client = mqtt.Client(protocol=mqtt.MQTTv5)
          client.username_pw_set(username=self.user, password=self.password)
          client.connect(self.host, port=self.port)
          return client
      except Exception as e:
          print("Error establishing MQTT connection:", e)
          return None
  
  def disconnect_connection(self, client):
      try:
          client.disconnect()
      except Exception as e:
          print("Error disconnecting MQTT connection:", e)

  def send_command(self, topic:str, body:str):
      client = self.establish_connection()
      if client:
          try:
              client.publish(topic, body)
          except Exception as e:
              print("Error publishing MQTT message:", e)
          finally:
              self.disconnect_connection(client)

  def move_to_pos(self, pos:str):
     body = "movePos:" + pos
     self.send_command("ur3/set/cmd", body)

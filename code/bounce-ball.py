from vpython import *
import paho.mqtt.client as mqtt

# MQTT broker credentials
host = "urpi.local"
user = "urpi"
password = "urpi"
port = 1883

# Function to establish MQTT connection and publish the command
def send_command():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username=user, password=password)
    client.connect(host, port=port)
    client.publish("ur3/set/cmd", "x:0.2")
    client.publish("ur3/set/cmd", "movej")
    client.disconnect()

side = 4.0
wall_thickness = 0.3
side_two = 2 * side - wall_thickness
side_three = 2 * side + wall_thickness

ball = sphere(color=color.green, radius=0.4, make_trail=True, retain=200)
ball.mass = 1.0
ball.p = vector(-0.15, -0.23, +0.27)

side = side - wall_thickness * 0.5 - ball.radius

speed = 0.2

   
send_command()

while True:
    rate(100)
    print("Position: ", ball.pos)
    ball.pos = ball.pos + (ball.p / ball.mass) * speed
    if not (side > ball.pos.x > -side):
        ball.p.x = -ball.p.x
    if not (side > ball.pos.y > -side):
        ball.p.y = -ball.p.y
    if not (side > ball.pos.z > -side):
        ball.p.z = -ball.p.z
    

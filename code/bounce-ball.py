from vpython import *
from robot_interface.robot_service import Robot_Service
import sys

side = 4.0
wall_thickness = 0.3
side_two = 2 * side - wall_thickness
side_three = 2 * side + wall_thickness

ball = sphere(color=color.green, radius=0.4, make_trail=True, retain=200)
ball.mass = 1.0
ball.p = vector(-0.15, -0.23, +0.27)

side = side - wall_thickness * 0.5 - ball.radius

speed = 0.2

robot_service = Robot_Service()

try:
    while True:
        rate(100)
        ball.pos = ball.pos + (ball.p / ball.mass) * speed
        if not (side > ball.pos.x > -side):
            robot_service.move_to_tcp_pos(ball.pos.x, ball.pos.y, ball.pos.z)
            ball.p.x = -ball.p.x
        if not (side > ball.pos.y > -side):
            robot_service.move_to_tcp_pos(ball.pos.x, ball.pos.y, ball.pos.z)
            ball.p.y = -ball.p.y
        if not (side > ball.pos.z > -side):
            robot_service.move_to_tcp_pos(ball.pos.x, ball.pos.y, ball.pos.z)
            ball.p.z = -ball.p.z

except KeyboardInterrupt:
    print("Script interrupted. Disconnecting MQTT...")
finally:
    robot_service.disconnect()

sys.exit(0)

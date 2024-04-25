# I,Robot

## References

- Script manual: https://s3-eu-west-1.amazonaws.com/ur-support-site/115824/scriptManual_SW5.11.pdf

## How to run the script

Create a new env: `python3 -m venv path/to/venv`

Install all dependencies: `path/to/venv/bin/pip install vPython`& `path/to/venv/bin/pip install paho-mqtt`

Run the script via: `path/to/venv/bin/python bounce-ball.py`


## Learnings
- p in front of list returns position
- get_actual_tcp_pose() returns actual position
- ur3/set/cmd - getJoints to return position in MQTT


## To Do
- Define global variable of myPose, so changes to variables stay after restarting program
- Calculate bouncing ball box

# I,Robot

## References

- Script manual: https://s3-eu-west-1.amazonaws.com/ur-support-site/115824/scriptManual_SW5.11.pdf

## How to run the script

Create a new env: `python3 -m venv env_i_robot`

Activate the env: `source env_i_robot/bin/activate``

Now we can use python and pip as usual.

Install all dependencies: `pip install vPython`& `pip install paho-mqtt`

Run the script via: `python3 bounce-ball.py`

Type `exit` in the venv to exit.


## How to run UR3 virtual box
- download and install https://www.oracle.com/virtualization/technologies/vm/downloads/virtualbox-downloads.html
- unzip and run  https://s3-eu-west-1.amazonaws.com/ur-support-site/213149/URSim_VIRTUAL-5.12.6.1102099.rar

## Learnings
- p in front of list returns position
- get_actual_tcp_pose() returns actual position
- ur3/set/cmd - getJoints to return position in MQTT


## To Do
- Define global variable of myPose, so changes to variables stay after restarting program
- Calculate bouncing ball box
- [x] get Simulation running

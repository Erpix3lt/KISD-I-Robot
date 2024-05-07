# I,Robot

## References

- Script manual: https://s3-eu-west-1.amazonaws.com/ur-support-site/115824/scriptManual_SW5.11.pdf

## How to run the script

Create a new env: `python3 -m venv env_i_robot`

Activate the env: `source env_i_robot/bin/activate`

Now we can use python and pip as usual.

Install all dependencies: `pip install vPython`& `pip install paho-mqtt` `pip install python-dotenv`

Copy the .env.template file and name it .env, fill in all connection details. The default port is 1883.

Run the script via: `python3 bounce-ball.py`

Type `exit` in the venv to exit.


## How to run UR3 virtual box
- download and install https://www.oracle.com/virtualization/technologies/vm/downloads/virtualbox-downloads.html
- unzip and run  https://s3-eu-west-1.amazonaws.com/ur-support-site/213149/URSim_VIRTUAL-5.12.6.1102099.rar

## Learnings
- p in front of list returns position
- get_actual_tcp_pose() returns actual position
- ur3/set/cmd - getJoints to return position in MQTT

## Update Raspberry and UR Simulation
### Raspberry
- Login credentials are **USERNAME: urpi** and **PW: urpi**
- navigate to mqtt-ur3-bridge
- Delete current changes -> `git stash`
- Pull all the newest changes -> `git pull´
- restart the raspberry pi

### UR Simulation
- Navigate to program files folder (storing our urscript files)
- download the newest version from urscript folder https://gitlab.rlp.net/kitegg/public/kisd/mqtt-ur3-bridge/-/tree/auto-backup/src/urscript/auto-backup/mqtt-ur3-bridge?ref_type=heads

## To Do
- Define global variable of myPose, so changes to variables stay after restarting program
- Calculate bouncing ball box
- [x] get Simulation running

## UR3 IMPORTANT!
- SHARED FOLDER: /media/sf_robot-project/mqtt-ur3-bridge/src/urscript/auto-backup/mqtt-ur3-bridge
- UR3 PROGRAMM FOLDER: Desktop > ProgramsUr3 - /home/ur/ursim-current/programs.UR3

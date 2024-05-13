# I,Robot

## References
- Script manual: https://s3-eu-west-1.amazonaws.com/ur-support-site/115824/scriptManual_SW5.11.pdf

## How to run the script
Create a new env: `python3 -m venv _env_i_robot`

Activate the env: `source _env_i_robot/bin/activate`

Now we can use python and pip as usual.

Install all dependencies: `pip install -r requirements.txt`

Copy the .env.template file and name it .env, fill in all connection details. The default port is 1883.

Run the Bounce Ball script via: `python3 bounce-ball.py`

To run the Detection script into the detection folder: `cd detection`
and run: `python3 detection.py`

Type `exit` in the venv to exit.

## How to run the detection script?
## Object Detection
*Example taken from: https://medium.com/@KaziMushfiq1234/object-detection-using-yolov5-from-scartch-with-python-computer-vision-cfb6b65f540b*

Detection of object through the use of the YOLOv5 model. Target boxes are drawn using OpenCv

If yo want to analyse custom images enter them as a path.

## Architecture
Inside the code folder there a the following subdirectories: interface, tests. Alongside is the main file bounce_ball.py

**interface** The goal of the interface file is to provide all the basic functionality to communicate with the robot. 
There will also be additional functionality and helper functions.

**tests** The test folder contains both mockup and real-world tests.

**bounce_Ball.py** As of now this is our main file, it simulates a bouncing ball, sending the simulated positions to the robot itself.

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

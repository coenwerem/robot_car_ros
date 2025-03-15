# robot_car_ros
ROS(1) Melodic package for range-based obstacle avoidance on a diff-drive ground vehicle. Distance values from a basic ranging sensor (HC-SR04) are published via a custom distance message type (i.e., `ultRangerData.msg`) via the `ultrasonic_sensor.py` node. The `motor_driver.py` node, on the other hand, contains motion primitives and implements collision avoidance using these primitives by subscribing to the `ultrasonic_sensor.py` node and sending appropriate motor commands via the L298N Motor Driver installed on the robot (as ROS messages of type `motorDriver.msg`) that enable corresponding GPIO pins on the robot's single board computer (a Raspberry Pi 3).

## Dependencies and ROS-Hardware Configuration
These instructions assume you have a working ROS installation (preferably ROS Melodic) on a PC running Ubuntu 18.04. It also assumes a similar hardware (HC-SR04-Rpi-L298N) setup as in the above, but the code can easily be adapted to other setups by appropriately modifying the necessary files or creating scripts, message types, or services of your own. We do not use any ROS packages that aren't available in a barebones or desktop ROS installation; you will however need to install the [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) Python library (if you're using an RPi SBC) with a Python version of at least 3.5+ installed on the SBC.

## Installation and Usage
0. Create a ROS workspace if you don't have one already.
1. Clone the repo in the following directory within your ROS workspace: `<path-to-your-ros-workspace>/src/`.
2. Run `catkin_make` in the parent directory of `src` in the above path.
3. Source your ROS installation.
4. Run `roslaunch robot_car_ros robot_car_teleop.launch`. 

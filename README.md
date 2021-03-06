# Olin Aquatic Robotic Systems

Git repository for the Olin Aquatic Robotic Systems team. Learn how to do things in our [wiki](https://github.com/olin-robotic-sailing/oars-roboboat/wiki).

For information about our team, blog updates and more, visit our website at [olinaquabots.com](https://www.olinaquabots.com/).

# Setting up your computer

In order to run OARS code, you need the following things setup on your computer:

1. [Ubuntu](http://howtoubuntu.org/how-to-install-ubuntu-14-04-trusty-tahr) (14.04 highly recommended)
    * test by running `lsb_release -a` in a terminal
2. [ROS](http://wiki.ros.org/indigo/Installation/Ubuntu) (indigo recommended)
    * test by running `rosversion -d` in a terminal
3. A properly-configured [catkin workspace](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)
    * test by running `echo $ROS_PACKAGE_PATH` in a terminal. 
The result should include */home/yourname/catkin_ws/src*
    * If this fails, go to [Appendix A](#appendix-a-getting-your-catkin_ws-setup) to debug and fix it.
4. [git](https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-14-04#how-to-install-git-with-apt) (any version fine)
    * test by running `git --version` in a terminal
5. [V-REP](http://www.coppeliarobotics.com/downloads.html) (educational version, ≥3.3.2)
    * test by running `a command that is yet to be determined` in a terminal
6. the [oars-roboboat](https://github.com/olin-robotic-sailing/oars-roboboat) git repository in your catkin_ws/src folder
    * test by running `roscd oars_pkg` in a terminal
7. All of the dependencies of the oars packages
* test by running 
```
rosdep update
rosdep --ignore-src check --from-paths $(rospack find oars_pkg)/..
```

* fix by running 
```
sudo apt-get update
rosdep --ignore-src install --from-paths $(rospack find oars_pkg)/..
```

# Running the Code

## Jankboat
1. Turn eveything on (e-stop can remain off)
2. Connect several times via SSH
3. Run relevant scripts on boat
   * `roscore`
   * `roslaunch oars_pkg core.launch`
   * `rosrun oars_pkg course_tf_handler.py _config:=courses/sample_course.json`
   * When you're ready: `rosrun oars_pkg planner.py test1`
4. Setup your computer with ROS_IP, ROS_MASTER_URI, and then...
   * `roslaunch oars_pkg joystick.launch`

## Tugboat

1. Turn the tugboat on

    * The Raspberry Pi should be powered from a USB power bank

2. Connect to the tugboat via SSH

    * Connect to the `OLIN-ROBOTICS` WiFI network (password `R0B0TS-RULE`)

    * Visit [https://7a7b657d70.dataplicity.io/](https://7a7b657d70.dataplicity.io/) and find the "inet addr" starting with 192.168.\**.\**

    * In Terminal, connect to the Raspberry Pi using the command
`ssh pi@192.168.**.**` (with the IP address from above)

        1. The password is `raspberry`

3. Update the code on the tugboat to match what you want to test

    * *in the ssh session*

    * `roscd oars_pkg`

    * `git checkout master` (or whatever branch you are working on)

    * `git pull`

4. Run the code on the boat computer (over SSH)

    * In one tab: `roscore`

    * In another tab, launch one of the launch files beginning with `app_`. These correspond to different modes of operation (e.g. piloting Jankboat
1 around obstacle course A, piloting the tugboat in search of an underwater sound's source). For example, run `roslaunch oars_pkg app_tugboat.launch` to pilot the tugboat.

5. (Optional) Use a joystick to manually control the boat. Note: All of these commands should be run on **your computer**, not on the boat (via SSH).

    a) Plug in the controller to your computer via USB

    b) Tell your computer that a ROS master is running on the tugboat:
`export ROS_MASTER_URI=http://<tugboat_ip_address>:11311`

    c) Tell ROS what your IP address is: `export ROS_IP=<your_ip_address>`

    d) Launch the necessary nodes: `roslaunch oars_pkg joystick.launch`

    * If you're running into trouble, make sure your computer can see the joystick by running `ls /dev/input/js*`. (There may be multiple `js#` devices
on your computer, so you might want to try disconnecting the joystick, running the aforementioned command, plugging the joystick back in, and running the command again to make sure a new device showed up.)

    * If the joystick isn’t `js0`, run `roslaunch oars_pkg joystick.launch dev:=/dev/input/js#` (where the `#` is replaced by the correct number).




# Appendix A: Getting your catkin_ws setup

## Step 1: Do you have a catkin_ws folder?

In a terminal type `cd ~/catkin_ws/src`

* If it works, you have a catkin_ws folder already, continue to Step 2

* If it doesn’t work, follow the instructions [here](http://wiki.ros.org/catkin/Tutorials/create_a_workspace), then continue to Step 2

## Step 2: Make your catkin_ws folder the default ROS location

In a terminal, type `gedit ~/.bashrc`

In the resulting text file, add the following two lines to the bottom of the file, if they aren’t there:

<table>
  <tr>
    <td>source /opt/ros/indigo/setup.bash
source ~/catkin_ws/devel/setup.bash</td>
  </tr>
</table>


This file is loaded every time you open a terminal, so it stores the "default" location of your catkin workspace. Any code in the ~/catkin_ws/src directory will now be useable by ROS (once you close and reopen your terminal)

""" 
This example brings the robot's arm to the start_frame and interpolates to the end_frame 
Here we focus on how to use the function move_cartesian_frame_linear_interpolation under the robot class

Class: robot.py
Method: move_cartesian_frame_linear_interpolation(self, abs_frame, speed)
Method: open_gripper(degree)
Dependencies: tfx / robot / numpy

Input param:  
1st) abs_frame 		-> The frame of the end position expressed as a list type. (abs_frame must be a tfx.pose object)

2nd) speed 		    -> (float) type if cubic interpolation is False

3rd) degree         -> The degree you want to open the gripper arm to

Explaination:

- This function takes you through the basics of using the robot API commands.
    - We start with the opening and closing of the gripper
    - Refer to functions open_gripper(degree) and close_gripper() 

    - We then move on to using 2 interpolation techniques offered
    - Refer to move_cartesian_frame_linear_interpolation(abs_frame, speed) and move_cartesian_frame(abs_frame)    

    - The function takes in an absolute frame in catresian space and applies SLERP interpolation to bring it from its current position to the position
    that is specified by the user in abs_frame.

    - Vector interpolation is done linearly in a straight line from the start to end points
    - Rotation is done using quaternion SLERP function under the tfx.transformations.quaternion_slerp method

    - We calculate the vector norm of the start and end points and divide into segments based on 1 interval per 0.1 mm of distance travelled
"""

import time
import numpy as np
import robot
import sys
import tfx

def Interpolate(robotname):
    r = robot.robot(robotname)

    # Open and close gripper 
    print("Starting gripper opening and closing")
    r.open_gripper(80)
    time.sleep(0.1)
    r.close_gripper()

    # Using move_cartesian_linear_interpolate
    # Move to a different cartesian and rotation pose
    start_pose = r.get_current_cartesian_position()

    pose1 = r.get_current_cartesian_position()
    pose1.position.y -= 0.03
    end_pose = tfx.pose(pose1.as_tf()*tfx.transform(tfx.rotation_tb(30, -60, 30)))

    print("Starting move_cartesian_frame_linear_interpolation")
    r.move_cartesian_frame_linear_interpolation(start_pose, 0.01)
    time.sleep(2)
    r.move_cartesian_frame_linear_interpolation(end_pose, 0.01)
    time.sleep(2)
    r.move_cartesian_frame_linear_interpolation(start_pose, 0.01)

    # Using move_cartesian_frame
    print("Starting move_cartesian_frame")
    r.move_cartesian_frame(start_pose, interpolate=True)
    time.sleep(2)
    r.move_cartesian_frame(end_pose, interpolate=True)
    time.sleep(2)
    r.move_cartesian_frame(start_pose, interpolate=True)

    print start_pose
    print end_pose

    # Tutorial ends

if __name__ == '__main__':
    """Here will check if we are given the name of the robot arm or not, if we are we run Interpolate()"""
    """ Expected inputs are robot's arm """

    if (len(sys.argv) == 2):
        raw_input("The dvrk arm will now move. Please ensure that there not obstacles in a 1cm cube around the arm. Press any key to continue")
        Interpolate(sys.argv[1])
    else:
        print sys.argv[0] + ' requires one argument, i.e. name of dVRK arm'



#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
listen the end effecotr transform and recored the pose info ini csv file
"""
"""
BUGS here:
1) getch() will wait untill key press happen,
2) keyboard module must be used as root, where ROS env is not accessible 
3) well, callback, rospy.is_shutdown doesn't accept arguments,
"""


# import roslib
# roslib.load_manifest('learning_tf')
import rospy
# import math
import tf
import pandas as pd
# import keyboard
import sys, termios, tty, os, time

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == '__main__':
    rospy.init_node('tiago_ee_listener')

    listener = tf.TransformListener()
    pose_data = []  
    rate = rospy.Rate(10.0)
    while True:
        try:
            # trans is list [x y z], rot is a quat [x y z w]
            (trans,rot) = listener.lookupTransform('/base_footprint', '/arm_7_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        # print 'trans', trans
        print 'rot: ', rot
        tempt = trans + rot
        pose_data.append(tempt)

        if getch() == 'q':#if key 'q' is pressed 
            print('Record is over!')
            break#finishing the loop
        else:
            pass

        rate.sleep()

    my_df = pd.DataFrame(pose_data)
    file_name = raw_input("Please input the CSV file name:")
    my_df.to_csv(file_name, index=False, header=['x', 'y', 'z', 'q_x', 'q_y', 'q_z', 'w'])

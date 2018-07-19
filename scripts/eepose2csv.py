#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
listen the end effecotr transform and recored the pose info ini csv file
"""

# import roslib
import rospy
# import math
import tf
import pandas as pd
import readchar


if __name__ == '__main__':
    rospy.init_node('tiago_ee_listener')
    listener = tf.TransformListener()
    pose_data = []  
    rate = rospy.Rate(10.0)
    time = 0.0
    try:
        while True:
            try:
                # trans is list [x y z], rot is a quat [x y z w]
                (trans,rot) = listener.lookupTransform('/base_footprint', '/arm_7_link', rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                continue

            # print 'trans', trans
            print 'rot: ', rot
            tempt = [time] + trans + rot
            pose_data.append(tempt)
            rate.sleep()
            time += 0.1 # update time
    except KeyboardInterrupt:
        pass

    my_df = pd.DataFrame(pose_data)
    file_name = raw_input("Please input the CSV file name:")
    my_df.to_csv(file_name, index=False, header=['t', 'x', 'y', 'z', 'q_x', 'q_y', 'q_z', 'w'])
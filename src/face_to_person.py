#!/usr/bin/env python
import roslib; roslib.load_manifest('accompany')
import rospy
from std_msgs.msg import Float64
from geometry_msgs.msg import Pose2D
from simple_script_server import *
from tf import TransformListener
# from accompany_uva_msg.msg import TrackedHumans

sss=simple_script_server()

class FTPNode:
    def __init__(self, *args):
        print("init")
        self.tf = TransformListener()
        rospy.Subscriber("/trackedHumans", Float64, self.pos_callback)
        # rospy.Subscriber("/trackedHumans", TrackedHumans, pos_callback)

    def pos_callback(self, data):
        rospy.loginfo("on updated pos, face robot towards guy...")
        print("hi")
        if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
            t = self.tf.getLatestCommonTime("/base_link", "/map")
            position, quaternion = self.tf.lookupTransform("/base_link", "/map", t)
             print position
             vector = [0,0,0.5]
             sss.move_base_rel(vector)

if __name__ == '__main__':
    rospy.init_node('face_to_person')
    FTPNode()
    rospy.spin()


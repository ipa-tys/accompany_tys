#!/usr/bin/env python
import roslib; roslib.load_manifest('accompany_tys')
import rospy
# from std_msgs.msg import Float64
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import PointStamped
from simple_script_server import *
from tf import TransformListener
from tf import Transformer
from accompany_uva_msg.msg import TrackedHumans
import math
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

sss=simple_script_server()

class FTPNode:
    def __init__(self, *args):
        print("init")
        self.tf = TransformListener()
        self.tt = Transformer()
        rospy.Subscriber("/trackedHumans", TrackedHumans, self.pos_callback)
        self.publisher = rospy.Publisher("directionmarker_array", MarkerArray)
        self.markerArray = MarkerArray()

    def pos_callback(self, data):
        rospy.loginfo("on updated pos, face robot towards guy...")
        print("hi")
        if (len(data.trackedHumans) > 0):
            print(data.trackedHumans[0].location.point.x)
            try:
                self.tf.waitForTransform(data.trackedHumans[0].location.header.frame_id, "/base_link", rospy.Time.now(), rospy.Duration(2.0))
                pp = self.tf.transformPoint("/base_link", data.trackedHumans[0].location)
                print "Original:"
                print [data.trackedHumans[0].location.point]
                print "Transform:"
                print pp.point

                phi = math.atan2(pp.point.y, pp.point.x)
                # sss.move_base_rel("base", [0,0,phi])
                print phi*180/math.pi

                self.marker = Marker()
                self.marker.header.frame_id = "/map"
                self.marker.type = self.marker.ARROW
                self.marker.action = self.marker.ADD
                self.marker.scale.x = 1
                self.marker.scale.y = 1
                self.marker.scale.z = 1
                self.marker.color.a = 1.0
                self.marker.color.r = 1.0
                self.marker.color.g = 1.0
                self.marker.color.b = 0.0
                # self.marker.points = [[0,0,0],[1,0,0]]
                self.marker.pose.position.x = 1
                self.marker.pose.position.y = 0
                self.marker.pose.position.z = 1
                self.marker.pose.orientation.w = 1
                self.markerArray.markers = []
                self.markerArray.markers.append(self.marker)
                self.publisher.publish(self.markerArray)
                print "try ended"
            except Exception as e:
                print e
            #if self.tf.frameExists("/base_link") and self.tf.frameExists("/map"):
             #   t = self.tf.getLatestCommonTime("/base_link", "/map")
        #     position, quaternion = self.tf.lookupTransform("/base_link", "/map", t)
        #     print position
        #     vector = [0,0,0.5]
        #     sss.move_base_rel(vector)

if __name__ == '__main__':
    rospy.init_node('face_to_person')
    # sss.move_base_rel("base", [0.1,0.0,0.25])
    FTPNode()
    rospy.spin()


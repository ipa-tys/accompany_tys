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

## reality: make sure that person to align to is not robot itself
## align to person with lowest id (except robot) 

sss=simple_script_server()

class FTPNode:
    def __init__(self, *args):
        print("init")
        self.tf = TransformListener()
        self.tt = Transformer()
        rospy.Subscriber("/trackedHumans", TrackedHumans, self.pos_callback)
        self.publisher = rospy.Publisher("directionmarker_array", MarkerArray)


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
                sss.move_base_rel("base", [0,0,phi])
                print phi*180/math.pi
                
                markerArray = MarkerArray()
                marker = Marker()
                marker.header.stamp = rospy.Time();    
                marker.ns = "my_namespace";
                marker.id = 0;  
                marker.header.frame_id = "/base_link"
                marker.type = marker.ARROW
                marker.action = marker.ADD
                marker.scale.x = .1
                marker.scale.y = .1
                marker.scale.z = .1
                marker.color.a = 1.0
                marker.color.r = 1.0
                marker.color.g = 1.0
                marker.color.b = 0.0
                p1 = Point()
                p1.x = 0
                p1.y = 0
                p1.z = 0
                p2 = Point()
                p2.x = pp.point.x
                p2.y = pp.point.y
                p2.z = 0
                marker.points = [p1,p2]
                #marker.pose.position.x = 1
                #marker.pose.position.y = 0
                #marker.pose.position.z = 1
                #marker.pose.orientation.w = 1
                markerArray.markers.append(marker)
                self.publisher.publish(markerArray)
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


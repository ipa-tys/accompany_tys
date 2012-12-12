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
import operator
from tf.transformations import euler_from_quaternion
## reality: make sure that person to align to is not robot itself
## align to person with lowest id (except robot) 

rospy.init_node('face_to_person')

sss=simple_script_server()
#sss.init("base")
#sss.move("arm","folded")
listener = TransformListener()
# listener1 = TransformListener()
publisher = rospy.Publisher("followedPerson", MarkerArray)
publisher1 = rospy.Publisher("diameter", MarkerArray)
listener.waitForTransform('/map','/base_link',rospy.Time(),rospy.Duration(5))

target_angle = 0

trackedPerson = ""

personsToFollow = ['Richard'] # can be a list

def mydist(rob, hum):
    return math.sqrt( (rob[0]-hum.location.point.x)**2 + 
                      (rob[1]-hum.location.point.y)**2 )

def trackedHumans_callback(data):
    print "calllback"
    global trackedPerson
    global target_angle
    (trans, rot) = listener.lookupTransform('/map','/base_link',rospy.Time(0))
    if len(data.trackedHumans)==0:
        print "no humans tracked"
    if len(data.trackedHumans)>0:
        hh = {}
        for h in data.trackedHumans:
            hh[ h.identity ] = h
        
        i = 0
        found = False
        while (not found) and i<len(personsToFollow):
            if personsToFollow[i] in hh:
                found = True
            else:
                i += 1
        if not found:
            if trackedPerson != "":
                print "no person found. not following"
                # sss.say(["no person found. not following"])
                trackedPerson = ""
        if found:
            tt = personsToFollow[i]
            humanX = hh[ tt ].location.point.x
            humanY = hh[ tt ].location.point.y
            if trackedPerson !=  tt :
                trackedPerson = tt
                print "now following " + tt
                dddd = "Now tracking " + tt
                # sss.say([dddd])
            
            markerArray = MarkerArray()
            marker = Marker()
            marker.header.stamp = rospy.Time();    
            marker.ns = "my_namespace";
            marker.id = 0;  
            marker.header.frame_id = "/map"
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
            p1.x = trans[0]
            p1.y = trans[1]
            p1.z = 0
            p2 = Point()
            p2.x = humanX
            p2.y = humanY
            p2.z = 0
            marker.points = [p1,p2]
            markerArray.markers.append(marker)
            publisher.publish(markerArray)
            dx = humanX - trans[0]
            dy = humanY - trans[1]
            target_angle = math.atan2(dy, dx)

rospy.Subscriber("/trackedHumansMod", TrackedHumans, trackedHumans_callback)

print("hi")
# sss.say(["hello"])
# sss.move("base", [1,-0.5,0])
print("ho")
while not rospy.is_shutdown():
    # listener1.waitForTransform('/map','/base_link',rospy.Time(),rospy.Duration(5))
    if trackedPerson != "":
        (trans, rot) = listener.lookupTransform('/map','/base_link',rospy.Time(0))
        phi = euler_from_quaternion(rot)
        current_angle = phi[2]
        "Current angle:"
        print phi
        # h = sss.move("base", [trans[0], trans[1], target_angle], False)
        h = sss.move("base", [trans[0], trans[1], target_angle], False)
        rospy.sleep(3)
    else:
        print "not follow"

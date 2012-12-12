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

rospy.init_node('fusion')

names = {}
stability = {}

stabilityThresh = 5
tolerance = 0.6*0.6

modifiedTrackedHumansPublisher = rospy.Publisher("/trackedHumansMod", TrackedHumans)

def my2dist(rob, hum):
    return (rob[0]-hum.location.point.x)**2 + (rob[1]-hum.location.point.y)**2 

def fusion_callback(data):
    global tolerance
    global names
    global stability
    global stabilityThresh
        
    (trans, rot) = listener.lookupTransform('/map','/base_link',rospy.Time(0))
    filteredHumans = [h for h in data.trackedHumans if my2dist(trans, h) > tolerance ]

    mostStableHumans = {}
    
    for h in filteredHumans:
        if h.id not in names:
            names[h.id] = h.identity
            stability[h.id] = 1
            
        elif h.id in names and names[h.id]==h.identity:
            stability[h.id] +=1

        elif h.id in names and names[h.id]!=h.identity and stability[h.id]<stabilityThresh:
            names[h.id] = h.identity
            stability[h.id] = 1
            
        else: # h.id in names and names[h.id]!=h.identity and stability[h.id]>=stabilityThresh:
            h.identity = names[h.id]
            
        if h.identity not in mostStableHumans:
            mostStableHumans[h.identity] = h.id
        elif stability[ mostStableHumans[h.identity] ] < stability[ h.id ]:
            mostStableHumans[h.identity] = h.id

    for h in filteredHumans:
        if (mostStableHumans[ h.identity ] != h.id and 
            stability[ mostStableHumans[ h.identity ] ] < stabilityThreshold):
            h.identity = ""
        elif (mostStableHumans[ h.identity ] != h.id and 
            stability[ mostStableHumans[ h.identity ] ] >= stabilityThreshold):
            h.identity = ""
            names[h.id] = ""
            stability[h.id] = 0

    modifiedTrackedHumansPublisher.publish(filteredHumans)


rospy.Subscriber("/trackedHumans", TrackedHumans, fusion_callback)

rospy.spin()



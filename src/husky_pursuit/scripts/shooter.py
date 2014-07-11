#!/usr/bin/env python
'''
Ajay Jain
Created June 16, 2014
Last updated July 11, 2014
ARSENL Lab, Naval Postgraduate School
'''

import roslib; roslib.load_manifest("husky_pursuit")
import rospy, math
# import phidgets # phidgets.py
from husky_pursuit.msg import RelativePosition
from std_msgs.msg import Bool

max_range = 5 # Meters

bearing_tolerance = math.radians(15)

yaw_tolerance = math.radians(20)

fire_pub = None
fire_msg = Bool(True)

def get_params():
    global max_range
    global bearing_tolerance
    global yaw_tolerance

    max_range = rospy.get_param('~max_fire_range', max_range)

    bearing_tolerance = rospy.get_param('~bearing_tolerance', bearing_tolerance)

    yaw_tolerance = rospy.get_param('~yaw_tolerance', yaw_tolerance)


    # MAX_LIN = rospy.get_param('~linear_vel_max',  MAX_LIN)
    # MAX_ANG = rospy.get_param('~angular_vel_max', MAX_ANG)


# def shoot():
    # fire_pub.publish(fire_msg)
#     phidgets.interfaceKit.setOutputState(0, 1)
#     sleep(1)
#     phidgets.interfaceKit.setOutputState(0, 0)

def on_relative_position(rel):
    print "relative position"
    get_params()
    if rel.range > max_range:
        rospy.loginfo("Out of range: %f", rel.range)
        return
    if abs(rel.bearing) > bearing_tolerance:
        rospy.loginfo("Out of bearing_tolerance: bearing = %f, tolerance = %f", rel.bearing, bearing_tolerance)
        return
    if abs(rel.yaw) > yaw_tolerance:
        rospy.loginfo("Out of yaw_tolerance: yaw = %f, tolerance = %f", rel.yaw, yaw_tolerance)
        return
    rospy.loginfo("SHOOTING: PUBLISHING FIRE MSG!")
    fire_pub.publish(fire_msg)

def close():
    print("Closing...")

    try:
        phidgets.interfaceKit.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)

    print("Done.")
    exit(0)


def main():
    global fire_pub

    rospy.init_node("shooter")

    fire_pub = rospy.Publisher("status/fire", Bool)
    rospy.Subscriber("/target_relative", RelativePosition, on_relative_position)

    rospy.spin()

    close()

if __name__ == "__main__":
    main()
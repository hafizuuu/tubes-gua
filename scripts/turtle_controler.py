#! /usr/bin/env python3

import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

def pose_callback(msg: Pose):
    cmd = Twist()

    print("x:",msg.x, "y:", msg.y)
    if msg.x > 9.0 or msg.x < 2.0 or msg.y > 9.0 or msg.y < 2.0:
        cmd.linear.x = 1.0
        cmd.angular.z = 1.4

    else:
        cmd.linear.x = 2.0

    pub_cmd.publish(cmd)


def turtle_controller():
    rospy.init_node('turtle_controller')
    rospy.loginfo("Turtle controller node has been started ")
    rospy.Subscriber('/turtle/pose', Pose, pose_callback)
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('turtle_controller')
    rospy.loginfo("Turtle Controller Node has been started")
    pub_cmd = rospy.Publisher('/turtle')
    turtle_controller()

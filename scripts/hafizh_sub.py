#! /usr/bin/env python3

import rospy
from std_msgs.msg import String,Int64


def callback_hafizuu(terserah: String):
    rospy.loginfo("Pesan yang diterima adalah" +terserah.data)

def subscriber():
    rospy.init_node("hafizuu_sub_node")
    rospy.Subscriber('hafizuu_topic', String, callback_hafizuu)
    rospy.spin()


if __name__ == '__main__':
    subscriber()
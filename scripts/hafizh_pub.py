#! /usr/bin/env python3

import rospy
from std_msgs.msg import String, Int64

def publisher():
    rospy.init_node('hafizuu_node', anonymous=False)
    Hafizuu = rospy.Publisher('hafizuu_topic',String, queue_size = 10)
    rate = rospy.Rate(10)
    pesan = "Fizu was Here!"

    Hafizuu = rospy.Publisher('hafizuu_topic',Int64, queue_size = 10)
    rate = rospy.Rate(10)
    angka = "1234"


    while not rospy.is_shutdown():
        print(pesan)
        print(angka)
        rospy.loginfo(pesan)
        Hafizuu.publish(pesan)
        rospy.loginfo(angka)
        Hafizuu.publish(angka)
        rate.sleep()
        rate.sleep()

if __name__ == '__main__':
    publisher()
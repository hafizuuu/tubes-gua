#! /usr/bin/env python3

import rospy
from hafiz_pkg.msg import identitas

def main():
    rospy.init_node("pub_identitas")
    rospy.loginfo("identitas publisher mulai1")
    pub_identitas = rospy.Publisher("identitas_topic", identitas, queue_size=10)
    orang = identitas()
    orang.nama = "hafizhhhhh"
    orang.umur = 19
    orang.hobby = "ganggu orng"

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        pub_identitas.publish(orang)
        rate.sleep()


if __name__ == "__main__":
    main()
#!usr/bin/env python3
import rospy
from std_msgs.msg import String

class Subscriber():
    def __init__(self):
        self.pub_oop = rospy.Publisher("oop", String, queue_size = 10)
        self.orang1 = "hafizh"

    def publish(self):
        self.pub_oop.publish(self.orang1)

def main():
        rospy.init_node("pub_oop", anonymous=True)
        subscriber = Subscriber()
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            subscriber.publish()
            rate.sleep()

if __name__ == "__main__":
    main()
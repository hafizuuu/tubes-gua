#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

class Subscriber():
    def __init__(self):
        # Subscribe ke topik oop dengan tipe pesan identias
        rospy.Subscriber("oop", String, self.callback_Identitas)

    def callback_Identitas(self, data: String):
        self.nama = data.data
        rospy.loginfo("Nama: %s", self.nama)

    def spin(self):
        rospy.spin() #memastikan node tetap berjalan

def main():
        #identitas node ROs bernama 'sub oop"
        rospy.init_node("sub_oop", anonymous=True)
        subscriber = Subscriber() #inisialisasi kelas subscribr
        subscriber.spin()


if __name__ == "__main__":
    main()
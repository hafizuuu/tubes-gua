#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool

class ATM:
    def __init__(self, saldo=0):
        self.saldo = saldo
        self.parameter_log_in = False
        self.transaction_status_pub = rospy.Publisher('/transaction_status', Bool, queue_size=10)
        self.led_control_pub = rospy.Publisher('/led_control', String, queue_size=10)

    def login(self, deteksi_warna_benda):
        if deteksi_warna_benda == 'Segitiga Biru': 
            self.parameter_log_in = True
            print("=== Selamat Anda Berhasil Login! ===")
            self.menu_transaksi()
        else:
            print("Login gagal! Bentuk atau warna tidak sesuai.")
            self.parameter_log_in = False

    def menu_transaksi(self):
        if self.parameter_log_in:
            print("\n=== Silahkan pilih menu transaksi ===")
            print("1. Transfer")
            menu = input("Pilih menu (1): ")
            if menu == '1':
                self.transfer()
            else:
                print("Menu yang Anda pilih tidak tersedia.")
        else:
            print("Login diperlukan terlebih dahulu.")

    def transfer(self):
        if not self.parameter_log_in:
            print("Dimohon untuk melakukan login terlebih dahulu.")
            return
        try:
            rekening_tujuan = input("Silahkan masukkan nomor rekening tujuan: ")
            Jtransfer = int(input("Silahkan masukkan nominal transfer: Rp "))
            if Jtransfer > self.saldo:
                print("Mohon maaf saldo Anda tidak cukup.")
                print(f"Saldo yang Anda miliki saat ini: Rp {self.saldo}")
                self.publish_transaction_status(False)
            else:
                self.saldo -= Jtransfer
                print(f"Transfer telah berhasil! Rp {Jtransfer} telah ditransfer ke rekening {rekening_tujuan}.")
                print(f"Saldo yang Anda miliki saat ini: Rp {self.saldo}")
                self.publish_transaction_status(True)
        except ValueError:
            print("Masukkan jumlah yang valid!")

    def publish_transaction_status(self, status):
        self.transaction_status_pub.publish(status)
        if status:
            self.led_control_pub.publish("Hijau")
        else:
            self.led_control_pub.publish("Merah")

    def deteksi_warna_benda_callback(self, msg):
        deteksi_warna_benda = msg.data
        print(f"deteksi bentuk dan warna :{deteksi_warna_benda}")
        self.login(deteksi_warna_benda)

def main():
    rospy.init_node('bank_node', anonymous=True)
    print("=== Selamat Datang di Fyzu Bank ===")
    print("Silahkan scan kode warna dan bentuk Anda (contoh: Segitiga Biru)...\n")

    atm = ATM(saldo=1000000)

    rospy.Subscriber('/deteksi_warna_benda', String, atm.deteksi_warna_benda_callback)
    rospy.spin()  

if __name__ == '__main__':
    main()

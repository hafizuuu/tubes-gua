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
            print("\n=== Selamat Anda Berhasil Login! ===")
            self.menu_transaksi()
        else:
            print("\nLogin gagal! Bentuk atau warna tidak sesuai.\n")
            self.parameter_log_in = False

    def menu_transaksi(self):
        if self.parameter_log_in:
            print("\n=======================================")
            print("=== Silahkan pilih menu transaksi ===")
            print("=======================================\n")
            print("1. Transfer")
            print("2. Cek Saldo")
            print("3. Tarik Tunai")
            print("4. Bayar Tagihan")
            menu = input("Pilih menu (1): ")
            if menu == '1':
                self.transfer()
            elif menu == '2':
                self.cek_saldo()
            elif menu == '3':
                self.tarik_tunai()
            elif menu == '4':
                self.bayar_tagihan()
            else:
                print("\nMenu yang Anda pilih tidak tersedia.\n")
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
            print("Masukkan jumlah yang valid!\n")

    def cek_saldo(self):
        if not self.parameter_log_in:
            print("Dimohon untuk melakukan login terlebih dahulu.")
            return
        print(f"Saldo yang anda miliki untuk saat ini : Rp {self.saldo}")

    def tarik_tunai(self):
        if not self.parameter_log_in:
            print("Dimohon untuk melakukan login terlebih dahulu.")
            return
        try:
            Jtarik = int(input("Masukkan nominal uang yang ingin anda tarik: Rp"))
            if Jtarik > self.saldo:
                print("Mohon maaf saldo Anda tidak cukup.")
                print(f"Saldo yang Anda miliki saat ini: Rp {self.saldo}")
                self.publish_transaction_status(False)
            else:
                self.saldo -= Jtarik
                print("Penarikan Anda berhasil!")
                print(f"Saldo yang Anda miliki saat ini: Rp {self.saldo}")
                self.publish_transaction_status(True)
        except ValueError:
            print("Masukkan jumlah yang valid!")

    def bayar_tagihan(self):
        if not self.parameter_log_in:
            print("Dimohon untuk melakukan login terlebih dahulu.")
            return
        print("=== Pilih Jenis Tagihan ===")
        print("1. Listrik")
        print("2. Air")
        print("3. Telepon")
        print("4. Internet")
        pilih_tagihan = input("Masukkan jenis tagihan yang ingin dibayar: ")
        try:
            Jtagihan = int(input("Masukkan nominal tagihan yang akan dibayar: Rp "))
            if Jtagihan > self.saldo:
                print("Mohon maaf saldo Anda tidak cukup.")
                print(f"Saldo yang Anda miliki saat ini: Rp {self.saldo}")
                self.publish_transaction_status(False)
            else:
                self.saldo -= Jtagihan  
                print("Pembayaran tagihan berhasil!")
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

    atm = ATM(saldo=5000000)

    rospy.Subscriber('/deteksi_warna_benda', String, atm.deteksi_warna_benda_callback)
    rospy.spin()  

if __name__ == '__main__':
    main()

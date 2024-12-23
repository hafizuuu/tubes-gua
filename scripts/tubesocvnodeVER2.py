import rospy
import cv2
import numpy as np

# Fungsi untuk mendeteksi kontur dan menggambar hasilnya
def getContour(frame, frameContour, color_name):
    contours, _ = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if area > 500:  # Hanya kontur dengan area lebih besar dari 500 yang diproses
            cv2.drawContours(frameContour, [cnt], -1, (0, 0, 225), 2)  # Menggambar kontur

            # Menghitung panjang keliling kontur
            peri = cv2.arcLength(cnt, True)  # Perbaiki penulisan arcLength
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # Menghitung pendekatan polygon
            korner = len(approx)  # Menghitung jumlah sudut

            print(korner)

            x, y, w, h = cv2.boundingRect(approx)  # Menentukan bounding box

            # Identifikasi bentuk
            if korner == 3:
                benda = "Segitiga"
            else:
                benda = "Bentuk Tidak Sesuai"
            
            # Menggambar bounding box dan menambahkan teks
            cv2.rectangle(frameContour, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Perbaiki pemisahan argumen
            cv2.putText(frameContour, f"{benda} {color_name}", (x + (w // 2) - 10, y + (h // 2) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

# Fungsi untuk mendapatkan batas bawah HSV
def get_lower_hsv():
    lower_hue = cv2.getTrackbarPos('LB', 'BGR Trackbar')
    lower_sat = cv2.getTrackbarPos('LG', 'BGR Trackbar')
    lower_val = cv2.getTrackbarPos('LR', 'BGR Trackbar')
    return (lower_hue, lower_sat, lower_val)

# Fungsi untuk mendapatkan batas atas HSV
def get_upper_hsv():
    upper_hue = cv2.getTrackbarPos('UH', 'BGR Trackbar')
    upper_sat = cv2.getTrackbarPos('US', 'BGR Trackbar')
    upper_val = cv2.getTrackbarPos('UV', 'BGR Trackbar')
    return (upper_hue, upper_sat, upper_val)

def main(video):
    while True:
        ret, frame = video.read()

        if not ret:
            break

        # Salin frame untuk memodifikasi dan menampilkan hasil
        frameContour = frame.copy()

        # Mengonversi gambar ke HSV
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Membaca rentang warna dari file
        low = np.load('/home/fizu/hafizuu/src/hafiz_pkg/red_low_npy.npy')
        high = np.load('/home/fizu/hafizuu/src/hafiz_pkg/red_High_npy.npy')
        color_name = "Merah"

        # Thresholding berdasarkan rentang warna dalam ruang HSV
        thresh = cv2.inRange(frame_hsv, low, high)

        # Menggunakan operasi morfologi untuk mengurangi noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # Deteksi kontur pada gambar thresholding
        getContour(thresh, frameContour, color_name)

        # Menampilkan gambar-gambar hasil
        cv2.imshow('thresh', thresh)
        cv2.imshow('frame', frame)
        cv2.imshow('Hasil', frameContour)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    # Mengambil video dari kamera
    cam = cv2.VideoCapture(0)
    main(cam)



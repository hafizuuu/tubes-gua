#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from std_msgs.msg import String, Bool


scan_active = True

def stop_scan_callback(msg):
    global scan_active
    scan_active = not msg.data

def getContour(frame, frameContour, color_name):
    contours, _ =cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500 :

            cv2.drawContours (frameContour, [cnt], -1, (0, 0, 225), 2)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 *peri, True)
            korner = len(approx)
            print(korner)

            x,y,w,h = cv2.boundingRect(approx)

            if korner == 3:
                benda = "Segitiga"
            else:
                benda = "bentuk tidak sesuai"
            
            cv2.rectangle(frameContour, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(frameContour, f"{benda} {color_name}", (x + (w // 2) - 10, y + (h // 2) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            detected_info = f"{benda} {color_name}"
            pub.publish(detected_info)
def get_lower_hsv():
    lower_hue = cv2.getTracbarPos('LB', 'BGR Trackbar')
    lower_sat = cv2.getTracbarPos('LG', 'BGR Trackbar')
    lower_val = cv2.getTracbarPos('LR', 'BGR Trackbar')
    return (lower_hue, lower_sat, lower_val)

def get_upper_hsv():
    upper_hue = cv2.getTracbarPos('UH', 'BGR Trackbar')
    upper_sat = cv2.getTracbarPos('US', 'BGR Trackbar')
    upper_val = cv2.getTracbarPos('UV', 'BGR Trackbar')
    return (upper_hue, upper_sat, upper_val)




def main(video):
    rospy.init_node('ocv_node', anonymous=True)
    global pub
    rospy.Subscriber('/stop_scan', Bool, stop_scan_callback)
    pub = rospy.Publisher('/deteksi_warna_benda', String, queue_size=10)
    while True:
        if not scan_active:
            break
        ret, frame = video.read()
        
        if not ret:
            break
        frameContour = frame.copy()
        frameBlur = cv2.GaussianBlur(frame, (7, 7), 1)
        frameCanny = cv2.Canny(frameBlur, 50, 70)

        low = np.load('/home/fizu/hafizuu/src/hafiz_pkg/red_low_npy.npy')
        high = np.load('/home/fizu/hafizuu/src/hafiz_pkg/red_High_npy.npy')
        color_name = "Biru"

        thresh = cv2.inRange(frame, low, high)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        #thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        #contour, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

        getContour(thresh, frameContour, color_name)
        
        

        cv2.imshow('thresh', thresh)
        cv2.imshow('frame', frame)
        cv2.imshow('canny', frameCanny)
        cv2.imshow('Hasil', frameContour)

        if cv2.waitKey(1) & 0xFF == ord('q') :
            break



if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    main(cam)
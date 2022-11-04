from email.mime import base
import cv2
import numpy as np
from time import time


BREATHRATE = 20
#convert 

b_cycle = 60/BREATHRATE
f = 180
frame_gap = b_cycle/f


guide_base = np.zeros((1000,1000,3), dtype=np.uint8)
cv2.rectangle(guide_base, (475, 475), (525, 525), (255, 255, 18), -1)
next = time()
wide = 900
index = 425
frame = 1
fix = 1
start = time()
count = 0
while True:
    if time() >= next:
        guide_base = np.zeros((1000,1000,3), dtype=np.uint8)
        s = "{:.2f} s".format(time()-start)
        c = "{} times".format(count//2)
        cv2.putText(guide_base,s,(50,50),cv2.FONT_HERSHEY_PLAIN,3,(30,255,255),5)
        cv2.putText(guide_base,c,(50,100),cv2.FONT_HERSHEY_PLAIN,3,(30,255,255),5)
        cv2.rectangle(guide_base, (475, 475-index), (525, 525-index), (255, 255, 18), -1,cv2.LINE_AA)
        cv2.imshow('breath_guide', guide_base)
        index -= int(fix*(wide / (f/2)))
        frame += 1
        if frame == f/2:
            count+=1
            frame = 1
            fix *=-1
        next += frame_gap
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()
"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pandas as pd

gaze = GazeTracking()
webcam = cv2.VideoCapture(1)
left = []
right = []
leftPrev = 0
rightPrev = 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""

    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()

    if left_pupil is None:
        leftPrev += 1
        if leftPrev <= 4: 
            left.append(left_pupil)
    else:
        leftPrev = 0
        left.append(left_pupil)

    if right_pupil is None:
        rightPrev += 1
        if rightPrev <= 4: 
            right.append(right_pupil)
    else:
        rightPrev = 0
        right.append(right_pupil)

    
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), left_pupil, cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    # demo = cv2.resize(frame, (1920,1080))
    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break

fileName = "test"

dfLeft = pd.DataFrame(left)
dfRight = pd.DataFrame(right)

dfLeft.to_csv('eye-track-algo/data/left/{}.csv'.format(fileName), index=False)
dfRight.to_csv('eye-track-algo/data/right/{}.csv'.format(fileName), index=False)

webcam.release()
cv2.destroyAllWindows()

# USAGE
# python ball_tracking_demo.py --video video.mp4
# python ball_tracking_demo.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2


video = "vision/videos/video2.mp4"
video = ""
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
# HSV Info: http://infohost.nmt.edu/tcc/help/pubs/colortheory/web/hsv.html
yellow_lower_threshold = (160, 100, 140)
yellow_upper_threshold = (179, 255, 255)
red_lower_threshold = (0, 100, 140)
red_upper_threshold = (20, 255, 255)

# if a video path was not supplied, grab the reference
# to the webcam
if not video:
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(video)

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if video and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "orange", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask_red = cv2.inRange(hsv, red_lower_threshold, red_upper_threshold)
    mask_yellow = cv2.inRange(hsv, yellow_lower_threshold, yellow_upper_threshold)
    mask = mask_red + mask_yellow
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(contours) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 1:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius + 20), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

    # update the points queue
    print (center)

    # show the frame to our screen
    cv2.imshow("Frame", frame)


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

# USAGE
# python ball_tracking_demo.py --video video.mp4
# python ball_tracking_demo.py

# import the necessary packages
from collections import deque
import numpy
import argparse
import imutils
import cv2
from Properties import Properties
from homograpy.utils import get_four_points

# -------------------------------
# --------- ARG PARSING ---------
# -------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())


# -------------------------------
# -------- TUNING SETUP ---------
# -------------------------------
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
# HSV Info: http://infohost.nmt.edu/tcc/help/pubs/colortheory/web/hsv.html
yellowLowerThreshold = (170, 100, 140)
yellowUpperThreshold = (179, 255, 255)
redLowerThreshold = (0, 100, 140) 
redUpperThreshold = (20, 255, 255) 
pts = deque(maxlen=args["buffer"])
# Destination image
size = (Properties.GRID_SIZE_X, Properties.GRID_SIZE_Y, 3)

# -------------------------------
# ------- VIDEO FEED SETUP ------
# -------------------------------
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

# -------------------------------
# --------- CALIBRATION ---------
# -------------------------------
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(0) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

    # if the 'l' key is pressed, load matrix from file
    elif key == ord("l"):
        deskew_matrix = None
        try:
            deskew_matrix = numpy.loadtxt("deskew_matrix.txt")
            print("Loaded deskew matrix from calibration file.")
            print(deskew_matrix)
        except:
            print("WARNING: No deskew matrix found. Please re-run calibration to map the playing area.")

        break

    # if the 'c' key is pressed, enter calibration mode
    elif key == ord("c"):
        print ('''
        Click on the four corners of the book -- top left first and
        bottom left last -- and then hit ENTER
        ''')

        # Show image and wait for 4 clicks.
        # cv2.imshow("Click 4 Corners (Top Left -> Top Right -> Bottom Right -> Bottom Left", frame)
        pts_src = get_four_points(frame)

        # Destination image
        im_dst = numpy.zeros(size, numpy.uint8)
        pts_dst = numpy.array(
                           [
                            [0,0],
                            [size[0] - 1, 0],
                            [size[0] - 1, size[1] -1],
                            [0, size[1] - 1 ]
                            ], dtype=float
                           )

        # Calculate the homography
        deskew_matrix, status = cv2.findHomography(pts_src, pts_dst)
        
        # Save the calibration values to a file
        print ("------ Saved:")
        print (deskew_matrix)
        numpy.savetxt("deskew_matrix.txt", deskew_matrix)
        print ("------ Loaded back:")
        print (numpy.loadtxt("deskew_matrix.txt"))
        
        cv2.destroyAllWindows()
        break
        # print (h)
        #
        # # Warp source image to destination
        # im_dst = cv2.warpPerspective(frame, h, size[0:2])
        #
        # # Show output
        # cv2.imshow("Image", im_dst)
        # cv2.waitKey(0)


transform_matrix = numpy.matrix([[4.84926407e+00,   2.23812188e+00,  -1.81810101e+03],
                                 [-3.75380532e-01,   6.67343169e+00,  -3.16620966e+03],
                                 [-1.41789764e-04,   1.29975526e-03,   1.00000000e+00]])

print ("TYPED IN TRANSFORM MATRIX")
print (transform_matrix)

# -------------------------------
# ------- TRACK DAT BALL --------
# -------------------------------
while True:
    # grab the current frame
    (grabbed, frame_distorted) = camera.read()
    frame = cv2.warpPerspective(frame_distorted, deskew_matrix, size[0:2])

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "orange", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    maskRed = cv2.inRange(hsv, redLowerThreshold, redUpperThreshold)
    maskYellow = cv2.inRange(hsv, yellowLowerThreshold, yellowUpperThreshold)
    mask = maskRed + maskYellow
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 1:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            # cv2.putText(frame, "Hello!", , cvInitFont() ,(0, 255, 255))
            cv2.putText(frame,"BALL FOUND!", (10, 50), cv2.FONT_ITALIC, 1, 255)
            cv2.circle(frame, (int(x), int(y)), int(radius + 1), (0, 255, 255), 1)
            cv2.circle(frame, center, 2, (0, 255, 255), -1)

    # update the points queue
    pts.appendleft(center)
    print (center)

    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(numpy.sqrt(args["buffer"] / float(i + 1)) * 0.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)

    # show the frame to our screen
    frame = imutils.resize(frame, width=500)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

import cv2
import argparse
import numpy as np


def mouse_handler(event, x, y, flags, data) :

    if event == cv2.EVENT_LBUTTONDOWN :
        cv2.circle(data['im'], (x,y),3, (0,0,255), 5, 16);
        cv2.imshow("Image", data['im']);
        if len(data['points']) < 4 :
            data['points'].append([x,y])


def get_four_points(im):

    # Set up data to send to mouse handler
    data = {}
    data['im'] = im.copy()
    data['points'] = []

    # Set the callback function for any mouse event
    cv2.imshow("Image",im)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)

    # Convert array to np.array
    points = np.vstack(data['points']).astype(float)

    return points


# -------------------------------

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())


if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])


while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(0) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

    elif key == ord("c"):
        print ('''
        Click on the four corners of the book -- top left first and
        bottom left last -- and then hit ENTER
        ''')

        # Show image and wait for 4 clicks.
        cv2.imshow("Click 4 Corners (Top Left -> Top Right -> Bottom Right -> Bottom Left", frame)
        pts_src = get_four_points(frame)

        # Destination image
        size = (500,500,3)
        im_dst = np.zeros(size, np.uint8)
        pts_dst = np.array(
                           [
                            [0,0],
                            [size[0] - 1, 0],
                            [size[0] - 1, size[1] -1],
                            [0, size[1] - 1 ]
                            ], dtype=float
                           )

        # Calculate the homography
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Save the calibration values to a file
        print ("------ Saved:")
        print (h)
        np.savetxt("deskew_matrix.txt", h)
        print ("------ Loaded back:")
        print (np.loadtxt("deskew_matrix.txt"))


        # Warp source image to destination
        im_dst = cv2.warpPerspective(frame, h, size[0:2])
        cv2.destroyAllWindows()

        # Show output
        cv2.imshow("Image", im_dst)
        cv2.waitKey(0)

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

# BallTracker
# Singleton class for keeping an observable coordinates of a ball, found via camera input

import cv2
import threading
import time
import numpy as np


class BallTracker:

    # Singleton instance
    instance = None


    @staticmethod
    def get_instance():
        if BallTracker.instance is None:
            BallTracker.instance = BallTracker()

        return BallTracker.instance



    def __init__(self):
        self.ballTrackingEnabled = False
        self.xBallPosition = None
        self.yBallPosition = None
        self.lastUpdated = time.localtime()
        self.ballRadius = 0.07  # NOTE: This is a magic number and should be moved to a "physical properties" class
        self.observers = []
        self.deskew_matrix = None
        try:
            self.deskew_matrix = np.loadtxt("deskew_matrix.txt")
            print("Loaded deskew matrix from calibration file.")
            print(self.deskew_matrix)
        except:
            print("WARNING: No deskew matrix found. Please re-run calibration to map the playing area.")

        # Singleton logic
        if BallTracker.instance is None:
            BallTracker.instance = self
        else:
            print("WARNING: You are creating an instance directly in a class intended to be a singleton. "
                  "Use BallTracker.get_instance() instead.")



    def start_ball_tracking(self):
        # TODO: Handle case where already started

        self.ballTrackingEnabled = True

        # Start ball tracking thread
        t1 = threading.Thread(target=self.track_ball)
        t1.daemon = True
        t1.start()



    def stop_ball_tracking(self):
        self.ballTrackingEnabled = False

    # Only to be run on its own thread
    def track_ball(self, video=""):

        print ('Started real camera ball tracking!!!!')
        print (cv2.__version__)
        # define the lower and upper boundaries of the "green"
        # ball in the HSV color space, then initialize the
        # list of tracked points
        # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
        # HSV Info: http://infohost.nmt.edu/tcc/help/pubs/colortheory/web/hsv.html
        yellow_lower_threshold = (160, 100, 40)
        yellow_upper_threshold = (179, 255, 255)
        red_lower_threshold = (0, 100, 40)
        red_upper_threshold = (20, 255, 255)

        # if a video path was not supplied, grab the reference
        # to the webcam
        if not video:
            camera = cv2.VideoCapture(0)

        # otherwise, grab a reference to the video file
        else:
            camera = cv2.VideoCapture(video)

        # keep looping
        while self.ballTrackingEnabled:

            # grab the current frame
            (grabbed, frame_distorted) = camera.read() # grab the current frame
            destination_img_size = (100, 100, 3)

            # Deskew the camera input to make the playing field a grid
            if self.deskew_matrix is not None:
                frame = cv2.warpPerspective(frame_distorted, self.deskew_matrix, destination_img_size[0:2])
            else:
                frame = frame_distorted

            # check for end of video
            if video and not grabbed:
                break

            # resize the frame, blur it, and convert it to the HSV
            # color space
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
                self.xBallPosition = center[0]
                self.yBallPosition = center[1]

                # only proceed if the radius meets a minimum size
                if radius > 1:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius + 1), (0, 255, 255), 1)
                    cv2.circle(frame, center, 2, (0, 255, 255), -1)

            # send update of ball location
            self.lastUpdated = time.clock()
            if self.yBallPosition is not None:
                y_flipped = 100-self.yBallPosition
            else:
                y_flipped = self.yBallPosition
                
            self.push_notification("Location Updated:",
                                   x=self.xBallPosition,
                                   y=y_flipped,    # Move origin to bottom left corner
                                   updated_at=self.lastUpdated,
                                   frame=frame)

        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()

        print ("Ball tracking stopped.")

    def read_keyboard_input(self):
        key = raw_input('q = Exit, p = Get Ball Position \n')
        print ("Key entered: " + key)

        if key == 'q':
            self.stop_ball_tracking()

        elif key == 'p':
            print (self.get_ball_position())
            self.read_keyboard_input()

        else:
            self.read_keyboard_input()

    # def get_ball_position(self):
    # 	return [self.xBallPosition, self.yBallPosition, self.lastUpdated]



    def get_ball_radius(self):
        return self.ballRadius

    # Observer Functions
    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def push_notification(self, *args, **keywordargs):
        for observer in self.observers:
            observer.notify(*args, **keywordargs)

    def initialize_camera(self, path):
        # TODO: Might need to add code here to gracefully handle a failed camera initialization
        if path is None:
            camera = cv2.VideoCapture(0)
        else:
            camera = cv2.VideoCapture(path)

# BallTracker
# Singleton class for keeping an observable coordinates of a ball, found via camera input

import cv2
import threading
import time
import numpy as np
from Properties import Properties


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
    def track_ball(self):

        print ('Started camera ball tracking')
        print (cv2.__version__)

        # -------------------------------
        # -------- TUNING SETUP ---------
        # -------------------------------
        # Set HSV color range thresholds
        # HSV Info: http://infohost.nmt.edu/tcc/help/pubs/colortheory/web/hsv.html
        # (Hue, Saturation, Value)
        # For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]
        yellow_lower_threshold = (160, 100, 40)
        yellow_upper_threshold = (179, 255, 255)
        red_lower_threshold = (0, 50, 40)
        red_upper_threshold = (40, 255, 255)
        index = 0   # Index in the round queue

        # -------------------------------
        # ------- VIDEO FEED SETUP ------
        # -------------------------------
        camera = cv2.VideoCapture(0)
        if camera is None:
            self.stop_ball_tracking()
            print("Camera not found.")

        # -------------------------------
        # ------- TRACK DAT BALL --------
        # -------------------------------
        # Ball tracking algorithm inspired by Adrian Rosebrock @ PyImageSearch.com
        # http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

        while self.ballTrackingEnabled:

            # Grab the current frame and track the processing time
            processing_start_time = time.clock()
            (grabbed, frame_distorted) = camera.read()
            destination_img_size = (Properties.GRID_SIZE_X, Properties.GRID_SIZE_Y, 3)

            # Before beginning the processing notify subscribers that a new frame has been grabbed
            self.push_notification(new_frame_being_processed=True)

            # Deskew the camera input to make the playing field a grid
            if self.deskew_matrix is not None:
                frame = cv2.warpPerspective(frame_distorted, self.deskew_matrix, destination_img_size[0:2])  # Pi Processing time test:  0.02

            else:
                frame = frame_distorted

            # Convert to HSV color mode
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                                      # Pi Processing time test: 0.001

            # Create a mask containing only the areas that fall within the HSV thresholds       # Pi Processing time test: 0.04
            mask_red = cv2.inRange(hsv, red_lower_threshold, red_upper_threshold)
            mask_yellow = cv2.inRange(hsv, yellow_lower_threshold, yellow_upper_threshold)
            mask = mask_red + mask_yellow

            # Perform erosion and dilation to smooth out blobs
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)

            # Find largest contour
            contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]            # 0.03
            if len(contours) > 0:
                c = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                self.xBallPosition = center[0]
                self.yBallPosition = center[1]

                # Proceed if the radius meets a minimum size
                if radius > 1:
                    cv2.circle(frame, center, int(Properties.BALL_RADIUS), (0, 255, 255), 1)

            # Send update of ball location
            processing_time = time.clock() - processing_start_time
            self.lastUpdated = time.clock()
            if self.yBallPosition is not None:
                y_flipped = Properties.GRID_SIZE_Y-self.yBallPosition
            else:
                y_flipped = self.yBallPosition

            self.push_notification("Location Updated:",
                                   x=self.xBallPosition,
                                   y=y_flipped,    # Move origin to bottom left corner
                                   updated_at=self.lastUpdated,
                                   latency=processing_time,
                                   frame=frame,
                                   index=index)

        camera.release()
        print ("Ball tracking stopped.")


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


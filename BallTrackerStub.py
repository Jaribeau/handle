# BallTrackerStub
# Singleton class for keeping an observable coordinates of a ball, found via camera input

import time
import random
import threading

class BallTracker:
    # Singleton instance
    instance = None

    @staticmethod
    def get_instance():
        if BallTracker.instance is None:
            BallTracker.instance = BallTracker()

        return BallTracker.instance

    def __init__(self):
        self.observers = []

    def start_ball_tracking(self):
        print("Psudo ball tracking started.")
        t2 = threading.Thread(target=self.ball_tracking())
        t2.daemon = True
        t2.start()


    def ball_tracking(self):
        while True:
            self.push_notification("Location Updated:",
                       x=random.random(),
                       y=random.random())
            time.sleep(1)


    def stop_ball_tracking(self):
        self.ballTrackingEnabled = False

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

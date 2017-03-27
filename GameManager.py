# GameManager

from BallTracker import BallTracker
from ObstacleManager import ObstacleManager
from Properties import Properties
import imutils
import threading
import cv2
import time
import calendar


class GameManager:

    def __init__(self, difficulty="Normal"):
        self.observers = []
        self.ballTracker = BallTracker.get_instance()
        self.obstacle = ObstacleManager()
        self.timeElapsed = 0
        self.start_time = 0
        self.difficulty = difficulty
        self.gameOn = False
        self.frame = None
        self.score = 0
        self.game_up_to_date = True
        self.message = ""



    def start_game(self):
        print ("Starting Game!!!")
        print ("----------------")
        self.ballTracker.start_ball_tracking()
        self.ballTracker.register(self)
        self.obstacle.start_movement()
        self.obstacle.set_mode("fixed")
        self.start_time = time.clock()
        self.gameOn = True
        # self.window = cv2.namedWindow("WebcamWindow")

        print("Starting update_game thread.")
        mainGameThread = threading.Thread(target=self.update_game)
        mainGameThread.daemon = True
        mainGameThread.start()



    def update_game(self):
        while self.gameOn:
            if self.game_up_to_date is False:
                time_update_started = time.clock()
                self.timeElapsed = int((time.clock() - self.start_time))

                # Starting count-down
                if self.timeElapsed < 6:
                    if self.timeElapsed > 3:
                        self.message = "GO!"
                        # self.obstacle.set_mode("bounce")
                    elif self.timeElapsed > 2:
                        self.message = "1"
                    elif self.timeElapsed > 1:
                        self.message = "2"
                    elif self.timeElapsed > 0:
                        self.message = "3"

                elif self.timeElapsed < 7:
                    self.message = ""

                # Regular gameplay
                if self.frame is not None:
                    cv2.putText(self.frame, "Score:" + str(self.score), (5, 10), cv2.FONT_ITALIC, 0.5, 255)
                    cv2.putText(self.frame, "o", (int(self.obstacle.xPosition * Properties.GRID_SIZE_X)-25, Properties.GRID_SIZE_Y - int(self.obstacle.yPosition * Properties.GRID_SIZE_Y)+20), cv2.FONT_HERSHEY_SIMPLEX, 3, 0)
                    self.frame = imutils.resize(self.frame, width=Properties.GRID_SIZE_X)
                    # cv2.imshow(self.window, self.frame)

                if self.obstacle.collides_with([self.ballTracker.xBallPosition, self.ballTracker.yBallPosition], Properties.BALL_RADIUS):
                    print("------- Collision!!! -------- SCORE: -", self.score)
                    self.message = "GAME OVER\nSCORE: " + str(self.score)
                    self.push_notification("update",
                                       message=self.message,
                                       frame=self.frame,
                                       timeRemaining=self.timeElapsed,
                                       gameOn=self.gameOn,
                                       score=self.score,
                    )
                    self.end_game()
                else:
                    # Check timer, increment score every ~second
                    # self.score += 1
                    self.score = self.timeElapsed * 10

                # Notify subscribers that game state has been updated
                latency_out = self.latency_in + time.clock() - time_update_started
                self.push_notification("update",
                                       message=self.message,
                                       frame=self.frame,
                                       timeRemaining=self.timeElapsed,
                                       gameOn=self.gameOn,
                                       score=self.score,
                                       latency=latency_out
                                       )
                self.game_up_to_date = True



    def end_game(self):
        print ("Game Over.")
        if self.gameOn is True:
            self.gameOn = False
            self.obstacle.stop_movement()
            self.ballTracker.unregister_all()
            self.ballTracker.stop_ball_tracking()
            self.unregister_all()
            self.timeElapsed = 0



    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):

        # Store frame value for display from main thread
        if keywordargs.get('frame') is not None:
            self.frame = keywordargs.get('frame')
            self.latency_in = keywordargs.get('latency')

        # # TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
        # if keywordargs.get('x') is not None and keywordargs.get('y') is not None:
        #     self.game_up_to_date = False

        self.game_up_to_date = False


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

# GameManager

from BallTracker import BallTracker
from ObstacleManager import ObstacleManager
from Properties import Properties
import imutils
import threading
import cv2


class GameManager:

    def __init__(self, time=60000, difficulty="Normal"):
        self.observers = []
        self.ballTracker = BallTracker.get_instance()
        self.obstacle = ObstacleManager()
        self.timeRemaining = time
        self.difficulty = difficulty
        self.gameOn = False
        self.frame = None
        self.score = 0
        self.game_up_to_date = True



    def start_game(self):
        print ("Starting Game!!!")
        print ("----------------")
        self.ballTracker.start_ball_tracking()
        self.ballTracker.register(self)
        self.obstacle.start_movement()
        self.timeRemaining = 60000
        self.gameOn = True
        # self.window = cv2.namedWindow("WebcamWindow")

        print("Starting update_game thread.")
        mainGameThread = threading.Thread(target=self.update_game)
        mainGameThread.daemon = True
        mainGameThread.start()



    def update_game(self):
        while self.gameOn:
            if self.game_up_to_date is False:
                self.timeRemaining -= 1

                if self.frame is not None:
                    cv2.putText(self.frame, "Score:" + str(self.score), (5, 10), cv2.FONT_ITALIC, 0.5, 255)
                    cv2.putText(self.frame, "o", (int(self.obstacle.xPosition * Properties.GRID_SIZE_X)-25, Properties.GRID_SIZE_Y - int(self.obstacle.yPosition * Properties.GRID_SIZE_Y)+20), cv2.FONT_HERSHEY_SIMPLEX, 3, 0)
                    self.frame = imutils.resize(self.frame, width=Properties.GRID_SIZE_X)
                    # cv2.imshow(self.window, self.frame)
                    self.push_notification("image",
                                           image=self.frame)

                if self.obstacle.collides_with([self.ballTracker.xBallPosition, self.ballTracker.yBallPosition], Properties.BALL_RADIUS):
                    print ("------- Collision!!! -------- SCORE: -", self.score)
                    self.score += 1

                cv2.waitKey(1)
                self.game_up_to_date = True



    def end_game(self):
        print ("Game Over.")
        self.gameOn = False
        self.obstacle.stop_movement()
        self.ballTracker.unregister_all()
        # self.ballTracker.stop_ball_tracking()
        self.unregister_all()
        self.timeRemaining = 0



    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):

        # Store frame value for display from main thread
        if keywordargs.get('frame') is not None:
            self.frame = keywordargs.get('frame')

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

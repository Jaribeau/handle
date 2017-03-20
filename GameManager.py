# GameManager

from BallTracker import BallTracker
from ObstacleManager import ObstacleManager
import imutils
import cv2


class GameManager:



    def __init__(self, time=60000, difficulty="Normal"):
        self.ballTracker = BallTracker.get_instance()
        self.obstacle = ObstacleManager()
        self.timeRemaining = time
        self.difficulty = difficulty
        self.gameOn = False
        self.frame = None
        self.score = 0



    def start_game(self):
        print ("Starting Game!!!")
        print ("----------------")
        self.ballTracker.start_ball_tracking()
        self.ballTracker.register(self)
        self.obstacle.start_movement()
        self.timeRemaining = 60000
        self.gameOn = True

        while self.gameOn:
            self.timeRemaining -= 1
            if self.frame is not None:
                cv2.putText(self.frame, "Score:" + str(self.score), (5, 10), cv2.FONT_ITALIC, 0.5, 255)
                cv2.putText(self.frame, "x", (int(self.obstacle.xPosition*100)-5, 100 - int(self.obstacle.yPosition*100)-5), cv2.FONT_ITALIC, 1, 0)
                self.frame = imutils.resize(self.frame, width=900)
                cv2.imshow("Ball Tracking", self.frame)
                cv2.waitKey(1)



    def end_game(self):
        print ("Game Over.")
        self.ballTracker.stop_ball_tracking()
        self.ballTracker.unregister_all()
        self.obstacle.stop_movement()
        self.timeRemaining = 0
        self.gameOn = False



    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):

        # Store frame value for display from main thread
        self.frame = keywordargs.get('frame')

        # TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
        if keywordargs.get('x') is not None \
                and keywordargs.get('y') is not None \
                and self.obstacle.collides_with([keywordargs.get('x'), keywordargs.get('y')], self.ballTracker.get_ball_radius()):
            print ("------- Collision!!! -------- SCORE: -", self.score)
            self.score += 1
            #self.end_game()



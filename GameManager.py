# GameManager

from BallTracker import BallTracker
from ObstacleManager import ObstacleManager


class GameManager:



    def __init__(self, time=60000, difficulty="Normal"):
        self.ballTracker = BallTracker()
        self.obstacle = ObstacleManager()
        self.timeRemaining = time
        self.difficulty = difficulty
        self.gameOn = False



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



    def end_game(self):
        print ("Game Over.")
        self.ballTracker.stop_ball_tracking()
        self.ballTracker.unregister_all()
        self.obstacle.stop_movement()
        self.timeRemaining = 0
        self.gameOn = False



    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):

        # TODO: CHECK ARGUMENTS TO DETERMINE MESSAGE/TYPE - pass on to handlers?
        if self.obstacle.collides_with([keywordargs.get('x'), keywordargs.get('y')], self.ballTracker.get_ball_radius()):

            # TODO: Figure out why frame isn't being passed through correctly
            # print (keywordargs.get('frame'))
            # cv2.imshow("Ball Tracking", keywordargs.get('frame'))
            # cv2.waitKey(1)
            print ("------- Collision!!! --------")
            self.end_game()



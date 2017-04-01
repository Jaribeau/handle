# GameManager

from BallTracker import BallTracker
from ObstacleManager import ObstacleManager
from Properties import Properties
import imutils
import threading
import cv2
import time
try:
    import RPi.GPIO as GPIO
except:
    gpio_module_present = False


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
        self.average_latency = 0
        self.latency_in = 0
        self.obstacle_x = 0
        self.obstacle_y = 0

        if gpio_module_present:
            self.BUZZ_PIN = 21
            self.BUZZ_FREQ = 2000 # Frequency of pulses
            self.BUZZ_DC = 60 # affects sound frequency
            self.BUZZ_TIME_INTERVAL = 1.0 # time in seconds between buzzes
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.BUZZ_PIN, GPIO.OUT)
            self.buzzerPwm = GPIO.PWM(self.BUZZ_PIN, self.BUZZ_FREQ)



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
                        self.message = " GO!"
                        self.obstacle.set_mode("bounce")
                    elif self.timeElapsed > 2:
                        self.message = " 1"
                    elif self.timeElapsed > 1:
                        self.message = " 2"
                    elif self.timeElapsed > 0:
                        self.message = " 3"

                elif self.timeElapsed < 7:
                    self.message = ""

                # Regular gameplay
                if self.frame is not None:
                    # cv2.putText(self.frame, "Score:" + str(self.score), (5, 10), cv2.FONT_ITALIC, 0.5, 255)
                    # cv2.putText(self.frame, "o", (int(self.obstacle.xPosition * Properties.GRID_SIZE_X)-25, Properties.GRID_SIZE_Y - int(self.obstacle.yPosition * Properties.GRID_SIZE_Y)+20), cv2.FONT_HERSHEY_SIMPLEX, 3, 0)
                    cv2.circle(self.frame, (int(self.obstacle.xPosition), Properties.GRID_SIZE_Y - int(self.obstacle.yPosition)), int(Properties.BALL_RADIUS), (255, 0, 255), 1)
                    self.frame = imutils.resize(self.frame, width=Properties.GRID_DISPLAY_SIZE_X)
                    # cv2.imshow(self.window, self.frame)

                if self.timeElapsed > 5 and self.collides_with([self.ballTracker.xBallPosition, self.ballTracker.yBallPosition], [self.obstacle_x, self.obstacle_y], Properties.BALL_RADIUS):
                    print("------- Collision!!! -------- SCORE: -", self.score)
                    self.message = "GAME\nOVER"
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
                if self.average_latency == 0:
                    self.average_latency = latency_out
                else:
                    self.average_latency += (latency_out - self.average_latency)/10
                self.push_notification("update",
                                       message=self.message,
                                       frame=self.frame,
                                       timeRemaining=self.timeElapsed,
                                       gameOn=self.gameOn,
                                       score=self.score,
                                       latency=self.average_latency
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



    # called by GameManager
    def collides_with(self, ball_position, obstacle_position, radius):

        if ball_position[0] is None or ball_position[1] is None:
            ball_x = None
            ball_y = None
        else:
            ball_x = float(ball_position[0])
            ball_y = float(ball_position[1])

        if obstacle_position[0] is None or obstacle_position[1] is None:
            obstacle_x = None
            obstacle_y = None
        else:
            obstacle_x = float(obstacle_position[0])
            obstacle_y = float(obstacle_position[1])

        # Check for collision
        if obstacle_x is not None and obstacle_y is not None and \
                ((obstacle_x - radius) <= ball_x <= (obstacle_x + radius)) and \
                ((Properties.GRID_SIZE_Y - obstacle_y - radius) <= ball_y <= (Properties.GRID_SIZE_Y - obstacle_y + radius)):
            print("Ball:    " + str(obstacle_x) + ", " + str(obstacle_y))
            print("Obstacle:" + str(obstacle_x) + ", " + str(obstacle_y))

            if gpio_module_present:
                t2 = threading.Thread(target=self.buzzer)
                t2.daemon = True
                t2.start()
                return True
        else:
            return False


    # Note: Run asynchronously
    def buzz(self):
        if gpio_module_present:
            self.buzzerPwm.start(self.BUZZ_DC)
            time.sleep(self.BUZZ_TIME_INTERVAL) # In seconds
            self.buzzerPwm.stop()


    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):

        # Store frame value for display from main thread
        if keywordargs.get('frame') is not None:
            self.frame = keywordargs.get('frame')
            self.latency_in = keywordargs.get('latency')

        if keywordargs.get('new_frame_being_processed') is True:
            # Grab the obstacle location the corresponds to the timing of THIS frame
            self.obstacle_x = self.obstacle.xPosition
            self.obstacle_y = self.obstacle.yPosition

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

# GameClient

import sys
from PyQt5 import QtGui, QtWidgets, Qt
from GameManager import GameManager
import cv2


class GameClient():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)

        self.game = None
        self.game_cv_image = None
        self.game_message = ""
        self.game_time_remaining = 0
        self.game_is_over = True
        self.game_score = 0

        # Set label, size, and position
        self.window = QtWidgets.QWidget()
        self.window.setGeometry(10, 200, 600, 800)
        self.window.setWindowTitle("Handle")

        # Create UI elements
        self.pixmap = QtGui.QPixmap(500, 500)
        self.pixmap.fill(Qt.QColor("white"))
        self.game_image_label = QtWidgets.QLabel(self.window)
        self.game_image_label.setFixedHeight(500)
        self.game_image_label.setFixedWidth(500)
        self.game_image_label.move(50, 260)
        # self.game_image = QtGui.QImage(500, 500, )

        self.game_message_label = QtWidgets.QLabel(self.window)
        self.game_message_label.setText(self.game_message)
        self.game_message_label.move(80, 275)
        self.game_message_label.setFixedWidth(500)
        self.game_message_label.setFixedHeight(200)
        self.game_message_label.setFont(Qt.QFont("Helvetica [Cronyx]", 70, 30))  # Font family, size, weight

        self.game_score_label = QtWidgets.QLabel(self.window)
        self.game_score_label.setText(("SCORE: " + str(self.game_score)))
        self.game_score_label.move(80, 20)
        self.game_score_label.setFixedWidth(500)
        self.game_score_label.setFont(Qt.QFont("Helvetica [Cronyx]", 70, 30))  # Font family, size, weight


        self.start_game_button = QtWidgets.QPushButton("START GAME", self.window)
        self.start_game_button.move(50, 20)
        self.start_game_button.clicked.connect(self.start_game)

        self.end_game_button = QtWidgets.QPushButton("QUIT", self.window)
        self.end_game_button.move(50, 20)
        self.end_game_button.clicked.connect(self.end_game)
        self.end_game_button.hide()

        self.window.show()
        sys.exit(self.app.exec_())

    def start_game(self):
        if self.game is None or self.game.gameOn is False:
            self.game = GameManager()
            self.game.start_game()
            self.game.register(self)
            self.end_game_button.show()
            self.start_game_button.hide()

    def end_game(self):
        if self.game is not None:
            self.game.end_game()
            self.start_game_button.show()
            self.end_game_button.hide()

    def notify(self, *args, **keywordargs):

        if keywordargs.get('message') is not None:
            self.game_message = keywordargs.get('message')
            self.game_message_label.setText(self.game_message)

        if keywordargs.get('score') is not None:
            self.game_score = keywordargs.get('score')
            self.game_score_label.setText("SCORE: " + str(self.game_score))

        if keywordargs.get('timeRemaining') is not None:
            self.game_time_remaining = keywordargs.get('timeRemaining')

        if keywordargs.get('gameOn') is False:
            self.game_is_over = not keywordargs.get('gameOn')
            # Show game over screen

        if keywordargs.get('frame') is not None:
            self.game_cv_image = keywordargs.get('frame')
            # self.cvImage = cv2.imread(r'cat.jpg')
            height, width, byteValue = self.game_cv_image.shape
            byteValue = byteValue * width

            cv2.cvtColor(self.game_cv_image, cv2.COLOR_BGR2RGB, self.game_cv_image)

            self.mQImage = QtGui.QImage(self.game_cv_image, width, height, byteValue, QtGui.QImage.Format_RGB888)
            painter = QtGui.QPainter()
            painter.begin(self.pixmap)
            painter.drawImage(0, 0, self.mQImage)
            painter.end()

            self.game_image_label.setPixmap(self.pixmap)
            self.game_image_label.show()


# ----------------------------------------------------

if __name__ == '__main__':
    client = GameClient()


# while True:
#     key = input('q = Exit, p = Get Ball Position \n')
#     print ("Key entered: " + key)
#
#     if key == 'q':
#         break

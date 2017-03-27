# GameClient

import sys
from PyQt5 import QtGui, QtWidgets, Qt
from GameManager import GameManager
import cv2


class GameClient():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.game = None
        self.cvImage = None

        # Set label, size, and position
        self.window = QtWidgets.QWidget()
        self.window.setGeometry(10, 200, 600, 600)
        self.window.setWindowTitle("Handle")

        # Add Elements
        self.label = QtWidgets.QLabel(self.window)
        self.label.setText("Hello World!")
        self.label.move(50, 20)

        self.start_game_button = QtWidgets.QPushButton("START GAME", self.window)
        self.start_game_button.move(50, 20)
        self.start_game_button.clicked.connect(self.start_game)

        self.end_game_button = QtWidgets.QPushButton("QUIT", self.window)
        self.end_game_button.move(50, 20)
        self.end_game_button.clicked.connect(self.end_game)
        self.end_game_button.hide()

        self.pixmap = QtGui.QPixmap(500, 500)
        self.pixmap.fill(Qt.QColor("white"))
        self.game_image_label = QtWidgets.QLabel(self.window)
        self.game_image_label.setFixedHeight(500)
        self.game_image_label.setFixedWidth(500)
        self.game_image_label.move(50, 60)
        # self.game_image = QtGui.QImage(500, 500, )

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

        # Show image
        self.cvImage = keywordargs.get('image')
        # self.cvImage = cv2.imread(r'cat.jpg')
        height, width, byteValue = self.cvImage.shape
        byteValue = byteValue * width

        cv2.cvtColor(self.cvImage, cv2.COLOR_BGR2RGB, self.cvImage)

        self.mQImage = QtGui.QImage(self.cvImage, width, height, byteValue, QtGui.QImage.Format_RGB888)
        painter = QtGui.QPainter()
        painter.begin(self.pixmap)
        painter.drawImage(0, 0, self.mQImage)
        painter.end()

        self.game_image_label.setPixmap(self.pixmap)
        self.game_image_label.show()

        if keywordargs.get('gameOn') is False:
            #  Show end game screen.
            print("Game over.")


# ----------------------------------------------------

if __name__ == '__main__':
    client = GameClient()


# while True:
#     key = input('q = Exit, p = Get Ball Position \n')
#     print ("Key entered: " + key)
#
#     if key == 'q':
#         break

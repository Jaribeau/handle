# GameClient

import sys
from PyQt5 import QtGui, QtWidgets, Qt
from GameManager import GameManager
import UserManager
import cv2


class GameClient():
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.current_player = {'name': None, 'id': None}

        self.game = None
        self.game_cv_image = None
        self.game_message = ""
        self.game_time_remaining = 0
        self.game_is_over = True
        self.game_score = 0
        self.game_latency = 0

        # Set label, size, and position
        self.window = QtWidgets.QWidget()
        self.window.setGeometry(10, 200, 600, 800)
        self.window.setWindowTitle("Handle")

        # -- SHARED --
        self.view_label = QtWidgets.QLabel(self.window)
        self.view_label.setText("HANDLE")
        self.view_label.move(500, 20)
        self.view_label.setFixedWidth(600)
        self.view_label.setFont(Qt.QFont("Helvetica [Cronyx]", 70, 30))  # Font family, size, weight



        # -- IN GAME VIEW --
        self.pixmap = QtGui.QPixmap(500, 500)
        self.pixmap.fill(Qt.QColor("white"))
        self.game_image_label = QtWidgets.QLabel(self.window)
        self.game_image_label.setFixedHeight(500)
        self.game_image_label.setFixedWidth(800)
        self.game_image_label.move(500, 260)

        self.game_message_label = QtWidgets.QLabel(self.window)
        self.game_message_label.setText(self.game_message)
        self.game_message_label.move(1100, 275)
        self.game_message_label.setFixedWidth(600)
        self.game_message_label.setFixedHeight(500)
        self.game_message_label.setFont(Qt.QFont("Helvetica [Cronyx]", 70, 30))  # Font family, size, weight

        self.game_score_label = QtWidgets.QLabel(self.window)
        self.game_score_label.setText(("Score: " + str(self.game_score)))
        self.game_score_label.move(500, 20)
        self.game_score_label.setFixedWidth(600)
        self.game_score_label.setFont(Qt.QFont("Helvetica [Cronyx]", 70, 30))  # Font family, size, weight

        self.game_latency_label = QtWidgets.QLabel(self.window)
        self.game_latency_label.setText(("Latency: " + str(self.game_latency)))
        self.game_latency_label.move(5, 50)
        self.game_latency_label.setFixedHeight(100)
        self.game_latency_label.setFixedWidth(200)
        self.game_latency_label.setFont(Qt.QFont("Helvetica [Cronyx]", 10, -1))  # Font family, size, weight

        self.end_game_button = QtWidgets.QPushButton("QUIT", self.window)
        self.end_game_button.setFixedWidth(500)
        self.end_game_button.setFixedHeight(100)
        self.end_game_button.move(500, 150)
        self.end_game_button.clicked.connect(self.end_game)
        self.end_game_button.hide()



        # -- MENU VIEW --
        self.start_game_button = QtWidgets.QPushButton("START GAME", self.window)
        self.start_game_button.setFixedWidth(500)
        self.start_game_button.setFixedHeight(100)
        self.start_game_button.move(500, 150)
        self.start_game_button.clicked.connect(self.start_game)

        self.highscores_table = QtWidgets.QListWidget(self.window)
        self.highscores_table.move(5, 230)

        self.highscores_label = QtWidgets.QLabel(self.window)
        self.highscores_label.move(5, 200)
        self.highscores_label.setText("HIGHSCORES")
        self.highscores_label.setFixedWidth(300)
        self.highscores_label.setFont(Qt.QFont("Helvetica [Cronyx]", 30))  # Font family, size, weight



        # -- SELECT/CREATE PLAYER VIEW --

        self.existing_player_label = QtWidgets.QLabel(self.window)
        self.existing_player_label.move(5, 200)
        self.existing_player_label.setText("EXISTING PLAYER:")
        self.existing_player_label.setFixedWidth(300)
        self.existing_player_label.setFont(Qt.QFont("Helvetica [Cronyx]", 30))  # Font family, size, weight

        self.select_player_dropdown = QtWidgets.QComboBox(self.window)
        self.select_player_dropdown.setFont(Qt.QFont("Helvetica [Cronyx]",20))
        self.select_player_dropdown.setFixedWidth(200)
        self.select_player_dropdown.setFixedHeight(50)
        # self.select_player_dropdown.currentIndexChanged.connect(self.select_player)
        self.select_player_dropdown.move(5, 250)

        self.select_player_button = QtWidgets.QPushButton("SELECT", self.window)
        self.select_player_button.setFixedWidth(75)
        self.select_player_button.setFixedHeight(63)
        self.select_player_button.clicked.connect(self.select_player)
        self.select_player_button.move(205, 246)

        self.new_player_label = QtWidgets.QLabel(self.window)
        self.new_player_label.setText("NEW PLAYER:")
        self.new_player_label.setFixedWidth(300)
        self.new_player_label.setFont(Qt.QFont("Helvetica [Cronyx]", 30))  # Font family, size, weight
        self.new_player_label.move(5, 500)

        self.new_player_txt_input = QtWidgets.QLineEdit(self.window)
        # self.new_player_txt_input.setValidator(QIntValidator())
        self.new_player_txt_input.setMaxLength(20)
        self.new_player_txt_input.setFont(Qt.QFont("Helvetica [Cronyx]",20))
        self.new_player_txt_input.setFixedWidth(200)
        self.new_player_txt_input.setFixedHeight(50)
        self.new_player_txt_input.move(5, 550)

        self.create_player_button = QtWidgets.QPushButton("CREATE", self.window)
        self.create_player_button.setFixedWidth(75)
        self.create_player_button.setFixedHeight(63)
        self.create_player_button.clicked.connect(self.create_player)
        self.create_player_button.move(205, 546)


        self.window.showMaximized()
        self.show_select_player_view()
        sys.exit(self.app.exec_())

    def hide_all_elements(self):
        # self.view_label.hide()
        self.game_image_label.hide()
        self.game_message_label.hide()
        self.game_score_label.hide()
        self.game_latency_label.hide()
        self.start_game_button.hide()
        self.end_game_button.hide()
        self.new_player_txt_input.hide()
        self.create_player_button.hide()
        self.select_player_dropdown.hide()
        self.new_player_label.hide()
        self.existing_player_label.hide()
        self.select_player_button.hide()
        self.highscores_table.hide()
        self.highscores_label.hide()

    def show_select_player_view(self):
        self.view_label.setText("SELECT PLAYER")
        self.hide_all_elements()
        self.new_player_txt_input.show()
        self.create_player_button.show()
        self.select_player_dropdown.show()
        self.new_player_label.show()
        self.existing_player_label.show()
        self.select_player_button.show()

        for player in UserManager.player_list():
            self.select_player_dropdown.addItem(player[1], player[0])

    def create_player(self):
        if self.new_player_txt_input.text() is not None:
            UserManager.create_player(self.new_player_txt_input.text())
        self.new_player_txt_input.setText("")
        self.select_player_dropdown.clear()
        self.show_select_player_view()

    def select_player(self):
        self.current_player['name'] = self.select_player_dropdown.currentText()
        self.current_player['id'] = self.select_player_dropdown.currentData()
        print("PLAYER SELECTED:")
        print(self.current_player)
        self.show_menu_view()

    def show_menu_view(self):
        self.view_label.setText("Welcome, " + str(self.current_player['name']))
        self.hide_all_elements()
        self.start_game_button.show()
        self.highscores_table.show()
        self.highscores_label.show()
        self.show_highscores()

        # for player in UserManager.player_list():
        #     self.select_player_dropdown.addItem(player[1], player[0])

    def show_highscores(self):
        print("HIGH SCORES:")
        i = 1
        for record in UserManager.highscores():
            self.highscores_table.addItem((str(i) + ".  " + str(record[0]) + "  -  " + str(record[1])))
            i += 1

    def show_current_player_scores(self):
        print("MY SCORES!")

    def show_game_view(self):
        self.view_label.setText("GAME ON!")
        self.hide_all_elements()
        self.game_image_label.show()
        self.game_message_label.show()
        self.game_score_label.show()
        self.game_latency_label.show()
        self.end_game_button.show()

        # for player in UserManager.player_list():
        #     self.select_player_dropdown.addItem(player[1], player[0])

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
            self.game_score_label.setText("Score: " + str(self.game_score))

        if keywordargs.get('timeRemaining') is not None:
            self.game_time_remaining = keywordargs.get('timeRemaining')

        if keywordargs.get('gameOn') is False:
            self.game_is_over = not keywordargs.get('gameOn')

            # Show game over screen

        if keywordargs.get('latency') is not None:
            self.game_latency = keywordargs.get('latency')
            self.game_latency_label.setText("Latency:\n" + str(round(self.game_latency, 3)))

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

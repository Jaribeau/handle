# main

mode = "GameClient" # choices: "GameManager", "ObstacleManager", "LaserManager"

if mode == "GameManager":
    from GameManager import GameManager
    
    game = GameManager()
    game.start_game()

elif mode == "GameClient":
    from GameClient import GameClient

    if __name__ == '__main__':
        client = GameClient()

elif mode == "ObstacleManager":
    from ObstacleManager import ObstacleManager

    obstacle = ObstacleManager()
    obstacle.start_movement()
elif mode == "LaserManager":
    from LaserManager import LaserManager
    laser = LaserManager()
    laser.start()

    while True:
        userInput = input('please enter x,y: ')
        userInput = userInput.split(',')
        laser.setPosition(userInput[0],userInput[1])

# while True:
#     True

# GameServer

from GameManager import GameManager


class GameServer:

    def __init__(self):
        self.gameManager = GameManager()
        self.observers = []



    def request(self, title, **body):
        if title == "New Game":
            self.gameManager = GameManager(body.get('time'), "Hard")
            self.gameManager.start_game()
            self.register(body.get("observer"))
            return "Success"


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
            observer.update(*args, **keywordargs)

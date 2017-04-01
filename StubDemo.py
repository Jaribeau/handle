

from BallTrackerStub import BallTracker


class StubDemo:

    def __init__(self):
        print("Creating instance of ball tracker stub.")
        self.stub = BallTracker.get_instance()
        self.stub.register(self)
        self.stub.start_ball_tracking()

    # Observer function called by any observable class that this class registered to
    def notify(self, *args, **keywordargs):

        if keywordargs.get('x') is not None and keywordargs.get('y') is not None:
            print("Ball Location Updated!")



StubDemo()
while(True):
    pass

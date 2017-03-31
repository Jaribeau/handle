
import unittest


class TestLaserManagerMethods(unittest.TestCase):

    def test_to_polar_coords(self):
        from LaserManager import LaserManager
        lm = LaserManager()
        # self.assertEqual(LaserManager.toPolarCoords(0,0), )
        print(lm.toPolarCoords(1,1))


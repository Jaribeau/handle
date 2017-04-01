
import unittest


class TestLaserManagerMethods(unittest.TestCase):

    def runTest(self):
        from LaserManager import LaserManager
        lm = LaserManager()
        # self.assertEqual(lm.toPolarCoords(0, 0), (1.0, 1.0))
        # print(lm.toPolarCoords(1, 1))


class TestUserManager(unittest.TestCase):

    def setUp(self):
        import UserManager
        UserManager.reset_database()

    def runTest(self):
        import UserManager
        # Boundary Value Analysis
        # Class 1: Integer range
        # Class 2: Below integer range (< -2147483648)
        # Class 3: Above integer range (>  2147483647)
        self.assertTrue(UserManager.save_score(14, "Jack", 0))              # Middle
        self.assertTrue(UserManager.save_score(14, "Jack", 2147483647))     # Max
        self.assertTrue(UserManager.save_score(14, "Jack", -2147483648))    # Min
        self.assertFalse(UserManager.save_score(14, "Jack", -2147483649))   # Min - 1
        self.assertFalse(UserManager.save_score(14, "Jack", 2147483648))    # Max + 1
        self.assertFalse(UserManager.save_score(14, "Jack", 'letters'))
        self.assertFalse(UserManager.save_score('', "", ''))
        self.assertFalse(UserManager.save_score('', 55, ''))
        self.assertFalse(UserManager.save_score(None, None, None))
        self.assertFalse(UserManager.save_score(None, "Jack", 5))
        self.assertFalse(UserManager.save_score(14, None, 543))
        self.assertFalse(UserManager.save_score(14, "Jack", None))


class TestCollidesWith(unittest.TestCase):

    def runTest(self):
        from GameManager import GameManager
        gm = GameManager()

        # Statement, branch, condition, and path coverage
        # collides_with(self, ball_position, obstacle_position, radius)

        # Ensure each varying branch path is followed
        self.assertFalse(gm.collides_with((0, 0), (0, 0), 0))
        self.assertTrue(gm.collides_with((0, 0), (0, 0), 10))
        self.assertFalse(gm.collides_with((None, None), (0, 0), 10))
        self.assertFalse(gm.collides_with((0, 0), (None, None), 10))
        self.assertTrue(gm.collides_with((0, 0), (0, 0), None))

        # Collisions, checking that all axis collision combinations are checked
        self.assertTrue(gm.collides_with((5, 5), (4, 4), 1))
        self.assertTrue(gm.collides_with((5, 5), (6, 6), 1))
        self.assertTrue(gm.collides_with((5, 5), (4, 6), 1))
        self.assertTrue(gm.collides_with((5, 5), (6, 4), 1))

        # Non-collisions, checking that all axis non-collision combinations are checked
        self.assertFalse(gm.collides_with((5, 5), (3, 3), 1))
        self.assertFalse(gm.collides_with((5, 5), (7, 7), 1))
        self.assertFalse(gm.collides_with((5, 5), (3, 7), 1))
        self.assertFalse(gm.collides_with((5, 5), (7, 3), 1))
        self.assertFalse(gm.collides_with((5, 5), (5, 3), 1))
        self.assertFalse(gm.collides_with((5, 5), (5, 7), 1))
        self.assertFalse(gm.collides_with((5, 5), (7, 5), 1))
        self.assertFalse(gm.collides_with((5, 5), (3, 5), 1))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestLaserManagerMethods())
    suite.addTest(TestUserManager())
    suite.addTest(TestCollidesWith())
    return suite



# --------------------------------
if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)


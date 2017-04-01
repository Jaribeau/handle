
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
        self.assertTrue(UserManager.save_score(14, "Jack", 543))
        self.assertTrue(UserManager.save_score(14, "Jack", 0))
        self.assertTrue(UserManager.save_score(14, "Jack", 2147483647))     # Max
        self.assertTrue(UserManager.save_score(14, "Jack", -2147483647))    # Min
        self.assertFalse(UserManager.save_score(14, "Jack", 'letters'))
        self.assertFalse(UserManager.save_score('', "", ''))
        self.assertFalse(UserManager.save_score('', 55, ''))
        self.assertFalse(UserManager.save_score(None, None, None))
        self.assertFalse(UserManager.save_score(None, "Jack", 5))
        self.assertFalse(UserManager.save_score(14, None, 543))
        self.assertFalse(UserManager.save_score(14, "Jack", None))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestLaserManagerMethods())
    suite.addTest(TestUserManager())
    return suite



# --------------------------------
if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)


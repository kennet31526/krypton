import unittest
from krypton.auth.users.userModel import standardUser

class userAuth(unittest.TestCase):
    def setUp(self) -> None:
        self.model = standardUser(None)
        self.model.saveNewUser("Test", "TEST")
        return super().setUp()
    def tearDown(self) -> None:
        self.model.loggedin = True
        self.model.delete()
        return super().tearDown()
    def testLoginOut(self):
        self.model.logout()
        self.model.login(pwd="TEST")
    def testResetPWD(self):
        pass
    def testSingleUserEncrypt(self):
        ctext = self.model.encryptWithUserKey("TEST")
        test = self.model.decryptWithUserKey(ctext)
        self.assertEqual(test, b"TEST")
    def testCrossUserEncrypt(self):
        user2 = standardUser(None)
        user2.saveNewUser("user2", "pwd")
        test = user2.encryptWithUserKey("data", ["Test"])
        result = self.model.decryptWithUserKey(test[0][1], test[0][2], "user2")
        user2.delete()
        self.assertEqual(result, b"data")
    def testMFA(self):
        pass
    def testOTP(self):
        pass
    def testDB(self):
        self.model.setData("test", b"TEST_VALUE")
        result = self.model.getData("test")
        self.model.deleteData("test")
        self.assertEqual(result, b"TEST_VALUE")
    def testSessions(self):
        self.model.logout()
        key = self.model.login(pwd="TEST")
        newMod = standardUser(userName="Test")
        newMod.restoreSession(key)
        self.assertTrue(newMod.loggedin)
        newMod.logout()

if __name__ == "__main__":
    unittest.main()

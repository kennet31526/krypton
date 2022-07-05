import unittest
from krypton.basic import Crypto, KMS
from krypton import base
import os

TEST_PWD = "Example"
TEST_TEXT = "Example"
UPDATE_TEST_TEXT = "Example2"

class testKMS(unittest.TestCase):
    def test(self):
        id = "test Key"
        i = KMS()
        k = i.createNewKey(id, "Example")
        a = i.getKey(id, "Example")
        i.removeKey(id, "Example")
        self.assertEqual(len(a), 32)
        self.assertEqual(k, a)

class testCryptoClass(unittest.TestCase):
    def testWriteReadDelete(self):
        test = Crypto()
        a = test.secureCreate(TEST_TEXT,TEST_PWD)
        b = test.secureRead(a,TEST_PWD)
        test.secureDelete(a, TEST_PWD)
        self.assertEqual(TEST_TEXT, b.decode())

    def testWriteUpdateRead(self):
        test = Crypto()
        a = test.secureCreate(TEST_TEXT, TEST_PWD)
        test.secureUpdate(a,UPDATE_TEST_TEXT,TEST_PWD)
        b = test.secureRead(a,TEST_PWD)
        test.secureDelete(a, TEST_PWD)
        self.assertEqual(UPDATE_TEST_TEXT, b.decode())

    def testWriteDelete(self):
        test = Crypto()
        a = test.secureCreate(TEST_TEXT, TEST_PWD)
        test.secureDelete(a, TEST_PWD)
        working = False
        try:
            test.secureRead(a, TEST_PWD)
        except:
            working = True
        self.assertTrue(working)

class testCryptographicUnits(unittest.TestCase):
    def testAES(self):
        k = os.urandom(32)
        r = base._restEncrypt("Hello", k)
        fr = base._restDecrypt(r, k)
        self.assertEqual(fr, b"Hello")
    def testPBKDF2(self):
        kb = base.PBKDF2("abcdrf", os.urandom(12), 100000)
        self.assertIsInstance(kb, bytes)
        self.assertEqual(len(kb), 32)
    def testECCKeyGen(self):
        keys = base.createECCKey()
        self.assertTrue(keys[0].startswith("-----BEGIN EC PRIVATE KEY-----\n") and keys[0].endswith("\n-----END EC PRIVATE KEY-----\n"))
        self.assertTrue(keys[1].startswith("-----BEGIN PUBLIC KEY-----\n") and keys[1].endswith("\n-----END PUBLIC KEY-----\n"))
    def testECDH(self):
        keys = base.createECCKey()
        keys2 = base.createECCKey()
        salt = os.urandom(12)
        key = base.ECDH(keys[0], keys2[1], salt, keylen=32)
        self.assertEqual(len(key), 32)
        self.assertEqual(key, base.ECDH(keys[0], keys2[1], salt, keylen=32))
    def testBase64(self):
        text = "fdgdfgfdgdfsr"
        b64 = base.base64encode(text)
        t = base.base64decode(b64)
        self.assertEqual(text, t.decode())

class testDjangoAuth(unittest.TestCase):
    def testCreateNewUser(self):
        pass
    def testResetPWD(self):
        pass
    def testEncrypt(self):
        pass
    def testDecrypt(self):
        pass
    def testMFA(self):
        pass
    def testOTP(self):
        pass
    def testLoginOut(self):
        pass

if __name__ == "__main__":
    unittest.main()

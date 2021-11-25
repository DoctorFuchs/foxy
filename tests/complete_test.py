from benchmarks import save, speed
from installs import database
import unittest


class tester(unittest.TestCase):
    def testSAVE(self):
        assert save.check() == True

    def testSPEED(self):
        assert speed.check() == True, \
            "SPEED TEST NOT SUCCESSFUL!" +\
            "\nPLEASE MAKE A LONG_SPEED TEST TO GET MORE INFORMATIONS." +\
            "\nIF THE LONG_SPEED TEST IS SUCCESSFUL YOU CAN IGNORE THIS MESSAGE!"

    def testIMPORTDATABASE(self):
        assert database.check() == True

if __name__ == "__main__":
    unittest.main()

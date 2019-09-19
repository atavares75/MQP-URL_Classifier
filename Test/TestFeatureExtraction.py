import unittest

from FeatureExtraction.FeatureExtraction import Extractor


class TestExtractor(unittest.TestCase):
    ex1 = Extractor('https://www.235.353.222.354.com/abou.t.')
    ex2 = Extractor('www.google.co.uk:80')
    ex3 = Extractor('http://www.goog-le.com:600/ab.=out/?domain=goole&username=sugma')
    ex4 = Extractor('http://google.example.com/foo;key1=value1?key2=value2#key3=value3')
    ex5 = Extractor('https://235.353.222.354/about')
    ex6 = Extractor('http://username:password@example.com/')
    ex7 = Extractor(
        'http://target/login.asp?userid=bob%27%3b%20update%20logintable%20set%20passwd%3d%270wn3d%27%3b--%00')
    ex8 = Extractor('https://www.xn--80ak6aa92e.com')

    def test_checkProtocol_1(self):
        r = self.ex1.checkURLProtocol()
        self.assertEqual(r, 0)

    def test_checkProtocol_2(self):
        r = self.ex2.checkURLProtocol()
        self.assertEqual(r, 1)

    def test_checkProtocol_3(self):
        r = self.ex3.checkURLProtocol()
        self.assertEqual(r, 1)

    def test_checkForCharacterInHost_1(self):
        r = self.ex1.checkForCharacterInHost('-')
        self.assertEqual(r, 0)

    def test_checkForCharacterInHost_2(self):
        r = self.ex3.checkForCharacterInHost('-')
        self.assertEqual(r, 1)

    def test_checkForCharacterInPath_1(self):
        r = self.ex1.checkForCharacterInPath('=')
        self.assertEqual(r, 0)

    def test_checkForCharacterInPath_2(self):
        r = self.ex3.checkForCharacterInPath('=')
        self.assertEqual(r, 1)

    def test_countCharacterInURL_1(self):
        r = self.ex1.countCharacterInURL('.')
        self.assertEqual(r, 7)

    def test_countCharacterInURL_2(self):
        r = self.ex2.countCharacterInURL('.')
        self.assertEqual(r, 3)

    def test_countCharacterInHost_1(self):
        r = self.ex1.countCharacterInHost('.')
        self.assertEqual(r, 5)

    def test_countCharacterInHost_2(self):
        r = self.ex2.countCharacterInHost('.')
        self.assertEqual(r, 3)

    def test_countCharacterInPath_1(self):
        r = self.ex1.countCharacterInPath('.')
        self.assertEqual(r, 2)

    def test_countCharacterInPath_2(self):
        r = self.ex2.countCharacterInPath('.')
        self.assertEqual(r, 0)

    def test_checkLength(self):
        # URL doesn't have protocol so '//' is attached in beginning of URL
        r = self.ex2.checkLength()
        self.assertEqual(r, 21)

    def test_checkNonStandardPort_1(self):
        r = self.ex2.checkNonStandardPort()
        self.assertEqual(r, 0)

    def test_checkNonStandardPort_2(self):
        r = self.ex3.checkNonStandardPort()
        self.assertEqual(r, 1)

    def test_checkNonStandardPort_3(self):
        r = self.ex1.checkNonStandardPort()
        self.assertEqual(r, 0)

    def test_checkForFragments_1(self):
        r = self.ex1.checkForFragments()
        self.assertEqual(r, 0)

    def test_checkForFragments_2(self):
        r = self.ex4.checkForFragments()
        self.assertEqual(r, 1)

    def test_checkForQueries_1(self):
        r = self.ex4.checkForQueries()
        self.assertEqual(r, 1)

    def test_checkForQueries_2(self):
        r = self.ex1.checkForQueries()
        self.assertEqual(r, 0)

    def test_checkForParams_1(self):
        r = self.ex1.checkForParams()
        self.assertEqual(r, 0)

    def test_checkForParams_2(self):
        r = self.ex4.checkForParams()
        self.assertEqual(r, 1)

    def test_checkTLD_1(self):
        r = self.ex1.checkTLD()
        self.assertEquals(r, 'com')

    def test_checkTLD_2(self):
        r = self.ex2.checkTLD()
        self.assertEquals(r, 'co.uk')

    def test_checkForIPAddress_1(self):
        r = self.ex1.checkForIPAddress()
        self.assertEqual(r, 0)

    def test_checkForIPAddress_2(self):
        r = self.ex2.checkForIPAddress()
        self.assertEqual(r, 0)

    def test_checkForIPAddress_3(self):
        r = self.ex5.checkForIPAddress()
        self.assertEqual(r, 1)

    def test_checkForUsernameAndPassword_1(self):
        r = self.ex1.checkForUsernameAndPassword()
        self.assertEqual(r, 0)

    def test_checkForUsernameAndPassword_1(self):
        r = self.ex6.checkForUsernameAndPassword()
        self.assertEqual(r, 2)

    def test_checkForDigitsInDomain_1(self):
        r = self.ex2.checkForDigitsInDomain()
        self.assertEqual(r, 0)

    def test_checkForDigitsInDomain_2(self):
        r = self.ex1.checkForDigitsInDomain()
        self.assertEqual(r, 1)

    def test_checkAlexaTop1Million_1(self):
        r = self.ex3.checkAlexaTop1Million()
        self.assertEqual(r, 0)

    def test_checkAlexaTop1Million_2(self):
        r = self.ex2.checkAlexaTop1Million()
        self.assertEqual(r, 1)

    def test_checkSubDomains_1(self):
        r = self.ex2.checkSubDomains()
        self.assertEqual(r, 0)

    def test_checkSubDomains_2(self):
        r = self.ex4.checkSubDomains()
        self.assertEqual(r, 1)

    def test_checkForPunycode_1(self):
        r = self.ex1.checkForPunycode()
        self.assertEqual(r, 0)

    def test_checkForPunycode_2(self):
        r = self.ex8.checkForPunycode()
        self.assertEqual(r, 1)

    def test_addressLocation(self):
        r = self.ex8.addressLocation()
        self.assertEqual(r, 'US')

    def test_dateRegistered(self):
        r = self.ex2.dateRegistered()
        self.assertEqual(r, 'US')


if __name__ == '__main__':
    unittest.main()

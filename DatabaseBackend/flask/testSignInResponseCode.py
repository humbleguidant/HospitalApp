##################################################
## These are the unit tests for the flask app
##################################################
## YearMonthDay: 2021-04-25
## Project: Open Source Engine Integration
## Program Name: testSignInResponseCode.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.1
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 04/25/2021  Aubrey Nickerson            1             Set up first draft.
##################################################
## MIT License
## Copyright 2021 Okanagan College & Harris Healthcare

## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
## associated documentation files (the "Software"), to deal in the Software without restriction, including 
## without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
## copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
## OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
## IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## End license text.
##################################################
## import libraries for testing

import re
from app import application,db
from dbTestModel import Roles,ChatRoom
import unittest
from PyAES import AesCrypto
aes = AesCrypto('ddfbccae-b4c4-11')

# Create Unit testing class
class FlaskTest(unittest.TestCase):
    #check for response 200
    def test_index(self):
        tester = application.test_client(self)
        response = tester.get("/signIn")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
        #self.assertTrue('<h1>Login</h1>')
    
   #Run the unit test 
if __name__ == "__main__":
    unittest.main()
##################################################
## These are the unit tests for the flask app
##################################################
## YearMonthDay: 2021-03-04
## Project: Open Source Engine Integration
## Program Name: test.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.3
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 03/05/2021  Bao Mai            1             Set up first draft.
## 03/06/2021  Bao Mai            2             Add create_app(), setUp(), tearDown()
## 03/07/2021  Bao Mai            3             Add test_index(), test_login(), test_password_encryption(), 
##                                              test_password_decryption(), test_chat_room()
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
    # Set up the backend of the app
    def create_app(self):
        application.config.from_object('config.TestConfig')
        return application
    #Connect to the database
    def setUp(self):
        # Creates a test client
        application.config['TESTING'] = True
        application.config['WTF_CSRF_ENABLED'] = False
        application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://python-user:QJMR6.))iTY,@10.1.144.91/OpenSourceEngDB'
        application.config['SQLALCHEMY_ECHO'] = True
        self.app = application.test_client()
        self.app.testing = True 
        # Add dummy data to test. 
        db.create_all()
        db.session.add(Roles("mikey@gmail.com","letmein"))
        db.session.add(ChatRoom(3122,None,31,22))
        db.session.commit()
        
       # Destroy the session 
    def tearDown(self):
        db.session.remove()
        db.drop_all()
 
    #check for response 200
    def test_index(self):
        tester = application.test_client(self)
        response = tester.get("/signIn")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
        #self.assertTrue('<h1>Login</h1>')
    
    # Check if the user logs in
    def test_login(self):
        response = self.app.post("/signIn",
                                 data = {"email":"mikey@gmail.com","password":"letmein"},
                                 follow_redirects=True)
        self.assertEqual(response.status_code,200)

    # Test if the encryption works
    def test_password_encryption(self):
        user = Roles.query.filter_by(email='mikey@gmail.com').first()
        self.assertEqual(user.password, aes.encrypt('letmein'))
        #need to fix the \t\t\t\t\t\t\t\
    
    # Test if the decryption works
    def test_password_decryption(self):
        user = Roles.query.filter_by(email='mikey@gmail.com').first()        
        self.assertEqual(''.join(e for e in aes.decrypt(str(user.password)) if e.isalnum()),'letmein')

    # Test if the DB checks that the chat room exists between a doctor and an admin.       
    def test_chat_room_admin_doctor(self):
        response = self.app.get("/checkChatID/"+aes.encrypt(str(3122))+"/"+aes.encrypt(str(31))+"/"+aes.encrypt("Doctor")+"/"+aes.encrypt(str(22))+"/"+aes.encrypt("Administrator"))
        chatRoom = ChatRoom.query.filter_by(chat_id = 3122).first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(chatRoom.chat_id, 3122)
        self.assertEqual(chatRoom.doctor_id, 31)
        self.assertEqual(chatRoom.admin_id, 22)
        self.assertEqual(chatRoom.patient_id, None)

    # Test if the DB checks that the chat room exists between a doctor and a patient.
    def test_chat_room_patient_doctor(self):
        response = self.app.get("/checkChatID/"+aes.encrypt(str(5431))+"/"+aes.encrypt(str(54))+"/"+aes.encrypt("Patient")+"/"+aes.encrypt(str(31))+"/"+aes.encrypt("Doctor"))
        chatRoom = ChatRoom.query.filter_by(chat_id = 3122).first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(chatRoom.chat_id, 3122)
        self.assertEqual(chatRoom.doctor_id, 31)
        self.assertEqual(chatRoom.admin_id, 22)
        self.assertEqual(chatRoom.patient_id, None)

    # Test if the DB checks that the chat room exists between a patient and an admin.
    def test_chat_room_patient_administrator(self):
        response = self.app.get("/checkChatID/"+aes.encrypt(str(5422))+"/"+aes.encrypt(str(54))+"/"+aes.encrypt("Patient")+"/"+aes.encrypt(str(22))+"/"+aes.encrypt("Administrator"))
        chatRoom = ChatRoom.query.filter_by(chat_id = 3122).first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(chatRoom.chat_id, 3122)
        self.assertEqual(chatRoom.doctor_id, 31)
        self.assertEqual(chatRoom.admin_id, 22)
        self.assertEqual(chatRoom.patient_id, None)
   #Run the unit test 
if __name__ == "__main__":
    unittest.main()
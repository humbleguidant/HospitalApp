##################################################
## These are the class models for testing the database 
## in unit testing. 
##################################################
## YearMonthDay: 2021-03-03
## Project: Open Source Engine Integration
## Program Name: dbTestModel.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.2
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 03/05/2021  Bao Mai            1             Create Roles model
## 03/06/2021  Bao Mai            2             Create Chat Room model
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
# Import libraries
from flask_sqlalchemy import SQLAlchemy
from app import db,aes
# Class for Roles table
class Roles(db.Model):
  __tablename__ = "Roles"
  
  user_id = db.Column(db.Integer,primary_key =True)
  email = db.Column(db.String(2056))
  last_name = db.Column(db.String(50))
  first_name = db.Column(db.String(50))
  password = db.Column(db.String(2056))
  role = db.Column(db.String(30))
  is_active = db.Column(db.Integer)
  
  def __init__(self, email, password):
        self.email = email
        self.password = aes.encrypt(password)
  def is_authenticated(self):
        return True

  def is_active(self):
        return True

  def is_anonymous(self):
        return False

  def get_id(self):
        return unicode(self.id)

  def __repr__(self):
        return '<name - {}>'.format(self.name)

# Class for Chat Room table    
class ChatRoom(db.Model):
    __tablename__ = "ChatRoom"
    
    chat_id = db.Column(db.Integer,primary_key =True)
    patient_id = db.Column(db.Integer,nullable = True)
    doctor_id = db.Column(db.Integer,nullable = True)
    admin_id = db.Column(db.Integer,nullable = True)
    
    def __init__(self, chat_id,patient_id,doctor_id,admin_id):
        self.chat_id = chat_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.admin_id = admin_id
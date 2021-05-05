##################################################
## This program handles the back end and receives user 
## input of the application. Any user input coming from the
## application will be handled here.
##################################################
## YearMonthDay: 2020-11-02
## Project: Open Source Engine Integration
## Program Name: app.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.14
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 11/02/2020  Aubrey Nickerson   1             Set up first draft.
## 11/08/2020  Aubrey Nickerson   2             Connect to database.
## 11/13/2020  Aubrey Nickerson   3             Send data to front end.
## 11/30/2020  Aubrey Nickerson   4             Create function to get sorted messages.
## 02/06/2021  Aubrey Nickerson   5             Install SocketIO packages and implement chat channel
## 02/07/2021  Aubrey Nickerson   6             Add /getChatHistory route
## 02/08/2021  Aubrey Nickerson   7             Add 'message' socketio function to handle real time messages
## 02/09/2021  Aubrey Nickerson   8             Add /checkSession, /getSession, /destroySession for login functionality
## 03/03/2021  Aubrey Nickerson   9             Add encryption to all functions.
## 03/05/2021  Aubrey Nickerson   10            Change search functionality for searchPatient()
## 03/23/2021  Aubrey Nickerson   11            Add getPatientInfo() route
## 03/24/2021  Aubrey Nickerson   12            Change /schedule function
## 03/26/2021  Aubrey Nickerson   13            Add checkUserMainMenu()
## 04/02/2021  Aubrey Nickerson   14            Insert SIU messages to DB.
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

# Import the necessary libraries to make the program work.
# flask is what makes the program run on the server.
# flask_cors handles the user input from the application.
# dbQuerys handles the database functionality.
import dbQuerys
from datetime import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from PyAES import AesCrypto
from flask_sqlalchemy import SQLAlchemy
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
application.config.update(SECRET_KEY="b_5#y2LF4Q8znxec]")
socketio = SocketIO(application, cors_allowed_origins="*")
aes = AesCrypto('ddfbccae-b4c4-11')
db = SQLAlchemy(application)

# This function gets (GET) the user input from the login
# page and passes the input to the dbQuerys.getUsername() 
# function to check if the user exists. It then returns the
# status back to the application whether the user exists or not.
@application.route("/signIn", methods=['GET', 'POST'])
@cross_origin()
def signIn():
  email = request.args.get("email")
  password = request.args.get("password")
  status = dbQuerys.getEmail(email, password)
  if status != "This email does not exist in the system. Please contact administration." and status != "The password is incorrect. Please try again or contact administration.":
    session["userid"] = status[0][0]
    session["email"] = status[0][1]
    session["lastName"] = status[0][2]
    session["firstName"] = status[0][3]
    session["role"] = status[0][4]
    return str(status[0][4])
  return str(status)

## This function checks if the user is logged in or not.
## If the user is not logged in then the server will return
## "User is not logged in" to the client side of the app
## and the app will redirect the user to the login page. 
## Otherwise the user can proceed
@application.route("/checkSession", methods=['GET'])
@cross_origin()
def checkSession():
  if session.get("userid") is None:
    return "User is not logged in."
  return "All good"

## This function checks the main menu to see if the user
## is an admin, patient, or doctor
@application.route("/checkUserMainMenu", methods=['GET'])
@cross_origin()
def checkUserMainMenu():
  if session.get("userid") is None:
    return "User is not logged in."
  role = dbQuerys.checkRole(session.get("userid"))
  return str(role[1])

## This function gets the AJAX call from the client side of
## the app and calls the database query getSchedule to get
## the schedule information for the user. 
@application.route("/schedule", methods=['GET'])
@cross_origin() 
def getSchedule():
  rowData = []
  grabData = ""
  if request.args.get("patientID") is not None:
    grabData = dbQuerys.getSchedule(''.join(e for e in aes.decrypt(request.args.get("patientID")) if e.isalnum())) 
    if grabData is None:
      return jsonify(None)
    for index, tuple in enumerate(grabData):
      rowData.append((aes.encrypt(tuple[0]), 
                      aes.encrypt(tuple[1]), 
                      aes.encrypt(tuple[2]), 
                      aes.encrypt(tuple[3]), 
                      aes.encrypt(tuple[4]), 
                      aes.encrypt(str(tuple[5])), 
                      aes.encrypt(str(tuple[6])), 
                      aes.encrypt(str(tuple[7])), 
                      aes.encrypt(str(tuple[8])), 
                      aes.encrypt(str(tuple[9])), 
                      aes.encrypt(str(tuple[10]))))
    return jsonify(rowData)

  if session.get("userid") is None: 
    return "User is not logged in."
  sessionID = session.get("userid")
  grabData = dbQuerys.getSchedule(sessionID)
  if grabData is None:
    return jsonify(None)
    
  for index, tuple in enumerate(grabData):
    rowData.append((aes.encrypt(tuple[0]), 
                    aes.encrypt(tuple[1]), 
                    aes.encrypt(tuple[2]), 
                    aes.encrypt(tuple[3]), 
                    aes.encrypt(tuple[4]), 
                    aes.encrypt(str(tuple[5])), 
                    aes.encrypt(str(tuple[6])), 
                    aes.encrypt(str(tuple[7])), 
                    aes.encrypt(str(tuple[8])), 
                    aes.encrypt(str(tuple[9])), 
                    aes.encrypt(str(tuple[10])), 
                    aes.encrypt(tuple[11])))
  return jsonify(rowData)

## This function checks if the session id exists
## and gets the user ID from the database.
## If the session is not set then the client side of 
## the app redirects the user to the login page. If
## it does exist then the user ID is returned to the 
## front end. 
@application.route("/getSession", methods=['GET'])
@cross_origin()
def getSession():
  if session.get("userid") is None:
    return "User is not logged in."
  sessionID = session.get("userid")
  userID = dbQuerys.getUserID(sessionID)
  return jsonify(aes.encrypt(str(userID)))

## This function destroys the user session as soon as
## they are on the login page. If there is no session ID
## then nothing happens.
@application.route("/destroySession", methods=['GET'])
@cross_origin()
def destroySession():
  if session.get("userid") is None and session.get("email") is None and session.get("lastName") is None and session.get("firstName") is None and session.get("role") is None: 
    return "All good"
  session.pop("userid")
  session.pop("email")
  session.pop("lastName")
  session.pop("firstName")
  session.pop("role")
  return "All good"

## This function gets the AJAX call from the chatRoomSelectPage.js
## file and checks the role of the logged in user if they are a patient
## admin or doctor. It does so by calling the checkRole query in dbQuerys.py
@application.route("/getRole", methods=['GET'])
@cross_origin()
def getRole():
  if session.get("userid") is None:
    return "User is not logged in."
  sessionID = session.get("userid")
  record = dbQuerys.checkRole(sessionID)
  rowData = [aes.encrypt(str(record[0])), record[1]]
  return jsonify(rowData)

## This function gets the AJAX call from the chatRoomSelectPage.js
## to get all adminstrators from the database whether the user is a
## patient or a doctor.
@application.route("/getAdmin", methods=['GET'])
@cross_origin()
def getAdmin():
  rowData = []
  records = ""
  if session.get("role") == "Patient":
    records = dbQuerys.searchForAdministrator()
  elif session.get("role") == "Doctor":
    records = dbQuerys.searchForAdministrator()
  if records is None:
    return jsonify(None)
  for index, tuple in enumerate(records):
    rowData.append((aes.encrypt(str(tuple[0])), aes.encrypt(tuple[1]), aes.encrypt(tuple[2])))
  return jsonify(rowData)

## This function gets the AJAX call from the chatRoomSelectPage.js
## to get Doctors from the database. If the user is a patient
## then the database will only get the doctors associated with 
## the patient. If the user is an administrator then the database
## will get all doctors to display for the user. 
@application.route("/getDoctors", methods=['GET'])
@cross_origin()
def getDoctors():
  rowData = []
  records = ""
  if session.get("role") == "Patient":
    userID = session.get("userid")
    records = dbQuerys.searchForDoctors(userID)
  elif session.get("role") == "Administrator":
    records = dbQuerys.searchForAllDoctors()
  if records is None:
    return jsonify(None)
  for index, tuple in enumerate(records):
    rowData.append((aes.encrypt(str(tuple[0])), aes.encrypt(tuple[1]), aes.encrypt(tuple[2])))
  return jsonify(rowData)

## This function gets the AJAX call from the chatRoomSelectPage.js
## to get Patients from the database. If the user is a doctor
## then the database will only get the patients associated with 
## the doctor. If the user is an administrator then the database
## will get all patients to display for the user.
@application.route("/getPatients", methods=['GET'])
@cross_origin()
def getPatients():
  rowData = []
  records = ""
  if session.get("role") == "Doctor":
    userID = session.get("userid")
    records = dbQuerys.searchForPatients(userID)
  elif session.get("role") == "Administrator":
    records = dbQuerys.searchForAllPatients()
  if records is None:
    return jsonify(None)
  for index, tuple in enumerate(records):
    rowData.append((aes.encrypt(str(tuple[0])), aes.encrypt(tuple[1]), aes.encrypt(tuple[2])))
  return jsonify(rowData) 

## This function gets the AJAX call from the chat.js file so that it can
## check if there is a chat room that already exists.
@application.route("/checkChatID/<chatID>/<userID>/<userRole>/<callerID>/<callerRole>", methods=['GET', 'POST'])
@cross_origin()
def checkChatID(chatID, userID, userRole, callerID, callerRole):
  chatID = ''.join(e for e in aes.decrypt(chatID) if e.isalnum())
  userID = ''.join(e for e in aes.decrypt(userID) if e.isalnum())
  userRole = ''.join(e for e in aes.decrypt(userRole) if e.isalnum())
  callerID = ''.join(e for e in aes.decrypt(callerID) if e.isalnum())
  callerRole = ''.join(e for e in aes.decrypt(callerRole) if e.isalnum())
  dbQuerys.checkChatRoom(chatID, userID, userRole, callerID, callerRole)
  return "All good"

## This function gets the AJAX call from the chat.js file so that it can
## get the chat history and send to the client side of the app. 
@application.route("/getChatHistory/<chatID>")
@cross_origin()
def getChatHistory(chatID):
  messages = dbQuerys.getChatMessages(''.join(e for e in aes.decrypt(chatID) if e.isalnum()))
  return jsonify(messages)

## This function handles the socketio messages coming from the 
## Javascript side of the app. This function passes the values of
## the message to the database query and returns the message back
## to the client side of the app to display.
@socketio.on('message')
def handleMessage(msg):
  dbQuerys.insertChatMessage(''.join(e for e in aes.decrypt(msg['chatID']) if e.isalnum()), 
                            ''.join(e for e in aes.decrypt(msg['ID']) if e.isalnum()), 
                            msg['userMessage'], 
                            aes.decrypt(msg['currentTime'])[:18])
  decryptTime = aes.decrypt(msg['currentTime'])[:18]
  convertStringToDate = datetime.strptime(decryptTime, "%Y-%m-%d %H:%M:%S")
  formatAndEncryptTime = aes.encrypt(convertStringToDate.strftime("%m/%d/%Y %H:%M"))
  emit('message', 
      {
        'chatID': msg['chatID'], 
        'ID' : msg['ID'], 
        'userMessage': msg['userMessage'], 
        'currentTime': formatAndEncryptTime
      }, 
      broadcast=True)

# This function gets (GET) the user input from the search
# patient page and passes the input to dbQuerys.getPatientData()
# It then returns the status to the application.
@application.route("/searchPatient", methods=['GET'])
@cross_origin()
def searchPatient():
  rowData = []
  patientRecords = dbQuerys.getPatientData()
  for index, tuple in enumerate(patientRecords):
    rowData.append((aes.encrypt(tuple[0]), 
                    aes.encrypt(tuple[1]), 
                    aes.encrypt(str(tuple[2])), 
                    aes.encrypt(tuple[3]), 
                    aes.encrypt(tuple[4]),
                    aes.encrypt(str(tuple[5]))))
  return jsonify(rowData)
  
# This function gets (GET) the user input from the search
# patient page and passes the input to dbQuerys.getPatientData()
# It then returns the status to the application.
@application.route("/searchDoctor", methods=['GET'])
@cross_origin()
def searchDoctor():
  rowData = []
  records = dbQuerys.getDoctorData()
  for index, tuple in enumerate(records):
    rowData.append((aes.encrypt(tuple[0]),
                    aes.encrypt(tuple[1]),
                    aes.encrypt(str(tuple[2]))))
  return jsonify(rowData)

# This function gets (GET) the patient info from the database.
@application.route("/getPatientInfo/<patientID>", methods=['GET'])
@cross_origin()
def getPatientInfo(patientID):
  status = dbQuerys.getPatientDetails(''.join(e for e in aes.decrypt(patientID) if e.isalnum()))
  rowData = [(aes.encrypt(str(status[0][0])), 
              aes.encrypt(status[0][1]), 
              aes.encrypt(status[0][2]), 
              aes.encrypt(str(status[0][3])), 
              aes.encrypt(str(status[0][4])), 
              aes.encrypt(str(status[0][5])),
              aes.encrypt(str(status[0][6])), 
              aes.encrypt(str(status[0][7])), 
              aes.encrypt(str(status[0][8])), 
              aes.encrypt(str(status[0][9])), 
              aes.encrypt(str(status[0][10])), 
              aes.encrypt(str(status[0][11])), 
              aes.encrypt(str(status[0][12])))]
  return jsonify(rowData)

# This function gets (GET) the patients medical information from the database.
@application.route("/displayOrderMessage")
@cross_origin()
def displayOrderMessage():
  status = dbQuerys.getOrderMessage(''.join(e for e in aes.decrypt(request.args.get("patientID")) if e.isalnum()))
  if status is None:
    return "Nothing"
  rowData = [(aes.encrypt(status[0][0]), 
              aes.encrypt(status[0][1]), 
              aes.encrypt(status[0][2]), 
              aes.encrypt(status[0][3]), 
              aes.encrypt(status[0][4]),
              aes.encrypt(status[0][5]),
              aes.encrypt(status[0][6]))]
  return jsonify(rowData)

# This function gets (GET) the user input from the Occupancy
# Details page and passes the input to dbQuerys.getLocationDetails()
# It then returns the status to the application.
@application.route("/searchLocation", methods=['GET'])
@cross_origin()
def searchLocation():
  rowData = []
  records = dbQuerys.getLocationDetails()
  for index, tuple in enumerate(records):
    rowData.append((aes.encrypt(tuple[0]), 
                    aes.encrypt(tuple[1]),
                    aes.encrypt(tuple[2]),
                    aes.encrypt(tuple[3]),
                    aes.encrypt(tuple[4])))
  return jsonify(rowData)
  
# This function gets (GET) the user input from the Occupancy
# Overview page and passes the input to dbQuerys.getLocationOverview()
# It then returns the status to the application.
@application.route("/searchLocationOverview", methods=['GET'])
@cross_origin()
def searchLocationOverview():
  rowData = []
  records = dbQuerys.getLocationOverview()
  for index, tuple in enumerate(records):
    rowData.append((aes.encrypt(tuple)))
  return jsonify(rowData)
  

# This function gets (GET) the user input from the search
# patient page and passes the input to dbQuerys.getPatientData()
# It then returns the status to the application.
@application.route("/getDoctorPatients/<docID>", methods=['GET'])
@cross_origin()
def getDoctorPatients(docID):
  rowData = []
  patientRecords = dbQuerys.getPatientData2(''.join(e for e in aes.decrypt(docID) if e.isalnum()))
  for index, tuple in enumerate(patientRecords):
    rowData.append((aes.encrypt(tuple[0]), 
                    aes.encrypt(tuple[1]), 
                    aes.encrypt(str(tuple[2])), 
                    aes.encrypt(tuple[3]), 
                    aes.encrypt(tuple[4])))
  return jsonify(rowData)

# This function gets the newly created json file from
# the listener.
@application.route("/sendFile", methods=['GET', 'POST'])
@cross_origin()
def sendFile():
  document = request.files['document']
  dbQuerys.insertMessages(document)                                                                                            
  return "Success"

# Run the program
if __name__ == "__main__":
  socketio.run(application, debug=True)
  
##################################################
## This program handles the back end and receives user 
## input of the application. Any user input coming from the
## application will be handled here.
##################################################
## YearMonthDay: 2020-11-02
## Project: Open Source Engine Integration
## Program Name: application.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2020
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: Harris Smartworks
## Version: 1.0.6
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 11/02/2020  Aubrey Nickerson   1             Set up first draft.
## 11/08/2020  Aubrey Nickerson   2             Connect to database.
## 11/13/2020  Aubrey Nickerson   3             Send data to front end.
## 11/30/2020  Aubrey Nickerson   4             Create function to get sorted messages.
## 02/06/2021  Aubrey Nickerson   5             Install SocketIO packages and implement chat channel
##################################################
"""
MIT License
Copyright 2020 Okanagan College & Harris

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, including 
without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

End license text.
"""
# Imports the necessary libraries to make the program work.
# flask is what makes the program run on the server.
# flask_cors handles the user input from the application.
# dbQuerys handles the database functionality.
from datetime import datetime
from flask import Flask, request, jsonify, session
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit, join_room
import dbQuerys
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'
application.config.update(SECRET_KEY="b_5#y2LF4Q8znxec]")
socketio = SocketIO(application, cors_allowed_origins="*")

# This function gets (GET) the user input from the login
# page and passes the input to the dbQuerys.getUsername() 
# function to check if the user exists. It then returns the
# status back to the application whether the user exists or not.
@application.route("/signIn", methods=['GET'])
@cross_origin()
def signIn():
  email = request.args.get('email')
  password = request.args.get('password')
  status = dbQuerys.getEmail(email, password)
  if status != "This email does not exist in the system. Please contact administration." and status != "The password is incorrect. Please Try again or contact Administration.":
    session["userid"] = status[0][0]
    session["email"] = status[0][1]
  return jsonify(status)

@application.route("/checkSession", methods=['GET'])
@cross_origin()
def checkSession():
  if session.get("userid") is None:
    return "User is not logged in."
  print(session.get("userid"))
  return "All good"

@application.route("/getSession", methods=['GET'])
@cross_origin()
def getSession():
  if session.get("userid") is None:
    return "User is not logged in."
  sessionID = session.get("userid")
  userID = dbQuerys.getUserID(sessionID)
  return jsonify(userID)

@application.route("/destroySession", methods=['GET'])
@cross_origin()
def destroySession():
  session.pop("userid")
  session.pop("email")
  return "All good"

@application.route("/getChatHistory")
@cross_origin()
def getChatHistory():
  messages = dbQuerys.getChatMessages()
  return jsonify(messages)

@socketio.on('message')
def handleMessage(msg):
  userID = session.get("userid")
  now = datetime.now()
  formatDateTime = now.strftime("%m/%d/%Y %H:%M:%S")
  recentMessageRow = dbQuerys.insertChatMessage(userID, msg)
  print("Yo yo yo: " + str(recentMessageRow[0][0]))
  emit('message', {'ID' : recentMessageRow[0][0], 'userMessage': str(recentMessageRow[0][1]), 'currentTime': formatDateTime})

# This function gets (GET) the user input from the search
# patient page and passes the input to dbQuerys.getPatientData()
# It then returns the status to the application.
@application.route("/searchPatient", methods=['GET'])
@cross_origin()
def searchPatient():
  lastNameInput = request.args.get('lastName')
  firstNameInput = request.args.get('firstName')
  status = dbQuerys.getPatientData(lastNameInput, firstNameInput)
  return jsonify(status)

# This function gets the newly created json file from
# the listener.
@application.route("/sendFile", methods=['GET', 'POST'])
@cross_origin()
def sendFile():
  dbQuerys.insertMessages(request.files['document'])                                                                                            
  return "Success"

# Run the program
if __name__ == "__main__":
  socketio.run(application, debug=True)
  
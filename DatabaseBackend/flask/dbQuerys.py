##################################################
## This program handles all of the database functionality.
## It receives requests from the app and calls the database
## to get the data and checks if there are any records related to 
## the user input.
##################################################
## YearMonthDay: 2020-11-02
## Project: Open Source Engine Integration
## Program Name: dbQuerys.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.14
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author                            Revision      What was changed?
## 11/02/2020  Aubrey Nickerson                  1             Create JSON functions.
## 11/18/2020  Aubrey Nickerson                  2             Create getUsername() function.
## 11/20/2020  Aubrey Nickerson                  3             Create getPatientData() function.
## 12/01/2020  Aubrey Nickerson                  4             Create insertMessages() and other insert functions.
## 02/14/2021  Aubrey Nickerson                  5             Add getUserID() function to get the user id who logged in.
## 02/15/2021  Aubrey Nickerson                  6             Add getChatMessages() and insertChatMessage() to store and read messages between users.
## 02/18/2021  Aubrey Nickerson, Derek Manchee   7             Created searchForAdministrator(), searchForDoctors(), searchForAllDoctors(), searchForPatients(), and searchForAllPatients().
## 02/19/2021  Aubrey Nickerson, Derek Manchee   8             Created checkRole() and checkChatRoom().
## 02/19/2021  Bao Mai                           9             Created getSchedule()   
## 03/03/2021  Aubrey Nickerson                  10            Changed checkChatRoom()
## 03/05/2021  Aubrey Nickerson                  11            Added encryption functionality
## 03/23/2021  Aubrey Nickerson                  12            Add insertSchedulingActivity() and getPatientDetails() functions.
## 03/24/2021  Aubrey Nickerson, Derek Manchee   13            Edit getShcedule()     
## 04/02/2021  Aubrey Nickerson, Derek Manchee   14            Insert SIU messages to database.
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
## Import database configuration
import dbconfig
import json

## This function gets the data from the ROLES database table depending on 
## the user input from the app. If the user input matches in the database
## then it returns the user data to the client side to proceed to the next page
## If the user does not exist or if the password is incorrect then it will either return 
## "The email does not exist. Please contact administration" or "The password is 
## incorrect. Please try again or contact administration"
def getEmail(email, password):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = "SELECT * FROM ROLES WHERE EMAIL = %s"
    myCursor.execute(sqlQuery, (email,))
    record = myCursor.fetchone()
    if not record:
        return "This email does not exist in the system. Please contact administration."
    if password != record[4]:
        return "The password is incorrect. Please try again or contact administration."    
    grabData = [(record[0], record[1], record[2], record[3], record[5])]
    myCursor.close()
    myDB.close()
    return grabData

## This function performs a select query to get the schedule of the logged in 
## patient or doctor. If there are no schedules then it will return nothing to 
## the client side. If there are schedules associated with the user then it will
## append the data to an array and return it to the client side of the app.
## The client side will display the data in HTML format
def getSchedule(userID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = ""
    role = checkRole(userID)
    if role[1] == "Patient":
        sqlQuery =  "SELECT P.PATIENTGIVENNAME, P.PATIENTFAMILYNAME, PV.ATTENDING_DOCTOR_GIVEN_NAME, "
        sqlQuery += "       PV.ATTENDING_DOCTOR_FAMILY_NAME, SAI.APPOINTMENT_TYPE, SAI.APPOINTMENT_REASON, "
        sqlQuery += "       SAI.APPOINTMENT_TYPE, SAI.APPOINTMENT_DURATION, SAI.APPOINTMENT_DURATION_UNITS, "
        sqlQuery += "       TQ.START_DATE_TIME, TQ.END_DATE_TIME "
        sqlQuery += "FROM SCHEDULING_ACTIVITY_INFORMATION SAI, TIMING_QUANTITY TQ, "
        sqlQuery += "     PATIENTIDENTIFICATION P, PATIENTVISITS PV "
        sqlQuery += "WHERE TQ.SCHEDULE_ID = SAI.SCHEDULE_ID AND "
        sqlQuery += "      SAI.PATIENT_ID = %s AND "
        sqlQuery += "      P.PATIENTID = %s AND "
        sqlQuery += "      PV.PATIENT_ID = %s"
        myCursor.execute(sqlQuery,(userID, userID, userID))
        records = myCursor.fetchall()
    elif role[1] == "Doctor":
        sqlQuery =  "SELECT P.PATIENTGIVENNAME, P.PATIENTFAMILYNAME, "
        sqlQuery += "       SAI.OCCURENCE_NUMBER, SAI.EVENT_REASON, SAI.SCHEDULE_ID, "
        sqlQuery += "       SAI.APPOINTMENT_REASON, SAI.APPOINTMENT_TYPE, "
        sqlQuery += "       SAI.APPOINTMENT_DURATION, SAI.APPOINTMENT_DURATION_UNITS, "
        sqlQuery += "       TQ.START_DATE_TIME, TQ.END_DATE_TIME "
        sqlQuery += "FROM SCHEDULING_ACTIVITY_INFORMATION SAI, TIMING_QUANTITY TQ, "
        sqlQuery += "     PATIENTVISITS PV, PATIENTIDENTIFICATION P "
        sqlQuery += "WHERE TQ.SCHEDULE_ID = SAI.SCHEDULE_ID AND "
        sqlQuery += "      SAI.PATIENT_ID = PV.PATIENT_ID AND "
        sqlQuery += "      P.PATIENTID = PV.PATIENT_ID AND "
        sqlQuery += "      PV.ATTENDING_DOCTOR_PERSON_IDENTIFIER = %s"
        myCursor.execute(sqlQuery,(userID,))
        records = myCursor.fetchall()
    grabData = []
    if not records:
        return None
    for row in records:
        grabData.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9].strftime("%m/%d/%Y %H:%M"), row[10], role[1]))
    myCursor.close()
    myDB.close()
    return grabData

## This function gets the user id of the logged in user by performing
## a select query and returning the data to the client side of the app. 
def getUserID(userID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = "SELECT USER_ID FROM ROLES WHERE USER_ID = %s"
    myCursor.execute(sqlQuery, (userID,))
    record = myCursor.fetchone()
    myCursor.close()
    myDB.close()
    return record[0]

## This function performs a select query to check the role of the 
## logged in user. IF they are a patient, doctor, admin, and so on. 
def checkRole(userID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = "SELECT USER_ID, ROLE FROM ROLES WHERE USER_ID = %s"
    myCursor.execute(sqlQuery, (userID,))
    record = myCursor.fetchone()
    myCursor.close()
    myDB.close()
    return record

## This function performs a select query to get all the administrators
## in the database. If there are no administrators then it will return
## nothing to the client side of the app. If there are administrators then
## append all of them to an array and return the array to the client side of the
## app. The client side will display the array in HTML format with JavaScript.
def searchForAdministrator():
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    grabData = []
    sqlQuery = " SELECT USER_ID, LAST_NAME, FIRST_NAME "
    sqlQuery += "FROM ROLES "
    sqlQuery += "WHERE ROLE = 'Administrator' "
    sqlQuery += "ORDER BY LAST_NAME"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    if not record:
        return None
    for row in record:
        grabData.append((row[0], row[1], row[2]))
    myCursor.close()
    myDB.close()
    return grabData

## This function performs a select query to get the doctors associated with
## the user logged into the app. If there are no doctors then it will return
## nothing to the client side of the app. If there are doctors then it will
## append all the doctors to an array and return the array to the client side of the
## app. The client side will display the array in HTML format with JavaScript.
def searchForDoctors(userID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    grabData = []
    sqlQuery = " SELECT ATTENDING_DOCTOR_PERSON_IDENTIFIER, "
    sqlQuery += "       ATTENDING_DOCTOR_FAMILY_NAME, "
    sqlQuery += "       ATTENDING_DOCTOR_GIVEN_NAME "
    sqlQuery += "FROM PATIENTVISITS "
    sqlQuery += "WHERE PATIENT_ID = %s "
    sqlQuery += "ORDER BY ATTENDING_DOCTOR_FAMILY_NAME"
    myCursor.execute(sqlQuery, (userID,))
    record = myCursor.fetchall()
    if not record:
        return None
    for row in record:
        grabData.append((row[0], row[1], row[2]))
    myCursor.close()
    myDB.close()
    return grabData

## This function performs a select query to get all the doctors in the database
## If there are no doctors then it will return nothing to the client side of the 
## app. If there are doctors then it will append all the doctors to an array and 
## return the array to the client side of the app. The client side will display 
## the array in HTML format with JavaScript.
def searchForAllDoctors():
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    grabData = []
    sqlQuery = " SELECT USER_ID, LAST_NAME, FIRST_NAME "
    sqlQuery += "FROM ROLES "
    sqlQuery += "WHERE ROLE = 'Doctor' "
    sqlQuery += "ORDER BY LAST_NAME"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    if not record:
        return None
    for row in record:
        grabData.append((row[0], row[1], row[2]))
    myCursor.close()
    myDB.close()
    return grabData

## This function performs a select query to get the patients associated with
## the user logged into the app. If there are no patients then it will return
## nothing to the client side of the app. If there are patients then it will
## append all the patients to an array and return the array to the client side of the
## app. The client side will display the array in HTML format with JavaScript.
def searchForPatients(userID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    grabData = []
    sqlQuery = " SELECT USER_ID, LAST_NAME, FIRST_NAME "
    sqlQuery += "FROM ROLES R, PATIENTVISITS P "
    sqlQuery += "WHERE P.PATIENT_ID = R.USER_ID AND "
    sqlQuery += "      R.ROLE = 'Patient' AND "
    sqlQuery += "      R.IS_ACTIVE = 1 AND "
    sqlQuery += "      P.ATTENDING_DOCTOR_PERSON_IDENTIFIER = %s "
    sqlQuery += "ORDER BY LAST_NAME"
    myCursor.execute(sqlQuery, (userID,))
    record = myCursor.fetchall()
    if not record:
        return None
    for row in record:
        grabData.append((row[0], row[1], row[2]))
    myCursor.close()
    myDB.close()
    return grabData

## This function performs a select query to get all the patients in the database
## If there are no patients then it will return nothing to the client side of the 
## app. If there are patients then it will append all the patients to an array and 
## return the array to the client side of the app. The client side will display 
## the array in HTML format with JavaScript.
def searchForAllPatients():
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    grabData = []
    sqlQuery = " SELECT USER_ID, LAST_NAME, FIRST_NAME "
    sqlQuery += "FROM ROLES " 
    sqlQuery += "WHERE ROLE = 'Patient' AND "
    sqlQuery += "IS_ACTIVE = 1 "
    sqlQuery += "ORDER BY LAST_NAME"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    if not record:
        return None
    for row in record:
        grabData.append((row[0], row[1], row[2]))
    myCursor.close()
    myDB.close()
    return grabData

## This function performs a select query to check if the room id exists.
## If the room ID does not exist then it will insert a new row to create 
## a new chat room. Otherwise it will proceed. 
def checkChatRoom(chatID, userID, userRole, callerID, callerRole):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    userRoleAllCaps = userRole.upper() + "_ID"
    callerRoleAllCaps = callerRole.upper() + "_ID"
    sqlQuery = "SELECT * FROM CHAT_ROOMS WHERE CHAT_ROOM_ID = %s"
    myCursor.execute(sqlQuery, (chatID,))
    record = myCursor.fetchone()
    if not record:
        sqlInsert = " INSERT INTO CHAT_ROOMS "
        sqlInsert += "(CHAT_ROOM_ID, " + userRoleAllCaps + ", " + callerRoleAllCaps + ") "
        sqlInsert += "VALUES (%s, %s, %s)"
        myCursor.execute(sqlInsert, (chatID, userID, callerID,))
        myDB.commit()
    myCursor.close()
    myDB.close()

## This function gets the chat messages associated with the user and the caller.
## If there are no messages then it will return nothing to the client side of the
## app. If there are messages then it will append the messges to an array and return
## the array to the client side of the app. The client side will display the array
## in HTML format with JavaScript    
def getChatMessages(chatID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    grabData = []
    sqlQuery = "SELECT * FROM CHAT_HISTORY WHERE CHAT_ROOM_ID = %s"
    myCursor.execute(sqlQuery, (chatID,))
    record = myCursor.fetchall()
    if not record:
        return None
    for row in record:
        grabData.append((row[2], row[3], row[4].strftime("%m/%d/%Y %H:%M")))
    myCursor.close()
    myDB.close()
    return grabData

## This function inserts a chat message into the chat history database table. 
def insertChatMessage(chatID, userID, msg, currentTime):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsertQuery = " INSERT INTO CHAT_HISTORY "
    sqlInsertQuery += "(CHAT_ROOM_ID, USER_ID, MESSAGE, TIME_SENT) "
    sqlInsertQuery += "VALUES (%s, %s, %s, %s)"
    myCursor.execute(sqlInsertQuery, (chatID, userID, msg, currentTime,))
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function gets the data from the PATIENTIDENTIFICATION and DIAGNOSIS 
## database tables depending on the user input from the app. If the user input 
## matches in the database tables then it returns the data from the DB. If no 
## data exists then it returns nothing."
def getPatientData():
    array = []
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = "SELECT PATIENTFAMILYNAME, PATIENTGIVENNAME, "
    sqlQuery += "      PATIENTID, SEX, "
    sqlQuery += "      DATEOFBIRTH, IS_ACTIVE "
    sqlQuery += "FROM PATIENTIDENTIFICATION, ROLES "
    sqlQuery += "WHERE ROLE = 'Patient' AND PATIENTID = USER_ID "
    sqlQuery += "ORDER BY PATIENTFAMILYNAME"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    # If no records were found then return nothing.     
    if not record:
        return None
    # If records were found then append to array.       
    for row in record:  
        array.append((row[0], row[1], row[2], row[3], row[4], row[5]))
    # Disconnect database    
    myCursor.close()
    myDB.close()
    return array

## This function gets the data from the PATIENTIDENTIFICATION and DIAGNOSIS 
## database tables depending on the doctors input. If the user input 
## matches in the database tables then it returns the data from the DB. If no 
## data exists then it returns nothing."
def getPatientData2(DocID):
    array = []
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = " SELECT PATIENTFAMILYNAME, PATIENTGIVENNAME, "
    sqlQuery += "       PATIENTID, SEX, DATEOFBIRTH "
    sqlQuery += "FROM PATIENTIDENTIFICATION pI, PATIENTVISITS pV "
    sqlQuery += "WHERE pI.PATIENTID = pV.PATIENT_ID AND "
    sqlQuery += "      ATTENDING_DOCTOR_PERSON_IDENTIFIER = " + DocID 
    sqlQuery += " ORDER BY PATIENTFAMILYNAME"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    # If no records were found then return nothing.
    if not record:
        return None
    # If records were found then append to array.
    for row in record:
        array.append((row[0], row[1], row[2], row[3], row[4]))
    # Disconnect database
    myCursor.close()
    myDB.close()
    return array

# This function grabs the doctors information from the database
def getDoctorData():
    array = []
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = " SELECT FIRST_NAME, LAST_NAME, USER_ID "
    sqlQuery += "FROM ROLES " 
    sqlQuery += "WHERE ROLE = 'DOCTOR' "
    sqlQuery += "ORDER BY FIRST_NAME"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    # If no records were found then return nothing.     
    if not record:
        return None
    # If records were found then append to array.       
    for row in record:  
        array.append((row[0], row[1], row[2]))
    # Disconnect database    
    myCursor.close()
    myDB.close()
    return array

# This function grabs the patients information from the database
def getPatientDetails(patientID):
    array = []
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlQuery =  "SELECT PI.PATIENTID, PI.PATIENTFAMILYNAME, "
    sqlQuery += "       PI.PATIENTGIVENNAME, PI.DATEOFBIRTH, PI.SEX, "
    sqlQuery += "       PI.RACE, PI.PHONENUMBERHOME, PI.PRIMARYLANGUAGE "
    sqlQuery += "FROM PATIENTIDENTIFICATION PI "
    sqlQuery += "WHERE PI.PATIENTID = %s"
    myCursor.execute(sqlQuery, (str(patientID),))
    record = myCursor.fetchone()
    sqlQuery2 = "SELECT PHONENO FROM NEXTOFKIN WHERE PATIENTID = %s"
    myCursor.execute(sqlQuery2, (patientID,))
    record2 = myCursor.fetchone()
    if not record2:
        record2 = ["No Next of Kin"]
    sqlQuery3 = "SELECT ATTENDING_DOCTOR_GIVEN_NAME, "
    sqlQuery3 += "      ATTENDING_DOCTOR_FAMILY_NAME "
    sqlQuery3 += "FROM PATIENTVISITS WHERE PATIENT_ID = %s"
    myCursor.execute(sqlQuery3, (patientID,))
    record3 = myCursor.fetchone()
    sqlQuery4 = "SELECT DESCRIPTION FROM DIAGNOSIS WHERE PATIENT_ID = %s"
    myCursor.execute(sqlQuery4, (patientID,))
    record4 = myCursor.fetchone()
    sqlQuery5 = " SELECT PD.PROCEDURE_DESCRIPTION "
    sqlQuery5 += "FROM PROCEDURES PD, PATIENTVISITS PV "
    sqlQuery5 += "WHERE PV.PATIENTVISITID = PD.PATIENT_VISIT_ID AND "
    sqlQuery5 += "      PV.PATIENT_ID = %s"
    myCursor.execute(sqlQuery5, (patientID,))
    record5 = myCursor.fetchone()
    array = [(record[0], record[1], record[2], record[3], record[4], record[5], record[6], 
            record[7], record2[0], record3[0], record3[1], record4[0], record5[0])]
    myCursor.close()
    myDB.close()
    return array

# This function gets the order message, corresponding with the patient, from the database
def getOrderMessage(patientID):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered = True)
    sqlQuery = "  SELECT REQUESTED_GIVE_AMOUNT_MINIMUM, "
    sqlQuery += "        REQUESTED_GIVE_AMOUNT_MAXIMUM, "
    sqlQuery += "        REQUESTED_GIVE_UNITS, "
    sqlQuery += "        REQUESTED_DOSAGE_FORM, "
    sqlQuery += "        PROVIDERS_PHARMACY_INSTRUCTIONS, "
    sqlQuery += "        PROVIDERS_ADMINISTRATION_INSTRUCTIONS, "
    sqlQuery += "        ALLOW_SUBSTITUTIONS "
    sqlQuery += " FROM PHARMACY_PRESCRIPTION_ORDER_SEGMENT "
    sqlQuery += " WHERE PATIENT_ID = %s"
    myCursor.execute(sqlQuery, (patientID,))
    record = myCursor.fetchone()
    if not record:
        return None
    array =[(record[0], record[1], record[2], record[3], record[4], record[5], record[6])]
    myCursor.close()
    myDB.close()
    return array

## This function inserts a new row to the Patient Idenitification table
def insertPatientId(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = " INSERT INTO PATIENTIDENTIFICATION "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    patientIDValues = (data['PatientIdentification']['patientIdentifierList']['idNumber'],
                    data['PatientIdentification']['alternatePatientId-Pid'],
                    data['PatientIdentification']['patientName']['familyName'],
                    data['PatientIdentification']['patientName']['givenName'],
                    data['PatientIdentification']['mother\'sMaidenName'],
                    data['PatientIdentification']['date/TimeOfBirth'],
                    data['PatientIdentification']['administrativeSex'],
                    data['PatientIdentification']['patientAlias'],
                    data['PatientIdentification']['race'],
                    data['PatientIdentification']['countyCode'],
                    data['PatientIdentification']['phoneNumber-Home'],
                    data['PatientIdentification']['phoneNumber-Business'],
                    data['PatientIdentification']['primaryLanguage'],
                    data['PatientIdentification']['maritalStatus'],
                    data['PatientIdentification']['religion'],
                    data['PatientIdentification']['patientAccountNumber']['idNumber'],
                    data['PatientIdentification']['ssnNumber-Patient'],
                    data['PatientIdentification']['driver\'sLicenseNumber-Patient'],
                    data['PatientIdentification']['mother\'sIdentifier'],
                    data['PatientIdentification']['ethnicGroup'],
                    data['PatientIdentification']['birthPlace'],
                    data['PatientIdentification']['multipleBirthIndicator'],
                    data['PatientIdentification']['birthOrder'],
                    data['PatientIdentification']['citizenship'],
                    data['PatientIdentification']['veteransMilitaryStatus'],
                    data['PatientIdentification']['nationality'],
                    data['PatientIdentification']['patientDeathDateAndTime'],
                    data['PatientIdentification']['patientDeathIndicator'],)
    myCursor.execute(sqlInsert, patientIDValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the address table
def insertAddresses(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = "INSERT INTO ADDRESSES (PATIENTID, "
    sqlInsert += "                      STREETADDRESS, "
    sqlInsert += "                      CITY, "
    sqlInsert += "                      STATEORPROVINCE, "
    sqlInsert += "                      ZIPORPOSTALCODE) "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s)"
    addressValues = (data['PatientIdentification']['patientIdentifierList']['idNumber'],
                    data['PatientIdentification']['patientAddress']['streetAddress'],
                    data['PatientIdentification']['patientAddress']['city'],
                    data['PatientIdentification']['patientAddress']['stateOrProvince'],
                    data['PatientIdentification']['patientAddress']['zipOrPostalCode'],)
    myCursor.execute(sqlInsert, addressValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the next of kin table
def insertNextOfKin(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = "INSERT INTO NEXTOFKIN (PATIENTID, " 
    sqlInsert += "                      FAMILYNAME, " 
    sqlInsert += "                      GIVENNAME, "
    sqlInsert += "                      RELATIONSHIP, "
    sqlInsert += "                      STREETADDRESS, "
    sqlInsert += "                      CITY, "
    sqlInsert += "                      STATEORPROVINCE, "
    sqlInsert += "                      ZIPORPOSTALCODE, "
    sqlInsert += "                      PHONENO, " 
    sqlInsert += "                      BUSINESSPHONE, "
    sqlInsert += "                      CONTACTROLES, "
    sqlInsert += "                      STARTDATE, "
    sqlInsert += "                      ENDDATE, "
    sqlInsert += "                      ASSOCIATEDPARTIESJOBTITLE, "
    sqlInsert += "                      ASSOCIATEDPARTIESJOBCLASS, "
    sqlInsert += "                      ASSOCIATEDPARTIESEMPNO, "
    sqlInsert += "                      ORGANIZATIONNAME, "
    sqlInsert += "                      MARITALSTATUS, "
    sqlInsert += "                      ADMINISTRATIVESEX, "
    sqlInsert += "                      DATETIMEOFBIRTH, "
    sqlInsert += "                      LIVINGDEPENDENCY, "
    sqlInsert += "                      AMBULATORYSTATUS, "
    sqlInsert += "                      CITIZENSHIP, "
    sqlInsert += "                      PRIMARYLANGUAGE, " 
    sqlInsert += "                      LIVINGARRANGEMENT) "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    nextOfKinValues = (data['PatientIdentification']['patientIdentifierList']['idNumber'],
                            data['NextOfKin']['name']['familyName'],
                            data['NextOfKin']['name']['givenName'],
                            data['NextOfKin']['relationship'],
                            data['NextOfKin']['address']['streetAddress'],
                            data['NextOfKin']['address']['city'],
                            data['NextOfKin']['address']['stateOrProvince'],
                            data['NextOfKin']['address']['zipOrPostalCode'],
                            data['NextOfKin']['phoneNumber'],
                            data['NextOfKin']['businessPhoneNumber'],
                            data['NextOfKin']['contactRole'],
                            data['NextOfKin']['startDate'],
                            data['NextOfKin']['endDate'],
                            data['NextOfKin']['associatedPartiesJobTitle'],
                            data['NextOfKin']['associatedPartiesJobClass'],
                            data['NextOfKin']['associatedPartiesEmployeeNumber'],
                            data['NextOfKin']['organizationName'],
                            data['NextOfKin']['maritalStatus'],
                            data['NextOfKin']['administrativeSex'],
                            data['NextOfKin']['date/TimeOfBirth'],
                            data['NextOfKin']['livingDependency'],
                            data['NextOfKin']['ambulatoryStatus'],
                            data['NextOfKin']['citizenship'],
                            data['NextOfKin']['primaryLanguage'],
                            data['NextOfKin']['livingArrangement'],)
    myCursor.execute(sqlInsert, nextOfKinValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the Patient Visits table
def insertPatientVisit(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = "INSERT INTO PATIENTVISITS (PATIENT_ID, " 
    sqlInsert += "                          PATIENTCLASS, "
    sqlInsert += "                          ADMISSIONTYPE, "
    sqlInsert += "                          PREADMITNO, "
    sqlInsert += "                          PRIORPATIENTLOCATION, "
    sqlInsert += "                          ATTENDING_DOCTOR_PERSON_IDENTIFIER, "
    sqlInsert += "                          ATTENDING_DOCTOR_FAMILY_NAME, "
    sqlInsert += "                          ATTENDING_DOCTOR_GIVEN_NAME, "
    sqlInsert += "                          HOSPITALSERVICE, "
    sqlInsert += "                          PREADMITTESTINDICATOR, "
    sqlInsert += "                          READMISSIONINDICATOR, "
    sqlInsert += "                          ADMITSOURCE, "
    sqlInsert += "                          AMBULATORYSTATUS, "
    sqlInsert += "                          VIPINDICATOR, "
    sqlInsert += "                          ADMITTINGDOCTORPERSONIDENTIFIER, "
    sqlInsert += "                          ADMITTINGDOCTORFAMILYNAME, "
    sqlInsert += "                          ADMITTINGDOCTORGIVENNAME, "
    sqlInsert += "                          PATIENTTYPE, "
    sqlInsert += "                          VISITNO, "
    sqlInsert += "                          FINANCIALCLASS, "
    sqlInsert += "                          CHARGEPRICEINDICATOR, "
    sqlInsert += "                          COURTESYCODE, "
    sqlInsert += "                          CREDITRATING, "
    sqlInsert += "                          CONTRACTCODE, "
    sqlInsert += "                          CONTRACTEFFECTIVEDATE, "
    sqlInsert += "                          CONTRACTAMOUNT, "
    sqlInsert += "                          CONTRACTPERIOD, "
    sqlInsert += "                          INTERESTCODE, "
    sqlInsert += "                          TRANSFERTOBADDEBTCODE, "
    sqlInsert += "                          TRANSFERTOBADDEBTDATE, "
    sqlInsert += "                          BADDEBTAGENCYCODE, "
    sqlInsert += "                          BADDEBTTRANSFERAMOUNT, "
    sqlInsert += "                          BADDEBTRECOVERYAMOUNT, "
    sqlInsert += "                          DELETEACCOUNTINDICATOR, "
    sqlInsert += "                          DELETEACCOUNTDATE, "
    sqlInsert += "                          DISCHARGEDISPOSITION, "
    sqlInsert += "                          DISCHARGEDTOLOCATION, "
    sqlInsert += "                          DIETTYPE, "
    sqlInsert += "                          SERVICINGFACILITY, "
    sqlInsert += "                          BEDSTATUS, " 
    sqlInsert += "                          ACCOUNTSTATUS, "
    sqlInsert += "                          PENDINGLOCATION, "
    sqlInsert += "                          PRIORTEMPORARYLOCATION, "
    sqlInsert += "                          ADMITDATETIME) "
    sqlInsert += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    patientVisitsValues = (data['PatientIdentification']['patientIdentifierList']['idNumber'],
                                data['PatientVisit']['patientClass'],
                                data['PatientVisit']['admissionType'],
                                data['PatientVisit']['preAdmitNumber'],
                                data['PatientVisit']['assignedPatientLocation']['facility'],
                                data['PatientVisit']['attendingDoctor']['personIdentifier'],
                                data['PatientVisit']['attendingDoctor']['familyName'],
                                data['PatientVisit']['attendingDoctor']['givenName'],
                                #data['PatientVisit']['referringDoctor']['personIdentifier'],
                                #data['PatientVisit']['consultingDoctor']['personIdentifier'],
                                data['PatientVisit']['hospitalService'],
                                #data['PatientVisit']['temporaryLocation'],
                                data['PatientVisit']['preAdmitTestIndicator'],
                                data['PatientVisit']['re-admissionIndicator'],
                                data['PatientVisit']['admitSource'],
                                data['PatientVisit']['ambulatoryStatus'],
                                data['PatientVisit']['vipIndicator'],
                                data['PatientVisit']['admittingDoctor']['personIdentifier'],
                                data['PatientVisit']['admittingDoctor']['familyName'],
                                data['PatientVisit']['admittingDoctor']['givenName'],
                                data['PatientVisit']['patientType'],
                                data['PatientVisit']['visitNumber']['idNumber'],
                                data['PatientVisit']['financialClass'],
                                data['PatientVisit']['chargePriceIndicator'],
                                data['PatientVisit']['courtesyCode'],
                                data['PatientVisit']['creditRating'],
                                data['PatientVisit']['contractCode'],
                                data['PatientVisit']['contractEffectiveDate'],
                                data['PatientVisit']['contractAmount'],
                                data['PatientVisit']['contractPeriod'],
                                data['PatientVisit']['interestCode'],
                                data['PatientVisit']['transferToBadDebtCode'],
                                data['PatientVisit']['transferToBadDebtDate'],
                                data['PatientVisit']['badDebtAgencyCode'],
                                data['PatientVisit']['badDebtTransferAmount'],
                                data['PatientVisit']['badDebtRecoveryAmount'],
                                data['PatientVisit']['deleteAccountIndicator'],
                                data['PatientVisit']['deleteAccountDate'],
                                data['PatientVisit']['dischargeDisposition'],
                                data['PatientVisit']['dischargedToLocation'],
                                data['PatientVisit']['dietType'],
                                data['PatientVisit']['servicingFacility'],
                                data['PatientVisit']['bedStatus'],
                                data['PatientVisit']['accountStatus'],
                                data['PatientVisit']['pendingLocation'],
                                data['PatientVisit']['priorTemporaryLocation'],
                                data['PatientVisit']['admitDate/Time'],)
    myCursor.execute(sqlInsert, patientVisitsValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the Event Type table
def insertEventType(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = "INSERT INTO EVENTTYPE VALUES (%s, %s, %s, %s, %s)"
    eventTypeValues = (data['eventType']['eventTypeCode'],
                        data['eventType']['recordedDate/Time'],
                        data['eventType']['date/TimePlannedEvent'],
                        data['eventType']['eventReasonCode'],
                        data['eventType']['eventOccurred'],)
    myCursor.execute(sqlInsert, eventTypeValues)
    myDB.commit()
    myCursor.close()
    myDB.close() 

## This function inserts a new row to the Diagnosis table
def insertDiagnosis(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = "INSERT INTO DIAGNOSIS (CODINGMETHOD, " 
    sqlInsert += "                      CODE, "
    sqlInsert += "                      DESCRIPTION, "
    sqlInsert += "                      DATEANDTIME, "
    sqlInsert += "                      TYPE, "
    sqlInsert += "                      MAJORDIAGNOSTICCATEGORY) "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s, %s)"
    diagnosisValues = (data['Diagnosis']['diagnosisCodingMethod'],
                        data['Diagnosis']['diagnosisCode']['identifier'],
                        data['Diagnosis']['diagnosisDescription'],
                        data['Diagnosis']['diagnosisDate/Time'],
                        data['Diagnosis']['diagnosisType'],
                        data['Diagnosis']['majorDiagnosticCategory'],)
    myCursor.execute(sqlInsert, diagnosisValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the Observations table
def insertObservation(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlInsert = " INSERT INTO OBSERVATIONS (OBSVALUETYPE, " 
    sqlInsert += "                         OBSID, " 
    sqlInsert += "                         SUBID, "
    sqlInsert += "                         OBSVALUE, "
    sqlInsert += "                         UNITID, "
    sqlInsert += "                         UNITTEXT, "
    sqlInsert += "                         UNITNAMEOFCODINGSYSTEM, "
    sqlInsert += "                         OBSRANGE, " 
    sqlInsert += "                         INTERPRETATIONCODE, "
    sqlInsert += "                         PROBABILITY, "
    sqlInsert += "                         NATUREOFABNORMALTEST, "
    sqlInsert += "                         RESULTSTATUS) "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    observationValues = (data['Observation/result']['valueType'],
                        data['Observation/result']['observationIdentifier']['text'],
                        data['Observation/result']['observationSub-id'],
                        data['Observation/result']['observationValue'],
                        data['Observation/result']['units']['identifier'],
                        data['Observation/result']['units']['text'],
                        data['Observation/result']['units']['nameOfCodingSystem'],
                        data['Observation/result']['referencesRange'],
                        data['Observation/result']['interpretationCodes'],
                        data['Observation/result']['probability'],
                        data['Observation/result']['natureOfAbnormalTest'],
                        data['Observation/result']['observationResultStatus'],)
    myCursor.execute(sqlInsert, observationValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the addresses table
def insertAddress(data, myDB, myCursor):
    sqlInsertAddress = "  INSERT INTO ADDRESSES "
    sqlInsertAddress += " (STREETADDRESS, CITY, STATEORPROVINCE, ZIPORPOSTALCODE) "
    sqlInsertAddress += " VALUES (%s, %s, %s, %s) "
    addressValues = (data['schedulingActivityInformation']['placerContactAddress']['streetAddress'], 
                    data['schedulingActivityInformation']['placerContactAddress']['city'],
                    data['schedulingActivityInformation']['placerContactAddress']['stateOrProvince'],
                    data['schedulingActivityInformation']['placerContactAddress']['zipOrPostalCode'],)
    myCursor.execute(sqlInsertAddress, addressValues)
    myDB.commit()

    sqlQuery = "  SELECT ADDRESSID FROM ADDRESSES " 
    sqlQuery += " WHERE STREETADDRESS = %s AND "
    sqlQuery += " CITY = %s AND "
    sqlQuery += " STATEORPROVINCE = %s AND "
    sqlQuery += " ZIPORPOSTALCODE = %s "
    myCursor.execute(sqlQuery, addressValues)
    record = myCursor.fetchone()
    return record[0]

## This function inserts a new row to the SCHEDULING_ACTIVITY_INFORMATION table
def insertSchedulingActivity(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    addressID = insertAddress(data, myDB, myCursor)
    sqlInsert = "INSERT INTO SCHEDULING_ACTIVITY_INFORMATION (PATIENT_ID, "
    sqlInsert += "                                            PLACER_APPOINTMENT_ID, "
    sqlInsert += "                                            FILLER_APPOINTMENT_ID, "
    sqlInsert += "                                            OCCURENCE_NUMBER, "
    sqlInsert += "                                            PLACER_GROUP_NUMBER, "
    sqlInsert += "                                            SCHEDULE_ID, "
    sqlInsert += "                                            EVENT_REASON, "
    sqlInsert += "                                            APPOINTMENT_REASON, "
    sqlInsert += "                                            APPOINTMENT_TYPE, "
    sqlInsert += "                                            APPOINTMENT_DURATION, "
    sqlInsert += "                                            APPOINTMENT_DURATION_UNITS, "
    sqlInsert += "                                            APPOINTMENT_TIMING_QUANTITY, "
    sqlInsert += "                                            PLACER_CONTACT_PERSON, "
    sqlInsert += "                                            PLACER_CONTACT_PHONE, "
    sqlInsert += "                                            PLACER_CONTACT_ADDRESS, " # Is address ID in address table?
    sqlInsert += "                                            PLACER_CONTACT_LOCATION, "
    sqlInsert += "                                            FILLER_CONTACT_PERSON, "
    sqlInsert += "                                            FILLER_CONTACT_PHONE, "
    sqlInsert += "                                            ENTERED_BY_PERSON, "
    sqlInsert += "                                            ENTERED_BY_PHONE, "
    sqlInsert += "                                            ENTERED_BY_LOCATION, "
    sqlInsert += "                                            PARENT_PLACER_APPOINTMENT_ID, "
    sqlInsert += "                                            PARENT_FILLER_APPOINTMENT_ID, "
    sqlInsert += "                                            FILLER_STATUS_CODE, "
    sqlInsert += "                                            PLACER_ORDER_NUMBER) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    schedulingActivityValues = (data["PatientIdentification"]["patientId"], 
                                data["schedulingActivityInformation"]["placerAppointmentId"], 
                                data["schedulingActivityInformation"]["fillerAppointmentId"],
                                data["schedulingActivityInformation"]["occurrenceNumber"],
                                data["schedulingActivityInformation"]["placerGroupNumber"],
                                data["schedulingActivityInformation"]["scheduleID"],
                                data["schedulingActivityInformation"]["eventReason"],
                                data["schedulingActivityInformation"]["appointmentReason"],
                                data["schedulingActivityInformation"]["appointmentType"],
                                data["schedulingActivityInformation"]["appointmentDuration"],
                                data["schedulingActivityInformation"]["appointmentDurationUnits"],
                                data["schedulingActivityInformation"]["appointmentTimingQuantity"]["start Date/Time"],
                                data["schedulingActivityInformation"]["placerContactPerson"]["personIdentifier"],
                                data["schedulingActivityInformation"]["placerContactPhoneNumber"],
                                addressID,
                                data["schedulingActivityInformation"]["placerContactLocation"]["facility"],
                                data["schedulingActivityInformation"]["fillerContactPerson"]["personIdentifier"],
                                data["schedulingActivityInformation"]["fillerContactPhoneNumber"],
                                data["schedulingActivityInformation"]["enteredByPerson"]["personIdentifier"],
                                data["schedulingActivityInformation"]["enteredbyPhoneNumber"],
                                data["schedulingActivityInformation"]["enteredByLocation"]["facility"],
                                data["schedulingActivityInformation"]["parentPlacerAppointmentId"],
                                data["schedulingActivityInformation"]["parentFillerAppointmentId"],
                                data["schedulingActivityInformation"]["fillerStatusCode"],
                                data["schedulingActivityInformation"]["placerOrderNumber"],)
    myCursor.execute(sqlInsert, schedulingActivityValues)
    myDB.commit()
    myCursor.close()
    myDB.close()

## This function inserts a new row to the SCHEDULING_ACTIVITY_INFORMATION table    
def insertResourceGroup(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlQuery = "  SELECT ID FROM SCHEDULING_ACTIVITY_INFORMATION " 
    sqlQuery += " WHERE PATIENT_ID = %s AND "
    sqlQuery += " APPOINTMENT_TIMING_QUANTITY = %s"
    schedulingValues = (data["PatientIdentification"]["patientId"], 
                        data["schedulingActivityInformation"]["appointmentTimingQuantity"]["start Date/Time"],)
    myCursor.execute(sqlQuery, schedulingValues)
    record = myCursor.fetchone()
    schedulingID = record[0]

    sqlInsert = " INSERT INTO RESOURCE_GROUP (SCHEDULE_ID, SEGMENT_ACTION_CODE, RESOURCE_GROUP_ID) "
    sqlInsert += " VALUES (%s, %s, %s) "
    resourceGroupValues = (schedulingID, data["Resource Group"]['Segment Action Code'], data['Resource Group']['Resource Group ID'],)
    myCursor.execute(sqlInsert, resourceGroupValues)
    myDB.commit()

## This function inserts a new row to the APPOINTMENTS_INFORMATION table
def insertAppointmentInfo(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlInsert = " INSERT INTO APPOINTMENTS_INFORMATION (RESOURCE_GROUP_ID, "
    sqlInsert += "                                      SEGMENT_ACTION_CODE, " 
    sqlInsert += "                                      UNIVERSAL_SERVICE_IDENTIFIER, "
    sqlInsert += "                                      START_DATE_TIME, " 
    sqlInsert += "                                      START_DATE_TIME_OFFSET, " 
    sqlInsert += "                                      START_DATE_TIME_OFFSET_UNITS, "
    sqlInsert += "                                      DURATION, " 
    sqlInsert += "                                      DURATION_UNITS, " 
    sqlInsert += "                                      ALLOW_SUBSTITUTION_CODE, " 
    sqlInsert += "                                      FILLER_STATUS_CODE, " 
    sqlInsert += "                                      SOURCE_OF_COMMENT, " 
    sqlInsert += "                                      COMMENT) "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    appointmentInformationValues = (data["Resource Group"]["Resource Group ID"],
                                    data["Appoinment Information - Service"]["Segment Action Code"],
                                    data["Appoinment Information - Service"]["Universal Service Identifier"],
                                    data["Appoinment Information - Service"]["Start Date/Time"],
                                    data["Appoinment Information - Service"]["Start Date/Time Offset"],
                                    data["Appoinment Information - Service"]["Start Date/Time Offset Units"],
                                    data["Appoinment Information - Service"]["Duration"],
                                    data["Appoinment Information - Service"]["Duration Units"],
                                    data["Appoinment Information - Service"]["Allow Substitution Code"],
                                    data["Appoinment Information - Service"]["Filler Status Code"],
                                    data["notesAndComments[2]"]["sourceOfComment"],
                                    data["notesAndComments[2]"]["comment"],)
    myCursor.execute(sqlInsert, appointmentInformationValues)
    myDB.commit()

## This function inserts a new row to the APPOINTMENTS_INFORMATION_GENERAL_RESOURCES table
def insertAppointmentInfoGeneral(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlInsert = " INSERT INTO APPOINTMENTS_INFORMATION_GENERAL_RESOURCES (RESOURCE_GROUP_ID, "
    sqlInsert += "                                                        RESOURCE_ID, "
    sqlInsert += "                                                        RESOURCE_TYPE, "
    sqlInsert += "                                                        RESOURCE_GROUP, "
    sqlInsert += "                                                        RESOURCE_QUANTITY, "
    sqlInsert += "                                                        RESOURCE_QUANTITY_UNITS, "
    sqlInsert += "                                                        START_DATE_TIME, " 
    sqlInsert += "                                                        START_DATE_TIME_OFFSET, " 
    sqlInsert += "                                                        START_DATE_TIME_OFFSET_UNITS, "
    sqlInsert += "                                                        DURATION, " 
    sqlInsert += "                                                        DURATION_UNITS, " 
    sqlInsert += "                                                        ALLOW_SUBSTITUTION_CODE, " 
    sqlInsert += "                                                        FILLER_STATUS_CODE, " 
    sqlInsert += "                                                        SOURCE_OF_COMMENT, " 
    sqlInsert += "                                                        COMMENT) "
    sqlInsert += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    appointmentGeneralInfoData = (data["Resource Group"]["Resource Group ID"],
                                data["Appoinment Information - General Resource"]["Resource ID"]["identifier"],
                                data["Appoinment Information - General Resource"]["Resource Type"],
                                data["Appoinment Information - General Resource"]["Resource Group"],
                                data["Appoinment Information - General Resource"]["Resource Quantity"],
                                data["Appoinment Information - General Resource"]["Resource Quantity Units"],
                                data["Appoinment Information - General Resource"]["Start Date/Time"],
                                data["Appoinment Information - General Resource"]["Start Date/Time Offset"],
                                data["Appoinment Information - General Resource"]["Start Date/Time Offset Units"],
                                data["Appoinment Information - General Resource"]["Duration"],
                                data["Appoinment Information - General Resource"]["Duration Units"],
                                data["Appoinment Information - General Resource"]["Allow Substitution Code"],
                                data["Appoinment Information - General Resource"]["Filler Status Code"],
                                data["notesAndComments[3]"]["sourceOfComment"],
                                data["notesAndComments[3]"]["comment"],)
    myCursor.execute(sqlInsert, appointmentGeneralInfoData)
    myDB.commit()

## This function inserts a new row to the APPOINTMENTS_INFORMATION_LOCATION_RESOURCES table
def insertAppointmentInfoLocation(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlInsert = " INSERT INTO APPOINTMENTS_INFORMATION_LOCATION_RESOURCES (RESOURCE_GROUP_ID, "
    sqlInsert += "                                                         SEGMENT_ACTION_CODE, " 
    sqlInsert += "                                                         LOCATION_RESOURCE_ID, "
    sqlInsert += "                                                         LOCATION_TYPE_AIL, "
    sqlInsert += "                                                         LOCATION_GROUP, "
    sqlInsert += "                                                         START_DATE_TIME, " 
    sqlInsert += "                                                         START_DATE_TIME_OFFSET, " 
    sqlInsert += "                                                         START_DATE_TIME_OFFSET_UNITS, "
    sqlInsert += "                                                         DURATION, " 
    sqlInsert += "                                                         DURATION_UNITS, " 
    sqlInsert += "                                                         ALLOW_SUBSTITUTION_CODE, " 
    sqlInsert += "                                                         FILLER_STATUS_CODE, " 
    sqlInsert += "                                                         SOURCE_OF_COMMENT, " 
    sqlInsert += "                                                         COMMENT) "
    sqlInsert += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    appointmentInfoLocationvalues = (data["Resource Group"]["Resource Group ID"],
                                    data["Appoinment Information - Location"]["Segment Action Code"],
                                    data["Appoinment Information - Location"]["Location Resource ID"],
                                    data["Appoinment Information - Location"]["Location Type"],
                                    data["Appoinment Information - Location"]["Location Group"],
                                    data["Appoinment Information - Location"]["Start Date/Time"],
                                    data["Appoinment Information - Location"]["Start Date/Time Offset"],
                                    data["Appoinment Information - Location"]["Start Date/Time Offset Units"],
                                    data["Appoinment Information - Location"]["Duration"],
                                    data["Appoinment Information - Location"]["Duration Units"],
                                    data["Appoinment Information - Location"]["Allow Substitution Code"],
                                    data["Appoinment Information - Location"]["Filler Status Code"],
                                    data["notesAndComments[4]"]["sourceOfComment"],
                                    data["notesAndComments[4]"]["comment"],)
    myCursor.execute(sqlInsert, appointmentInfoLocationvalues)
    myDB.commit()

## This function inserts a new row to the APPOINTMENTS_INFORMATION_PERSONNEL_RESOURCES table
def insertAppointmentInfoPersonnel(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlInsert = " INSERT INTO APPOINTMENTS_INFORMATION_PERSONNEL_RESOURCES (RESOURCE_GROUP_ID, "
    sqlInsert += "                                                          SEGMENT_ACTION_CODE, "
    sqlInsert += "                                                          PERSONNEL_RESOURCE_ID, "
    sqlInsert += "                                                          RESOURCE_TYPE, "
    sqlInsert += "                                                          RESOURCE_GROUP, "
    sqlInsert += "                                                          START_DATE_TIME, " 
    sqlInsert += "                                                          START_DATE_TIME_OFFSET, " 
    sqlInsert += "                                                          START_DATE_TIME_OFFSET_UNITS, "
    sqlInsert += "                                                          DURATION, " 
    sqlInsert += "                                                          DURATION_UNITS, " 
    sqlInsert += "                                                          ALLOW_SUBSTITUTION_CODE, " 
    sqlInsert += "                                                          FILLER_STATUS_CODE, " 
    sqlInsert += "                                                          SOURCE_OF_COMMENT, " 
    sqlInsert += "                                                          COMMENT) "
    sqlInsert += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    appointmentInfoPersonaValues = (data["Resource Group"]["Resource Group ID"],
                                    data["Appoinment Information - Personnel Resource"]["Segment Action Code"],
                                    data["Appoinment Information - Personnel Resource"]["Personal Resource ID"]["Facility"],
                                    data["Appoinment Information - Personnel Resource"]["Resource Role"],
                                    data["Appoinment Information - Personnel Resource"]["Resource Group"],
                                    data["Appoinment Information - Personnel Resource"]["Start Date/Time"],
                                    data["Appoinment Information - Personnel Resource"]["Start Date/Time Offset"],
                                    data["Appoinment Information - Personnel Resource"]["Start Date/Time Offset Units"],
                                    data["Appoinment Information - Personnel Resource"]["Duration"],
                                    data["Appoinment Information - Personnel Resource"]["Duration Units"],
                                    data["Appoinment Information - Personnel Resource"]["Allow Substitution Code"],
                                    data["Appoinment Information - Personnel Resource"]["Filler Status Code"],
                                    data["notesAndComments[5]"]["sourceOfComment"],
                                    data["notesAndComments[5]"]["comment"],)
    myCursor.execute(sqlInsert, appointmentInfoPersonaValues)
    myDB.commit()

## This function inserts a new row to the COMMON_ORDER table
def insertCommonOrder(data):
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    sqlInsert =  " INSERT INTO COMMON_ORDER (PATIENT_ID, "
    sqlInsert += "                           ORDER_CONTROL, " 
    sqlInsert += "                           PLACER_ORDER_NUMBER, " 
    sqlInsert += "                           FILLER_ORDER_NUMBER, " 
    sqlInsert += "                           PLACER_GROUP_NUMBER, " 
    sqlInsert += "                           ORDER_STATUS, "
    sqlInsert += "                           RESPONSE_FLAG, " 
    sqlInsert += "                           QUANTITY_TIMING, " 
    sqlInsert += "                           PARENT_ORDER, "
    sqlInsert += "                           DATE_TIME_OF_TRANSACTION, " 
    sqlInsert += "                           ENTERED_BY, "  
    sqlInsert += "                           VERIFIED_BY, " 
    sqlInsert += "                           ORDERING_PROVIDER, " 
    sqlInsert += "                           ENTERERS_LOCATION, " 
    sqlInsert += "                           CALLBACK_PHONE, " 
    sqlInsert += "                           ORDER_EFFECTIVE_DATE_TIME, " 
    sqlInsert += "                           ORDER_CONTROL_CODE_REASON, " 
    sqlInsert += "                           ENTERING_ORGANIZATION, "
    sqlInsert += "                           ENTERING_DEVICE, " 
    sqlInsert += "                           ACTION_BY) " 
    sqlInsert += " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    commonOrderValues = (data["PatientIdentification"]["patientId"], 
                        data["Common order segment"]["Order Control"],
                        data["Common order segment"]["Place Order Number"],
                        data["Common order segment"]["Filler Order Number"],
                        data["Common order segment"]["Placer Group Number"],
                        data["Common order segment"]["Order Status"],
                        data["Common order segment"]["Response Flag"],
                        data["Common order segment"]["Quality/Timing"],
                        data["Common order segment"]["Parent Order"],
                        data["Common order segment"]["Date/Time of Transaction"],
                        data["Common order segment"]["Entered By"],
                        data["Common order segment"]["Verified By"],
                        data["Common order segment"]["Ordering Provider"],
                        data["Common order segment"]["Enterer's Location"],
                        data["Common order segment"]["Call Back Phone Number"],
                        data["Common order segment"]["Order Effective Date/Time"],
                        data["Common order segment"]["Order Control Code Reason"],
                        data["Common order segment"]["Entering Organization"],
                        data["Common order segment"]["Entering Device"],
                        data["Common order segment"]["Action By"],)
    myCursor.execute(sqlInsert, commonOrderValues)
    myDB.commit()

## This function checks if the patient id exists in the patient identification
## table. If it does not then it will call the functions that insert new rows to
## the specified tables. 
def insertMessages(jsonFile):
    data = json.load(jsonFile)
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor(buffered=True)
    if data['messageHeader']['messageType']['universalId'] == "A01" or data['messageHeader']['messageType']['universalId'] == "A03" or data['messageHeader']['messageType']['universalId'] == "A08": 
        sqlQuery = "SELECT PATIENTID FROM PATIENTIDENTIFICATION WHERE PATIENTID = %s"
        myCursor.execute(sqlQuery, (data['PatientIdentification']['patientIdentifierList']['idNumber'],))
        record = myCursor.fetchone()
        myCursor.close()
        myDB.close()
        if not record:
            insertPatientId(data)
            insertAddresses(data)
            insertNextOfKin(data)
            insertPatientVisit(data)
            insertEventType(data)
            insertDiagnosis(data)
            insertObservation(data)
        else:
            if data['eventType']['eventTypeCode'] == "A01":
                insertPatientVisit(data)

            #elif data['eventType']['eventTypeCode'] == "A03":

            #elif data['eventType']['eventTypeCode'] == "A08":
    elif data['messageHeader']['messageType']['universalId'] == "S12" or data['messageHeader']['messageType']['universalId'] == "S13":
        sqlQuery = "SELECT PATIENTID FROM PATIENTIDENTIFICATION WHERE PATIENTID = %s"
        myCursor.execute(sqlQuery, (data['PatientIdentification']['patientIdentifierList']['idNumber'],))
        record = myCursor.fetchone()
        myCursor.close()
        myDB.close()
        if not record:
            insertAddresses(data)
            insertPatientVisit(data)
            insertDiagnosis(data)
            insertSchedulingActivity(data)
            insertResourceGroup(data)
            insertAppointmentInfo(data)
            insertAppointmentInfoGeneral(data)
            insertAppointmentInfoLocation(data)
            insertAppointmentInfoPersonnel(data)
        else:
            if data['messageHeader']['messageType']['universalId'] == "S12":
                insertSchedulingActivity(data)
                insertResourceGroup(data)
                insertAppointmentInfo(data)
                insertAppointmentInfoGeneral(data)
                insertAppointmentInfoLocation(data)
                insertAppointmentInfoPersonnel(data)
                """
            else:
                updateSchedulingActivity(data)
                updateTimeAndQuantity(data)
                updateResourceGroup(data)
                updateAppointmentInfo(data)
                updateAppointmentInfoGeneral(data)
                updateAppointmentInfoLocation(data)
                updateAppointmentInfoPersonal(data)    
                """
    elif data['messageHeader']['messageType']['messageCode'] == "ORM":
        insertCommonOrder(data)
        
    
## This function gets the data from the LOCATIONS 
## database tables. If no 
## data exists then it returns nothing."
def getLocationDetails():
    array = []
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = " SELECT POINTOFCARE, FLOOR, "
    sqlQuery += "       ROOM, BED, STATUS " 
    sqlQuery += "FROM LOCATIONS "
    sqlQuery += "ORDER BY POINTOFCARE, FLOOR, "
    sqlQuery += "         ROOM, BED"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    # If no records were found then return nothing.     
    if not record:
        return None
    # If records were found then append to array.       
    for row in record:  
        array.append((row[0], row[1], row[2], row[3], row[4]))
    # Disconnect database    
    myCursor.close()
    myDB.close()
    return array


## This function gets the STATUS from the LOCATIONS 
## database tables. If no 
## data exists then it returns nothing."
def getLocationOverview():
    array = []
    myDB = dbconfig.connectDB()
    myCursor = myDB.cursor()
    sqlQuery = " SELECT STATUS "
    sqlQuery += "FROM LOCATIONS "
    sqlQuery += "ORDER BY FLOOR, ROOM, BED"
    myCursor.execute(sqlQuery)
    record = myCursor.fetchall()
    # If no records were found then return nothing.
    if not record:
        return None
    # If records were found then append to array.
    for row in record:
        array.append((row[0]))
    # Disconnect database
    myCursor.close()
    myDB.close()
    return array
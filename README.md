# Hospital App
The goal in this project was to develop an open source integration engine that takes legacy HL7 V2 messages and send to a cloud based FHIR server. Health Level Seven (HL7) is a set of international standards for transfer of clinical and administrative data between software applications used by various healthcare providers. The current business is using an outdated messaging standard. The goal of the project was to develop an open source integration engine that will take legacy HL7 V2 messages and send them to a cloud base FHIR server. Python was used to develop an integration engine that receives and converts messages. The project provided an android app to display information from the server. The benefits of this project was that it would make it easier to provide healthcare information to healthcare providers.

# Source Code
The code for the front end is in CordovaApp/opensourceintegration/www the JavaScript code is in js/, HTML is in pages/, and css is in css/. The back end code is in DatabaseBackend/flask. The main files for the back end are app.py, PyAES.py, and dbQuerys.py. Any other files that have "test" in the name are for unit testing and regression testing.

# Functional Requirements
1. User should be able to log in (patient, doctor, or admin).<br/> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/login.PNG?raw=true) <br /> <br />
2. Doctors Menu <br/> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/doctorsmenu.PNG?raw=true) <br /> <br />
3. Patients Menu <br/> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/patientsmenu.PNG?raw=true) <br /> <br />
4. Administrators Menu <br/> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/adminmenu.PNG?raw=true) <br /> <br />
5. User should access chat channel. The Administrators can chat with all patients and doctors in the hospital. Patients can only talk with associated doctors and administrators. Doctors can only speak with associated patients and administrators. 
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/chatroomselect.PNG?raw=true) <br /> <br />
6. 

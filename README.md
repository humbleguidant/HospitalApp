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
5. User should access chat channel. The Administrators can chat with all patients and doctors in the hospital. Patients can only chat with associated doctors and administrators. Doctors can only chat with associated patients and administrators. <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/chatroomselect.PNG?raw=true) <br /> <br />
6. User should be able to access chat history with caller. <br /> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/chathistory.PNG?raw=true) <br /> <br />
7. The administrator should be able to search for doctors in the hospital. <br /> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/searchdoctor.PNG?raw=true) <br /> <br />
8. The administrator should be able to search for the patients associated with a specific doctor. <br /> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/searchdoctorspatients.PNG?raw=true) <br /> <br />
9. When clicking on a patient, the user should be able to see the patients information. <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/doctorspatientinfo.PNG?raw=true) <br /> <br />
10. Along with the scheduled appointments. <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/doctorspatientschedule.PNG?raw=true) <br /> <br />
11. As well as the order message <br/> <br/>
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/doctorspatientmessage.PNG?raw=true) <br /> <br />
12. The administrator should be able to view the occuopancy overview of the hospital. (How many beds are free or used) <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/occupancyoverview.PNG?raw=true) <br /> <br />
13. The pie chart should be interactive <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/interactive.PNG?raw=true) <br /> <br />
14. The administrator should be able to select the occupancy details link and be presented with the details of the beds.  <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/occupancydetails.PNG?raw=true) <br /> <br />
15. The doctor should be able to search for all patients, inactive, and active. <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/searchpatients.PNG?raw=true) <br /> <br />
16. Inactive patients <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/inactive.PNG?raw=true) <br /> <br />
17. The doctor should be able to access their scheduled appointments. <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/doctorschedule.PNG?raw=true) <br /> <br />
18. As well as the patient <br /> <br />
![alt text](https://github.com/humbleguidant/HospitalApp/blob/master/Screenshots/patientschedule.PNG?raw=true) <br /> <br />

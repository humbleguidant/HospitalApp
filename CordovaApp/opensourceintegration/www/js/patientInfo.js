/**
##################################################
 This file gets the patients info from the database.
##################################################
 YearMonthDayCreated: 2021-02-01
 Project: Open Source Engine Integration
 Program Name: patientInfo.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.3
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/02/01               Bao mai            1             Creating AJAX call to flask
 2021/03/24               Aubrey Nickerson   2             Add second AJAX call to get patient info.
 2021/03/26               Aubrey Nickerson   3             Add another AJAX call to get patient schedule.
##################################################
MIT License
Copyright 2021 Okanagan College & Harris Healthcare

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
##################################################
 */
let key = "ddfbccae-b4c4-11";
let iv = "ddfbccae-b4c4-11";
$(document).ready(function() {
    $.ajax({
        url: 'http://10.1.144.91:8090/checkSession',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },
        success: function (data) {
            // If user is not logged in then return to the login page.
            if(data === "User is not logged in."){
                window.location = "../index.html";
                return false;
            }
        }
    });
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    let patientID;
    let DocID;
    if(urlParams.get("doctorPatientID") === null && urlParams.get("DocID") === null){
        patientID = urlParams.get("patientID");
        $("#theTextHeader").before("<a href=\"../pages/searchPatient.html\"> " +
                                "        <div id=\"backButton\" class=\"back\">" +
                                "            <i class=\"fas fa-chevron-left\"></i>" +
                                "        </div>" +
                                " </a>");
    } else {
        patientID = urlParams.get("doctorPatientID");
        DocID = urlParams.get("DocID");
        $("#theTextHeader").before("<a href='../pages/searchDoctorPatient.html?DocID=" + DocID + "'>" +
                                "        <div id=\"backButton\" class=\"back\">" +
                                "            <i class=\"fas fa-chevron-left\"></i>" +
                                "        </div>" +
                                " </a>");
    }

    let ul = document.getElementById("patientDetails");
    let dataString = "patientID=" + patientID;
    let li1 = document.createElement('li');
    let li2 = document.createElement('li');
    let li3 = document.createElement('li');
    let emergencyNumber = document.getElementById("emergencyNumber");
    let doctorsName = document.getElementById("doctorsName");
    let conditionDescription = document.getElementById("conditionDescription");
    let procedureDescription = document.getElementById("procedureDescription");
    let noDataDescription = document.getElementById("noData");
    let requestedGiveAmountMin = document.getElementById("requestedGiveAmountMin");
    let requestedGiveAmountMax = document.getElementById("requestedGiveAmountMax");
    let requestedGiveUnits = document.getElementById("requestedGiveUnits");
    let requestedDosageForm = document.getElementById("requestedDosageForm");
    let providersPharmacyInstructions = document.getElementById("providersPharmacyInstructions");
    let providersAdministrationInstructions = document.getElementById("providersAdministrationInstructions");
    let allowSubstitution = document.getElementById("allowSubstitutions");
    // this AJAX function sends a request to the searchPatient() function in app.py
    // to check if the user exists in the database.
    $.ajax({
        url: 'http://10.1.144.91:8090/getPatientInfo/' + patientID,
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        // if the request is successful then the data will be saved as an array
        // in the "data" variable.
        success: function(data) {
            // If the data exists in the database then display the data in a html table.
            if (data !== null) {
                li1.appendChild(document.createTextNode("Name: " + aes_decrypt(data[0][2], key, iv) + " " + aes_decrypt(data[0][1], key, iv)));
                ul.appendChild(li1);
                li2.appendChild(document.createTextNode("Phone: " + aes_decrypt(data[0][6], key, iv)));
                ul.appendChild(li2);
                li3.appendChild(document.createTextNode("Sex: " + aes_decrypt(data[0][4], key, iv)));
                ul.appendChild(li3);
                emergencyNumber.innerHTML = aes_decrypt(data[0][8], key, iv);
                doctorsName.innerHTML = aes_decrypt(data[0][9], key, iv) + " " + aes_decrypt(data[0][10], key, iv);
                conditionDescription.innerHTML = aes_decrypt(data[0][11], key, iv);
                procedureDescription.innerHTML = aes_decrypt(data[0][12], key, iv);
                return false;
            }
        }
    });
    $.ajax({
        url: 'http://10.1.144.91:8090/schedule',
        data: dataString,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        // if the request is successful then the data will be returned to the user
        // in the "data" variable.
        success: function(data){
            // If the user is not logged in then they are redirected to the login page.
            let row = "";
            if (data !== null) {
                for(let i = 0; i < data.length; i++){
                    row += "<tr style=\"height: 60px\">" +
                            "<td class='text-left'>" + aes_decrypt(data[i][4], key, iv) + "</td>" +
                            "<td class='text-left'>" + aes_decrypt(data[i][5], key, iv) + "</td>" +
                            "<td class='text-left'>" + aes_decrypt(data[i][9], key, iv) + "</td>" +
                           "</tr>";
                }
                $("#scheduleTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                $("#scheduleTable tbody").append(row);
                return false;
            }
        },

    });

    $.ajax({
        url: 'http://10.1.144.91:8090/displayOrderMessage',
        data: dataString,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        // if the request is successful then the data will be returned to the user
        // in the "data" variable.
        success: function(data){
            if(data !== "Nothing"){
                requestedGiveAmountMin.innerHTML = "Requested Give Amount Min: " + aes_decrypt(data[0][0], key, iv);
                requestedGiveAmountMax.innerHTML = "Requested Give Amount Max: " + aes_decrypt(data[0][1], key, iv);
                requestedGiveUnits.innerHTML = "Requested Give Units: " + aes_decrypt(data[0][2], key, iv);
                requestedDosageForm.innerHTML = "Requested Dosage Form: " + aes_decrypt(data[0][3], key, iv);
                providersPharmacyInstructions.innerHTML = "Pharmacy Instructions: " + aes_decrypt(data[0][4], key, iv);
                providersAdministrationInstructions.innerHTML = "Administration Instructions: " + aes_decrypt(data[0][5], key, iv);
                allowSubstitution.innerHTML = "Allow Substitutions: " + aes_decrypt(data[0][6], key, iv);
                return false;
            }
            noDataDescription.innerHTML = "No order message found user this patient."
            return false;
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });
});
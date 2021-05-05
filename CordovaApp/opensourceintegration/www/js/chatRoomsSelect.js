/**
##################################################
 This file handles displaying all the chat rooms available
 for the user. If the user is a doctor then the page will
 display the patients associated with the doctor as well as
 the administrators. If the user is a patient then the page
 will display all the doctors associated with the patient. If
 the user is an administrator then the page will display all
 patients and doctors.
##################################################
 YearMonthDayCreated: 2021-02-18
 Project: Open Source Engine Integration
 Program Name: chatRoomsSelect.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.3
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/02/18               Aubrey Nickerson   1             Created three AJAX functions called getAdmin(), getDoctors(),
                                                           and getPatients(). Created another AJAX function that gets the
                                                           roll of the user. If the user is a doctor then call getAdmin() and
                                                           getPatients(). If the user is a patient then call getDoctors() and
                                                           getPatients(). If the user is an administrator then call getDoctors()
                                                           and getPaients().
 2021/03/04               Aubrey Nickerson   2             Added encryption functionality.
 2021/03/05               Aubrey Nickerson   3             Added Search filter functionality.
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
$('#loadingDiv').hide();
function searchFunction() {
    let input, filter, table, tr, td, td2, i, txtValue;
    input = document.getElementById("searchinput");
    filter = input.value.toUpperCase();
    table = document.getElementById("patientTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        td2 = tr[i].getElementsByTagName("td")[1];
        if (td || td2) {
            txtValue = td.textContent + " " + td2.textContent || td.innerText + " " + td2.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// This functions gets the administrators from the database if the user is a patient or a doctor.
// It then lists the administrators in HTML format with a link that takes the user to the
// chat.html page associated with the administrator.
function getAdmin(sessionID, role){
    $.ajax({
        url: 'http://10.1.144.91:8090/getAdmin',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data !== null) {
                let row = "";
                let chatID = null;
                // If the table is empty then add new rows to the table
                if ($("#patientTable tr").length <= 1) {
                    for (let i = 0; i < data.length; i++) {
                        chatID = sessionID + aes_decrypt(data[i][0], key, iv);
                        row += "<tr id='tableRow' style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[i][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][2], key, iv) + "</td>" +
                                "<td class='text-left'>Administrator</td>" +
                                "<td><a href='../pages/chat.html?chatRoomKey=" + aes_encrypt(chatID, key, iv) +
                                                                "&sessionID=" + aes_encrypt(sessionID, key, iv) +
                                                                "&userRole=" + aes_encrypt(role, key, iv) +
                                                                "&callerID=" + data[i][0] +
                                                                "&callerLastName=" + data[i][1] +
                                                                "&callerFirstName=" + data[i][2] +
                                                                "&callerRole=" + aes_encrypt("Administrator", key, iv) + "'>Chat</a></td>" +
                               "</tr>";
                    }
                    $("#patientTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                    $("#patientTable tbody").append(row);
                    return false;
                // If the table is not empty then append the new rows to the table.
                } else {
                    for (let k = 0; k < data.length; k++) {
                        chatID = sessionID + aes_decrypt(data[k][0], key, iv);
                        row += "<tr id='tableRow' style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[k][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[k][2], key, iv) + "</td>" +
                                "<td class='text-left'>Administrator</td>" +
                                "<td><a href='../pages/chat.html?chatRoomKey=" +  aes_encrypt(chatID, key, iv) +
                                                                "&sessionID=" + aes_encrypt(sessionID, key, iv) +
                                                                "&userRole=" + aes_encrypt(role, key, iv) +
                                                                "&callerID=" + data[k][0] +
                                                                "&callerLastName=" + data[k][1] +
                                                                "&callerFirstName=" + data[k][2] +
                                                                "&callerRole=" + aes_encrypt("Administrator", key, iv) + "'>Chat</a></td>" +
                               "</tr>";
                    }
                    $("#patientTable tbody").append(row);
                    return false;
                }
            }
        }
    });
}

// This functions gets the patients from the database if the user is an administrator or a doctor.
// It then lists the patients in HTML format with a link that takes the user to the
// chat.html page associated with the patient.
function getPatients(sessionID, role){
    $.ajax({
        url: 'http://10.1.144.91:8090/getPatients',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data !== null) {
                let row = "";
                let chatID = null;
                // If the table is empty then add new rows to the table.
                if ($("#patientTable tr").length <= 1) {
                    for (let i = 0; i < data.length; i++) {
                        chatID = "" + aes_decrypt(data[i][0], key, iv) + sessionID;
                        row += "<tr id='tableRow' style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[i][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][2], key, iv) + "</td>" +
                                "<td class='text-left'>Patient</td>" +
                                "<td><a href='../pages/chat.html?chatRoomKey=" + aes_encrypt(chatID, key, iv) +
                                                                "&sessionID=" + aes_encrypt(sessionID, key, iv) +
                                                                "&userRole=" + aes_encrypt(role, key, iv) +
                                                                "&callerID=" + data[i][0] +
                                                                "&callerLastName=" + data[i][1] +
                                                                "&callerFirstName=" + data[i][2] +
                                                                "&callerRole=" + aes_encrypt("Patient", key, iv) + "'>Chat</a></td>" +
                               "</tr>";
                    }
                    $("#patientTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                    $("#patientTable tbody").append(row);
                    return false;
                // If the table is not empty then append the new rows to the table.
                } else {
                    for (let k = 0; k < data.length; k++) {
                        chatID = "" + aes_decrypt(data[k][0], key, iv) + sessionID;
                        row += "<tr id='tableRow' style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[k][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[k][2], key, iv) + "</td>" +
                                "<td class='text-left'>Patient</td>" +
                                "<td><a href='../pages/chat.html?chatRoomKey=" + aes_encrypt(chatID, key, iv) +
                                                                "&sessionID=" + aes_encrypt(sessionID, key, iv) +
                                                                "&userRole=" + aes_encrypt(role, key, iv) +
                                                                "&callerID=" + data[k][0] +
                                                                "&callerLastName=" + data[k][1] +
                                                                "&callerFirstName=" + data[k][2] +
                                                                "&callerRole=" + aes_encrypt("Patient", key, iv) + "'>Chat</a></td>" +
                               "</tr>";
                    }
                    $("#patientTable tbody").append(row);
                    return false;
                }
            }
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });
}

// This functions gets the doctors from the database if the user is an administrator or a patient.
// It then lists the patients in HTML format with a link that takes the user to the
// chat.html page associated with the patient.
function getDoctors(sessionID, role){
    $.ajax({
        url: 'http://10.1.144.91:8090/getDoctors',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data !== null) {
                let row = "";
                let chatID = null;
                // If the table is empty then add new rows to the table
                if ($("#patientTable tr").length <= 1) {
                    for (let i = 0; i < data.length; i++) {
                        // If the user is a patient then combine the user ID first and then the
                        // caller ID to match with the chat room.
                        if (role === "Patient"){
                            chatID = sessionID + aes_decrypt(data[i][0], key, iv);
                        // If the user is not a patient then combine the caller ID first and then the
                        // user ID to match with the chat room .
                        }else{
                            chatID = "" + aes_decrypt(data[i][0], key, iv) + sessionID;
                        }
                        row += "<tr id='tableRow' style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[i][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][2], key, iv) + "</td>" +
                                "<td class='text-left'>Doctor</td>" +
                                "<td><a href='../pages/chat.html?chatRoomKey=" + aes_encrypt(chatID, key, iv) +
                                                                "&sessionID=" + aes_encrypt(sessionID, key, iv) +
                                                                "&userRole=" + aes_encrypt(role, key, iv) +
                                                                "&callerID=" + data[i][0] +
                                                                "&callerLastName=" + data[i][1] +
                                                                "&callerFirstName=" + data[i][2] +
                                                                "&callerRole=" + aes_encrypt("Doctor", key, iv) + "'>Chat</a></td>" +
                               "</tr>";
                    }
                    $("#patientTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                    $("#patientTable tbody").append(row);
                    return false;
                // If the table is not empty then append the new rows to the table.
                } else {
                    for (let k = 0; k < data.length; k++) {
                        // If the user is a patient then combine the user ID first and then the
                        // caller ID to match with the chat room.
                        if (role === "Patient"){
                            chatID = sessionID + aes_decrypt(data[k][0], key, iv);
                        // If the user is not a patient then combine the caller ID first and then the
                        // user ID to match with the chat room.
                        }else{
                            chatID = "" + aes_decrypt(data[k][0], key, iv) + sessionID;
                        }
                        row += "<tr id='tableRow' style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[k][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[k][2], key, iv) + "</td>" +
                                "<td class='text-left'>Doctor</td>" +
                                "<td><a href='../pages/chat.html?chatRoomKey=" + aes_encrypt(chatID, key, iv) +
                                                                "&sessionID=" + aes_encrypt(sessionID, key, iv) +
                                                                "&userRole=" + aes_encrypt(role, key, iv) +
                                                                "&callerID=" + data[k][0] +
                                                                "&callerLastName=" + data[k][1] +
                                                                "&callerFirstName=" + data[k][2] +
                                                                "&callerRole=" + aes_encrypt("Doctor", key, iv) + "'>Chat</a></td>" +
                               "</tr>";
                    }
                    $("#patientTable tbody").append(row);
                    return false;
                }
            }
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });
}

$(document).ready(function() {
    let sessionID = null;
    let role = null;
    // remove any existing rows
    $("#patientTable").find("tr:gt(0)").remove();
    // Get the role of the user. (Patient, Doctor, Administrator, and so on)
    $.ajax({
        url: 'http://10.1.144.91:8090/getRole',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },
        success: function(data) {
            // If the user is not logged in then redirect to the login page.
            if(data === "User is not logged in."){
                window.location = "../index.html";
                return false;
            }
            sessionID = aes_decrypt(data[0], key, iv);
            role = data[1];
            // If the user is a doctor then call the getAdmin() and getPatients() functions.
            if (role === "Doctor"){
                getAdmin(sessionID, role);
                getPatients(sessionID, role);
            // If the user is an administrator then call the getDoctors() and getPatients() functions.
            } else if (role === "Administrator"){
                getDoctors(sessionID, role);
                getPatients(sessionID, role);
            // If the user is a patient then call the getAdmin() and getDoctors() functions.
            } else if (role === "Patient"){
                getAdmin(sessionID, role);
                getDoctors(sessionID, role);
            }
        }
    });
});
/**
##################################################
 This file displays all of the scheduled appointments of
 the patient or doctor who is logged in.
##################################################
 YearMonthDayCreated: 2021-02-15
 Project: Open Source Engine Integration
 Program Name: schedule.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.2
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/02/15               Bao Mai            1             Create AJAX call to flask and display data from flask in HTML table format.
 2021/03/26               Aubrey Nickerson   2             Add Doctor and Patient functionality for schedule.
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
###################################################
 */
let key = "ddfbccae-b4c4-11";
let iv = "ddfbccae-b4c4-11";
$(document).ready(function() {
    let callerHeader = document.getElementById("callerHeader");
    // Delete any existing rows before entering the page
    $("#scheduleTable").find("tr:gt(0)").remove();
    // Make an AJAX call to the application route called /schedule
    // on the server to get the data of the users scheduled appointments.
    
    $.ajax({
        url: 'http://10.1.144.91:8090/schedule',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },
        // if the request is successful then the data will be returned to the user
        // in the "data" variable.
        success: function(data){
            let userRole = aes_decrypt(data[0][11], key, iv);
            // If the user is not logged in then they are redirected to the login page.
            if (data === "User is not logged in."){
                window.location = "../index.html";
                return false;
            }
            let row = ""
            if (data !== null) {
                if(userRole === "Patient"){
                    callerHeader.innerHTML = "Doctor";
                    for(let i = 0; i < data.length; i++){
                        row += "<tr style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[i][2], key, iv) + " " + aes_decrypt(data[i][3], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][5], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][9], key, iv) + "</td>" +
                               "</tr>";
                    }
                    $("#scheduleTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                    $("#scheduleTable tbody").append(row);
                    return false;
                }else{
                    callerHeader.innerHTML = "Patient";
                    for(let i = 0; i < data.length; i++){
                        row += "<tr style=\"height: 60px\">" +
                                "<td class='text-left'>" + aes_decrypt(data[i][0], key, iv) + " " + aes_decrypt(data[i][1], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][5], key, iv) + "</td>" +
                                "<td class='text-left'>" + aes_decrypt(data[i][9], key, iv) + "</td>" +
                               "</tr>";
                    }
                    $("#scheduleTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                    $("#scheduleTable tbody").append(row);
                    return false;
                }
            }
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    })
});
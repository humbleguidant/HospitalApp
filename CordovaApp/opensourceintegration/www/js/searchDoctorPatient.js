/**
##################################################
 This file handles the user input from searchDoctorPatient.html
 and sends the input to the database using AJAX requests.
 If successful, the database then sends data back to this
 file and displays the data in table format. If no data is
 found then it will return no data found notification.
##################################################
 YearMonthDayCreated: 2020-11-02
 Project: Open Source Engine Integration
 Program Name: searchDoctorPatient.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.1
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/03/21               Bao Mai            1             Set up first revision
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
// Check to see if the user logged in.
let key = "ddfbccae-b4c4-11";
let iv = "ddfbccae-b4c4-11";
function searchFunction() {
    var input, filter, list, item,txtValue;
    input = document.getElementById("searchinput");
    filter = input.value.toUpperCase();
    list = document.getElementsByClassName("list-item");
    for (i = 0; i < list.length; i++) {
        item = list[i].getElementsByTagName("td")[0];    
        if (item) {
            txtValue = item.textContent || item.innerText 
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                list[i].style.display = "";
            } else {
                list[i].style.display = "none";
            }
        }
    }
}

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
	let DocID = urlParams.get("DocID");
    // this AJAX function sends a request to the searchPatient() function in app.py
    // to check if the user exists in the database.
    $.ajax({
        url: 'http://10.1.144.91:8090/getDoctorPatients/' + DocID,
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
                var row = "";
                for (var i = 0; i < data.length; i++) {
                    row += "<a href='../pages/patientInfo.html?doctorPatientID="+ data[i][2] + "&DocID="+ DocID +"'>" +
                            "<div id='listItem" + i +"'" + " class=\"list-item\">" +
                                "<div class=\"item-detail\">" +
                                    "<table>" +
                                        "<tr>" +
                                            "<td class =\"patientName\">" + aes_decrypt(data[i][0], key, iv) + ", " +
                                                                            aes_decrypt(data[i][1], key, iv) + "</td>" +
                                        "</tr>" +
                                        "<tr>" +
                                            "<td class = \"PatID\"> PatID: " + aes_decrypt(data[i][2], key, iv) + "</td>" +
                                        "</tr>" +
                                        "<tr>" +
                                            "<td class = \"info\">" + getAge(aes_decrypt(data[i][4], key, iv)) + " years " +
                                                                      aes_decrypt(data[i][3],key, iv).charAt(0) + " DOB: " +
                                                                      aes_decrypt(data[i][4], key, iv) + "</td>" +
                                        "</tr>" +
                                    "</table>" +
                                "</div>" +
                            "</div>" +
                            "</a>";
				}
				$(".patientList").append(row);
                return false;
            }
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });
});

function getAge(dateString) {
    var today = new Date();
    var birthDate = new Date(dateString);
    var age = today.getFullYear() - birthDate.getFullYear();
    var m = today.getMonth() - birthDate.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}
/**
##################################################
 This file handles the user input from occupancyDetails.html
 and sends the input to the database using AJAX requests.
 If successful, the database then sends data back to this
 file and displays the data in table format. If no data is
 found then it will return no data found notification.
##################################################
 YearMonthDayCreated: 2021-03-20
 Project: Open Source Engine Integration
 Program Name: occupancyDetails.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.6
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/03/20               Keaton Canuel      6             Added AJAX calls
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
    var input, filter, table, tr, td, td2, i, txtValue;
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

    // this AJAX function sends a request to the searchLocation() function in app.py
    // to check if the user exists in the database.
    $.ajax({
        url: 'http://10.1.144.91:8090/searchLocation',
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
                let row = "";
                for (var i = 0; i < data.length; i++) {
                    row += "<tr id='tableRow" + i + "'" + " style=\"height: 60px\">" +
                            "<td class='text-left'>" + aes_decrypt(data[i][0], key, iv) + "</td>" +
                            "<td class='text-left'>" + aes_decrypt(data[i][1], key, iv) + "</td>" +
                            "<td class='text-left'>" + aes_decrypt(data[i][2], key, iv) + "</td>" +
                            "<td class='text-left'>" + aes_decrypt(data[i][3], key, iv) + "</td>" +
                            "<td class='text-left'>" + aes_decrypt(data[i][4], key, iv) + "</td>" +
                           "</tr>";
				}
				
				
                $("#patientTable").append("<tbody class=\"table-hover\" style=\"height: 20px\"></tbody>");
                $("#patientTable tbody").append(row);
                return false;
            }
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });
});
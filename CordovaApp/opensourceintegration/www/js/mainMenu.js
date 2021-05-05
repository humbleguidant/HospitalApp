/**
##################################################
 This file checks to see if the user is logged in before
 they proceed to the main menu. It makes an AJAX call
 to the flask server checking if a session id exists.
 If the ID does not exist then that means the user is
 not logged in and is redirected to the sign in page.
##################################################
 YearMonthDayCreated: 2021-02-01
 Project: Open Source Engine Integration
 Program Name: mainMenu.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.2
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/02/01               Aubrey Nickerson   1             Creating AJAX call to flask server if user logged in or not.
 2021/03/27               Aubrey Nickerson   2             Change main menu to be dynamic for patients, doctors, and administration.
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
$(document).ready(function() {
    $.ajax({
        // check the flask application route called checkSession
        // to see if the user exists.
        url: 'http://10.1.144.91:8090/checkUserMainMenu',
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
            // If the user is not logged in then they are redirected to the login page.
            if(data === "User is not logged in."){
                window.location = "../index.html";
                return false;
            }
            // If the user is a doctor, then display the doctors menu.
            if(data === "Doctor"){
                document.getElementById("header").innerHTML = "Doctors Menu"
                $("#signOut").before("<a id='schedule' href=\"../pages/schedule.html\"><div class=\"menu-btn\"><i class=\"fas fa-calendar-alt\"></i>Schedule</div></a>");
                $("#schedule").before("<a id='searchPatient' href=\"../pages/searchPatient.html\"><div class=\"menu-btn\"><i class=\"fas fa-search\"></i>Search Patients</div></a>");
            // If the user is a patient, then display the patients menu.
            } else if(data === "Patient"){
                document.getElementById("header").innerHTML = "Patients Menu"
                $("#signOut").before("<a id='schedule' href=\"../pages/schedule.html\"><div class=\"menu-btn\"><i class=\"fas fa-calendar-alt\"></i>Schedule</div></a>");
            // If the user is an administrator, then display the administrators menu.
            } else {
                document.getElementById("header").innerHTML = "Administrators Menu"
                $("#signOut").before("<a id='occupancy' href=\"../pages/occupancyOverview.html\"><div class=\"menu-btn\"><i class=\"fas fa-users\"></i>Occupancy</div></a>");
                $("#occupancy").before("<a href=\"../pages/searchDoctor.html\"><div class=\"menu-btn\"><i class=\"fas fa-search\"></i>Search Doctors</div></a>");
            }
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });
});
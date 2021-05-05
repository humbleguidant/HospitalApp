/**
##################################################
 This file handles the user input from index.html
 which is the user login form. It checks if the user
 enters a valid email address and if the email address
 and password exists in the database. If the email and
 password are correct then it will check the role of the
 user if its a patient, admin, doctor, or physician. If it
 matches any of those roles then it is taken to a specific
 menu depending on the role.
##################################################
 YearMonthDayCreated: 2020-11-09
 Project: Open Source Engine Integration
 Program Name: signIn.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.6
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2020/11/09               Aubrey Nickerson   1             Set up first draft.
 2020/11/13               Aubrey Nickerson   2             Testing connection to database.
 2020/11/16               Aubrey Nickerson   3             Search for users from database.
 2020/11/18               Aubrey Nickerson   4             Add functionality to check if email is valid.
 2020/11/20               Aubrey Nickerson   5             Check if user exists in db.
 2021/02/18               Aubrey Nickerson   6             Added if statements to check the role of the user before accessing main menu.
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
// Destroy the users session ID since they are on the login page.
$(document).ready(function() {
    let key = "ddfbccae-b4c4-11"
    let iv = "ddfbccae-b4c4-11"
    $.ajax({
        url: 'http://10.1.144.91:8090/destroySession',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },
        complete: function(){
            $('#loader').addClass('hidden')
        }
    });
    // Add action event when button is clicked.
    $("#submit").click(function() {
        // Assign the user input to variables.
        var emailInput = document.getElementById("inputEmail").value;
        var passwordInput = document.getElementById("inputPassword").value.toString();
        // Remove special characters from email.
        var regex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        // If the user did not insert an email and password then they
        // cannot proceed.
        if(emailInput.length === 0 || passwordInput.length === 0){
            alert("Email or Password cannot be empty.");
            return false;
        // Or if the user inserts special characters or numbers in the email then they
        // cannot get results.
        }else if(!regex.test(emailInput)) {
            alert("You have entered an invalid email address.");
            return false;
        }

        let encryptEmail = aes_encrypt(emailInput, key, iv);
        let encryptPassword = aes_encrypt(passwordInput, key, iv);
        let dataString = "email=" + encryptEmail + "&password=" + encryptPassword;
        // this AJAX function sends a request to the signIn() function in app.py
        // to check if the user exists in the database.
        $.ajax({
            url: 'http://10.1.144.91:8090/signIn',
            data: dataString,
            type: 'GET',
            crossDomain: true,
            cache: false,
            beforeSend: function() {
                $('#loader').removeClass('hidden')
            },
            // if the request is successful then the data will be saved and check the status.
            success: function(data){
                // If the data does not equal the below conditions. Then check the user roles.
                // Then the user will be taken to their specific main menu depending which role they are.
                if(data !== "This email does not exist in the system. Please contact administration." && data !== "The password is incorrect. Please try again or contact administration."){
                    window.location = "pages/mainMenu.html";
                    return false;
                }
                alert(data);
                return false;
            },
            complete: function(){
                $('#loader').addClass('hidden')
            },
        });
    return false;
    });
});
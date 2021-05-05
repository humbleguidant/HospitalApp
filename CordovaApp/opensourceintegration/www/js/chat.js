/**
##################################################
 This file handles the chat and chat history between the user and
 caller. Before the user accesses the page,
 this file checks if they are logged in or not. After checking if they
 logged in then they will get the users chat history with the caller.
 After getting the chat history the file will connect a socket with
 the python flask server so that the user can send and receive messages
 in real time.
##################################################
 YearMonthDayCreated: 2021-02-05
 Project: Open Source Engine Integration
 Program Name: chat.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.5
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/02/05               Aubrey Nickerson   1             Created AJAX getSession() function to check if the user is logged in.
 2021/02/07               Aubrey Nickerson   2             Added URL params get functions and another AJAX function called
                                                           checkChatID().
 2021/02/08               Aubrey Nickerson   3             Added getChatHistory() to get the history of messages between
                                                           the user and the caller. Display in HTML & CSS format.
 2021/02/09               Aubrey Nickerson   4             Connect socket.io to the python flask server to send and rece-
                                                           ive messages in real time.
 2021/03/04               Aubrey Nickerson   5             Add encryption functionality.
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
// This function checkChatID() makes an AJAX call to the python flask application route called
// checkChatIDto get the Chat Room ID.// The chat ID, user ID, user role (Patient, Doctor, and so on),
// caller ID, caller role are passed as parameters to the server. If the chat room ID does
// not exist then a new chat room will be created. If there is already a chat room ID that
// matches then proceed as usual.

let key = "ddfbccae-b4c4-11";
let iv = "ddfbccae-b4c4-11";
let sessionID = null;

function checkChatID(chatID, userID, userRole, callerID, callerRole){
    $.ajax({
        url: 'http://10.1.144.91:8090/checkChatID/' + chatID + '/' + userID + '/' + userRole + '/' + callerID + '/' + callerRole,
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        }
    });
}

$(document).ready(function(){
    // Make an AJAX call to python application route called getSession
    $.ajax({
        url: 'http://10.1.144.91:8090/getSession',
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        // If the call was successful then check if the user logged in.
        // If not then redirect them back to the login page.
        success: function(data) {
            if(data === "User is not logged in."){
                window.location = "../index.html";
                return false;
            }
            // If the user logged in then get the session ID.
            sessionID = aes_decrypt(data, key, iv);
        }
    });
    // Grab the URL parameters from the list of chat links that the user
    // clicked on in chatRoomSelect.html
    let queryString = window.location.search;
    let urlParams = new URLSearchParams(queryString);
    let chatID = urlParams.get("chatRoomKey");
    let userID = urlParams.get("sessionID");
    let userRole = urlParams.get("userRole");
    let callerID = urlParams.get("callerID");
    let callerRole = urlParams.get("callerRole");
    $("h1").text(aes_decrypt(urlParams.get("callerFirstName"), key, iv) + " " + aes_decrypt(urlParams.get("callerLastName"), key, iv));
    // call the checkChatID() function to pass the URL parameters
    // to the python application route and check if the chat room exists.
    checkChatID(chatID, userID, userRole, callerID, callerRole);
    // Display the callers first name and last name on the header.

    // Make another AJAX call to the python application route getChatHistory
    // and get the chat history between the user and the caller.
    $.ajax({
        url: 'http://10.1.144.91:8090/getChatHistory/' + chatID,
        data: null,
        type: 'GET',
        crossDomain: true,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data){
            // If there is no chat history then return nothing.
            if(data === null){
                return false;
            }
            // If there is chat history available then display all the
            // data of the chat history in html format.
            let newMessage = "";
            for(var i = 0; i < data.length; i++){
                // If the user ID from the database matches the session ID
                // of the user then display all the users messages in blue.
                if(data[i][0].toString() === sessionID){
                    newMessage = $("<div class='container darker'></div>");
                    newMessage.append("<img src=\"../img/contact.jpg\" alt=\"Avatar\" class=\"right\" style=\"width:100%;\">\n" +
                                      "<p>" + aes_decrypt(data[i][1], key, iv) + "</p>\n" +
                                      "<span class=\"time-left\">" + data[i][2] + "</span>");
                    $("#messages").append(newMessage);
                // If the user ID does not match the session ID then that means
                // it is the callers ID. So display the messages in white.
                }else{
                    newMessage = $("<div class='container'></div>");
                    newMessage.append("<img src=\"../img/contact.jpg\" alt=\"Avatar\" style=\"width:100%;\">\n" +
                                      "<p>" + aes_decrypt(data[i][1], key, iv)  + "</p>\n" +
                                      "<span class=\"time-right\">" + data[i][2]  + "</span>");
                    $("#messages").append(newMessage);
                }
            }
            // After all messages are displayed, scroll to the bottom of the most recent message.
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        },
        complete: function(){
            $('#loader').addClass('hidden')
        },
    });

    // Connect the JavaScript socket to the python flask socket with the IP below.
    var socket = io.connect('http://10.1.144.91:8090');

    // Connect to the message function in Python that handles the messages in real time
    socket.on('message', function(msg){
        // If the user ID matches the session ID and the chat room ID matches the users chat room ID
        // then display the message in blue. This means that this is the user who sent the message in
        // real time.
        if(aes_decrypt(msg.ID, key, iv) === sessionID && aes_decrypt(msg.chatID, key, iv) === aes_decrypt(chatID, key, iv)){
            let newMessage = $("<div class='container darker'></div>");
            newMessage.append("<img src=\"../img/contact.jpg\" alt=\"Avatar\" class=\"right\" style=\"width:100%;\">\n" +
                              "<p>" + aes_decrypt(msg.userMessage, key, iv) + "</p>\n" +
                              "<span class=\"time-left\">" + aes_decrypt(msg.currentTime, key, iv) + "</span>");
            $("#messages").append(newMessage);
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        // If the user ID does not match the session ID then that means the caller ID is the one
        // who sent the message to the user in real time.
        } else if(aes_decrypt(msg.ID, key, iv) !== sessionID && aes_decrypt(msg.chatID, key, iv) === aes_decrypt(chatID, key, iv)) {
            let newMessage = $("<div class='container'></div>");
            newMessage.append("<img src=\"../img/contact.jpg\" alt=\"Avatar\" style=\"width:100%;\">\n" +
                              "<p>" + aes_decrypt(msg.userMessage, key, iv) + "</p>\n" +
                              "<span class=\"time-right\">" + aes_decrypt(msg.currentTime, key, iv) + "</span>");
            $("#messages").append(newMessage);
            $("html, body").animate({ scrollTop: $(document).height() }, 1000);
        }
    });

    // Send the message with the user and chat ID
    // to python socket as soon as the button is
    // clicked.
    $("#innerbutton").click(function() {
        let date = new Date();
        date = moment(date).format('YYYY-MM-DD HH:mm:ss');
        if (!$('#message').val()){
            alert("Message cannot be empty.");
            return false;
        }
        socket.emit('message', {
            chatID: chatID,
            ID: aes_encrypt(sessionID, key, iv),
            userMessage: aes_encrypt($('#message').val(), key, iv),
            currentTime: aes_encrypt(date, key, iv)
        });
        $('#message').val('');
        return false;
    });
});

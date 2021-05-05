/**
 ##################################################
 This program handles AES encryption and decryption.
 the aes_encryption function is referenced on other JS files
 in the program as well as the aes_decryption function.
 ##################################################
 YearMonthDayCreated: 2021-02-18
 Project: Open Source Engine Integration
 Program Name: jsAES.js
 Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
 Copyright: Copyright 2021
 Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
 License: MIT License
 Version: 1.1
 Maintainer: Okanagan College Team
 Status: Working
 Revision History:
 Date (YYYY/MM/DD)        Author             Revision      What was changed?
 2021/02/18               Aubrey Nickerson   1             Set up encryption and decryption functions.
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
function aes_encrypt(plaintext, key, iv) {
    key = CryptoJS.enc.Utf8.parse(key)
    iv = CryptoJS.enc.Utf8.parse(iv)
    let srcs = CryptoJS.enc.Utf8.parse(plaintext)
    let encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    })
    return encrypted.ciphertext.toString()
}


function aes_decrypt(ciphertext, key, iv) {
    key = CryptoJS.enc.Utf8.parse(key)
    iv = CryptoJS.enc.Utf8.parse(iv)
    let hex_string = CryptoJS.enc.Hex.parse(ciphertext)
    let srcs = CryptoJS.enc.Base64.stringify(hex_string)
    let decrypt = CryptoJS.AES.decrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    })
    decrypt = decrypt.toString(CryptoJS.enc.Utf8)
    return decrypt.toString()
}

##################################################
## This program handles the AES encryption and decryption
## the encryption function is referenced on app.py
## as well as the decryption function.
##################################################
## YearMonthDay: 2020-11-02
## Project: Open Source Engine Integration
## Program Name: PyAES.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.1
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 03/07/2021  Aubrey Nickerson   1             Set up first draft.
##################################################
## MIT License
## Copyright 2021 Okanagan College & Harris Healthcare

## Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
## associated documentation files (the "Software"), to deal in the Software without restriction, including 
## without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
## copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
## OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
## LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
## IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## End license text.
##################################################
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


class AesCrypto(object):
    def __init__(self, key):
        self.key = key.encode('utf-8')[:16]
        self.iv = self.key
        self.mode = AES.MODE_CBC

    @staticmethod
    def pkcs7_padding(data):
        if not isinstance(data, bytes):
            data = data.encode()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def encrypt(self, plaintext):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plaintext = plaintext
        plaintext = self.pkcs7_padding(plaintext)
        ciphertext = cryptor.encrypt(plaintext)
        return b2a_hex(ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        cryptor = AES.new(self.key, self.mode, self.iv)
        plaintext = cryptor.decrypt(a2b_hex(ciphertext))
        return bytes.decode(plaintext).rstrip('\0')



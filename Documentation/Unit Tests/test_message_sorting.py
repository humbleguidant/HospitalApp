##################################################
## This program receives HL7 medical messages from a sender.
## As soon as the program starts, it waits to receive messages
## once it receives the message it displays the received message
## and sends the a message back to the user that it was received.
##################################################
## {License_info}
##################################################
## YearMonthDay:
## Project: Open Source Engine Integration
## Program Name: testHL7Receiver.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2020
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: Harris Smartworks
## Version: 1.0.0
## Maintainer: Okanagan College Team
## Status: Working
## Revision History:
## Date        Author             Revision      What was changed?
## 11/15/2020  Bao Mai            1             Whole message sorted
##################################################
import unittest
import hl7
from message_sorting import message_sorting
class TestMessageSorting(unittest.TestCase):

    def test_message_1(self):
        message = 'MSH|^~&|AccMgr|1|||20050112154645||ADT^A03|59912415|P|2.3||| EVN|A03|20050112154642|||||\r'
        message += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111^DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
        message += 'PV1|1|I|IN1^214^1^1^^^S|3||IN1^214^1|37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4||||||||||||||||1|||1||P|||20050110045253|20050112152000|3115.89|3115.89|||\r'
        self.assertEqual(message_sorting(message)["PV1.5"],'Empty')

    def test_message_2(self):
        message = 'MSH|^~&|AccMgr|1|||20050112154645||ADT^A03|59912415|P|2.3||| EVN|A03|20050112154642|||||\r'
        message += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111^DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
        message += 'PV1|1|I|IN1^214^1^1^^^S|3||IN1^214^1|37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4||||||||||||||||1|||1||P|||20050110045253|20050112152000|3115.89|3115.89|||\r'
        self.assertEqual(message_sorting(message)["PID.1"],'1')

    def test_message_3(self):
        message = 'MSH|^~&|AccMgr|1|||20050112154645||ADT^A03|59912415|P|2.3||| EVN|A03|20050112154642|||||\r'
        message += 'EVN|A01|20050110045502|||||\r'
        message += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111^DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
        message += 'PV1|1|I|IN1^214^1^1^^^S|3||IN1^214^1|37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4||||||||||||||||1|||1||P|||20050110045253|20050112152000|3115.89|3115.89|||\r'
        self.assertEqual(message_sorting(message)["EVN.1"],'A01')
        self.assertEqual(message_sorting(message)["EVN.2"],'20050110045502')

    def test_message_4(self):
        message = 'MSH|^~&|AccMgr|1|||20050112154645||ADT^A03|59912415|P|2.3||| EVN|A03|20050112154642|||||\r'
        message += 'EVN|A01|20050110045502|||||\r'
        message += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111^DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
        message += 'PV1|1|I|IN1^214^1^1^^^S|3||IN1^214^1|37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4||||||||||||||||1|||1||P|||20050110045253|20050112152000|3115.89|3115.89|||\r'
        self.assertEqual(message_sorting(message)["MSH.9"],'ADT')

    def test_message_5(self):
        message = 'MSH|^~&|AccMgr|1|||20050112154645||ADT^A03|59912415|P|2.3||| EVN|A03|20050112154642|||||\r'
        message += 'EVN|A01|20050110045502|||||\r'
        message += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111^DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
        message += 'PV1|1|I|IN1^214^1^1^^^S|3||IN1^214^1|37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4||||||||||||||||1|||1||P|||20050110045253|20050112152000|3115.89|3115.89|||\r'
        self.assertEqual(message_sorting(message)["PV1.1"],'1')



if __name__ == '__main__':
    unittest.main()

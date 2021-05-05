##################################################
## This program sends HL7 medical messages to a receiver.
## As soon as the program starts, it sends a message to
## the receiver and then the receiver sends a message back
## that it was received.
##################################################
## YearMonthDay: 2020-11-09
## Project: Open Source Engine Integration
## Program Name: testHL7Listener.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.0.0
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 11/02/2020  Aubrey Nickerson   1             Set up first draft
##################################################
"""
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
"""

import aiorun
import asyncio
import hl7
import message_sorting 
from hl7.mllp import open_hl7_connection


async def main():
  
    message0 = 'MSH|^~&|AccMgr|1|||20050110045504||ADT^A01|599102|P|2.3|||\r'
    message0 += 'EVN|A01|20171222|20171222|02|ABBOTT^LORI^M|20171222\r' 
    message0 += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111 DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
    message0 += 'NK1|1|DUCK^HUEY|SO|3583 DUCK RD^^FOWL^CA^999990000|8885552222||Y||||||||||||||\r' 
    message0 += 'PV1|1|I|PREOP^101^1^1^^^S|3|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4|||||||||||||||||||1||G|||20050110045253||||||\r'  
    message0 += 'DG1|1|I9|71596^OSTEOARTHROS NOS-L/LEG ^I9|OSTEOARTHROS NOS-L/LEG ||A|\r'
    message0 += 'OBX|1|NM|^Body Height||1.80|m^Meter^ISO+|||||F\r'
    
    message = 'MSH|^~\&|EPIC|EPICADT|SMS|SMSADT|199912271408|CHARRIS|ADT^A04|1817457|D|2.5|\r'
    message +='PID||0493575^^^2^ID 1|454721||DOE^JOHN^^^^|DOE^JOHN^^^^|19480203|M||B|254 MYSTREET AVE^^MYTOWN^OH^44123^USA||(216)123-4567|||M|NON|400003403~1129086|\r'
    message +='NK1||ROE^MARIE^^^^|SPO||(216)123-4567||EC|||||||||||||||||||||||||||\r'
    message +='PV1||O|168 ~219~C~PMA^^^^^^^^^||||277^ALLEN MYLASTNAME^BONNIE^^^^|||||||||| ||2688684|||||||||||||||||||||||||199912271408||||||002376853\r'
    
    message1 = 'MSH|^~\&|AccMgr|1|||20050110045504||ADT^A01|599102|P|2.3|||\r'
    message1 += 'EVN|A01|20050110045502|||||\r' 
    message1 += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111 DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r' 
    message1 += 'NK1|1|DUCK^HUEY|SO|3583 DUCK RD^^FOWL^CA^999990000|8885552222||Y||||||||||||||\r' 
    message1 += 'PV1|1|I|PREOP^101^1^1^^^S|3|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4|||||||||||||||||||1||G|||20050110045253||||||\r' 
    message1 += 'GT1|1|8291|DUCK^DONALD^D||111^DUCK ST^^FOWL^CA^999990000|8885551212||19241010|M||1|123121234||||#Cartoon Ducks Inc|111^DUCK ST^^FOWL^CA^999990000|8885551212||PT|\r' 
    message1 += 'DG1|1|I9|71596^OSTEOARTHROS NOS-L/LEG ^I9|OSTEOARTHROS NOS-L/LEG ||A|\r' 
    message1 += 'IN1|1|MEDICARE|3|MEDICARE|||||||Cartoon Ducks Inc|19891001|||4|DUCK^DONALD^D|1|19241010|111^DUCK ST^^FOWL^CA^999990000|||||||||||||||||123121234A||||||PT|M|111 DUCK ST^^FOWL^CA^999990000|||||8291\r' 
    
    
    message_2 ="MSH|^~&|DATICA|DATICA HOSPITAL^^12345^^^DATICA HEALTHCARE|EXTERNAL EMR|EXTERNAL CLINIC|20171031||SIU^S12|1334068|T|2.3|\r"
    message_2 +="SCH|4624613|860506||5440109||BOOKED|CHECKUP|COMPLETE|30|MIN|^^^201711011000|73045493^FROST^BRUCE|8195377845|9767 ELM LN^^MADISON^NC^99258|XXPOC^268^3^DATICA HOSPITAL E|44151427^HAYS^MARILYN|8487719912|2126 ELM TER^^MADISON^NH^93493|XXPOC^437^2^DATICA HOSPITAL F|73045493^FROST^BRUCE|8195377845|XXPOC^187^0^DATICA HOSPITAL E|2964510|4752831|BOOKED|\r"
    message_2 +="NTE|1|TX|SOME NOTES ABOUT THE PATIENT GO HERE.\r"
    message_2 +="PID|1|93816095|38427039^2342234|81337786|NOBLE^BENJAMIN|FROST|19410513|M|SKIPPY|H|6188 HAWTHORN LN^^MADISON^UT^99767|99767|8324546834|8745990079|ID|UNK|JEW|991143^8237283|994736939|S584096999984789||H|MADISON|Y|3|US||US^UNITED STATES OF AMERICA||N||\r"
    message_2 +="PV1|1|P|XXPOC^901^0^DATICA HOSPITAL A|A|234570|XXPOC^852^1^DATICA HOSPITAL B|29763487^CANTRELL^JESSICA^F^^NP|35192786^PHELPS^MARIA^G^^CRNA|92980930^LYNN^MARIA^N^^PA|CAR|XXPOC^649^3^DATICA HOSPITAL A|N||8|B6||64295772^BELTRAN^JASON^X^^MD|U|211419^345454|A23|R|N|G|44|20151212|66.14|1|C|B|||||||||||||||\r"
    #message_2 +="PV2|XXPOC^235^1^DATICA HOSPITAL D|ZD|H54.2^LOW VISION, BOTH EYES^ICD-10||RING|FRONTDESK A|TE|||||||||||||||||||||||||||||||\r"
    #message_2 +="OBX|1|NM|103939^MCV^L^787-2^ERYTHROCYTE MEAN CORPUSCULAR VOLUME^LN||87|FL|79-97|||N|F|20160316||20160318|CB^PATHOLOGY LAB X|||\r"
    message_2 +="DG1|1||G43.11^MIGRANE WITH AURA,INTRACTABLE^ICD-10||20160824|F|\r"
    message_2 +="RGS|1||69718723\r"
    message_2 +="AIS|1||960847|20170710|||30|MIN|CONFIRM|BOOKED\r"
    message_2 +="NTE|2|TX|THE PATIENT CAN'T SEE WHAT I TYPED IN THE CHART\r"
    message_2 +="AIG|1||A4259^LANCETS, PER BOX OF 100^HCPCS|||||20170710|||30|MIN|CONFIRM|BOOKED\r"
    message_2 +="NTE|3|TX|I LIKED THE OLD PAPER CHARTS BETTER\r"
    message_2 +="AIL|1||5497|||20170710|||30|MIN|YES|BOOKED\r"
    message_2 +="NTE|4|TX|THE PATIENT CAN'T SEE WHAT I TYPED IN THE CHART\r"
    message_2 +="AIP|1||16955873^WATTS^HAROLD^Z^^PA|||20170711|||||NOTIFY|BOOKED\r"
    message_2 +="NTE|5|TX|THE PATIENT CAN'T SEE WHAT I TYPED IN THE CHART\r"

    Orm_mess ="MSH|^~&|DATICA|DATICA HOSPITAL^^12345^^^DATICA HEALTHCARE|EXTERNAL EMR|EXTERNAL CLINIC|20171222||ORM^O01|2518976|T|2.3|\r"
    Orm_mess +="NTE|1|TX|THE PATIENT CAN'T SEE WHAT I TYPED IN THE CHART\r"
    Orm_mess +="PID|1|54|73121932|83906432|MUELLER^JACOB|CANTRELL|19350401|M|BOOMER|U|8804 HAWTHORN WAY^^MADISON^VT^92901|92901|8732131395|8198276991|SR|T|MSH|237250|934772637|S110431226262678||N|MADISON|Y|5|US||US^UNITED STATES OF AMERICA||N||\r"
    #Orm_mess += "PD1|M|U|DATICA HOSPITAL^^12345^^^DATICA HEALTHCARE|28225098^PUGH^JEREMY^X^^MD|F||F|I|N||O|Y\r"
    Orm_mess +="NTE|2|TX|THE PATIENT CAN'T SEE WHAT I TYPED IN THE CHART\r"
    Orm_mess +="PV1|1|I|XXPOC^531^1^DATICA HOSPITAL A|E|519243|XXPOC^346^2^DATICA HOSPITAL B|42850944^HARPER^ROY^T^^MD|30341899^HAYS^MICHELLE^Y^^CRNA|86517642^SHERMAN^EMILY^M^^NP|PUL|XXPOC^457^1^DATICA HOSPITAL A|N||2|A3||59047365^ROSS^CHRISTINA^F^^NP|U|120635|A23|R|N|G|44|20150617|204.15|7|C|B|||||||||||||||\r"
    Orm_mess +="IN1|1|H95277524|31546844|DATICA INSURANCE CO|4684 CEDAR LN^^MADISON^OK^93735||8713182252|632048|INSURANCE GROUP P|671473343|ACME GROUP|20161020|20190125|A871795941|MCD|MUELLER^JACOB^A|SELF|19350401|8804 HAWTHORN WAY^^MADISON^VT^92901|Y|CO|1|N||N||N||20160110||U|||||Z508519821|0|||||U|M|6488 JUNIPER AVE^^MADISON^IN^98341||V92259627|H||32427285\r"
    Orm_mess +="GT1|1|73453718|WELCH^LOUIS^T||9346 JUNIPER CT^^MADISON^TN^96814|8081692370|8990121899|18980412|M|||904374124|20120514||1||||102762|U||N|||N||||5236781249|A||||||ILO|U||N|F|ANG|MONTES|USA|N|||||SOFTWARE DEVELOPER||||U||O\r"
    Orm_mess +="AL1|1|DA|F828984490^AZITHROMYCIN^^FROM ZITHROMAX Z-PAK|MO|NAUSEA|20150404\r"
    Orm_mess +="ORC|RE|994330981|578195160|G|CM||||||||||||||\r"
    Orm_mess +="NTE|3|TX|I LIKED THE OLD PAPER CHARTS BETTER\r"
    Orm_mess +="OBR|1|110404676^DATICAORD|899383980^DATICAORD|32825^GEN SCREENING|||20160921|20160921||20251671^MONTES^BARBARA^O^^CRNA|L|||||20251671^MONTES^BARBARA^O^^CRNA|8826404367\r "
    Orm_mess +="DG1|1||E11.42^TYPE 2 DIABETES MELLITUS WITH DIABETIC POLYNEUROPATHY^ICD-10||20160201|F\r "
    Orm_mess +="OBX|1|NM|864273^HEMATOCRIT^L^4544-3^HEMATOCRIT^LN||37.6|%|34.0-46.6|||N|F|20160914||20160921|CB^PATHOLOGY LAB X||\r "
    Orm_mess +="NTE|3|TX|THE PATIENT CAN'T SEE WHAT I TYPED IN THE CHART\r "
    
    # Open the connection to the HL7 receiver.
    # Using wait_for is optional, but recommended so
    # a dead receiver won't block you for long
    hl7_reader, hl7_writer = await asyncio.wait_for(
        open_hl7_connection("127.0.0.1", 2575),
        timeout=10,
    )

    hl7_message = hl7.parse(Orm_mess)

    # Write the HL7 message, and then wait for the writer
    # to drain to actually send the message
    hl7_writer.writemessage(hl7_message)
    await hl7_writer.drain()
    print(f'Sent message\n {hl7_message}'.replace('\r', '\n'))

    # Now wait for the ACK message from the receiever
    hl7_ack = await asyncio.wait_for(
      hl7_reader.readmessage(),
      timeout=10
    )
    print(f'Received ACK\n {hl7_ack}'.replace('\r', '\n'))


aiorun.run(main(), stop_on_unhandled_errors=True)
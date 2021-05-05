##################################################
## This program receives HL7 medical messages from a sender.
## As soon as the program starts, it waits to receive messages
## once it receives the message it displays the received message
## and sends the a message back to the user that it was received.
##################################################
## YearMonthDay:
## Project: Open Source Engine Integration
## Program Name: testHL7Receiver.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.0.0
## Maintainer: Okanagan College Team
## Status: Working
## Revision History: 
## Date        Author             Revision      What was changed?
## 11/15/2020  Bao Mai            1             Whole message sorted
## 11/22/2020  Bao Mai            2             Return the message in dictionary
## 11/30/2020  Bao Mai            3             Convert hl7 message to readable json file
## 03/31/2020  Bao Mai            4             Stored Repetition and Repeated Segment
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
import json
import hl7
import time
import requests
import os

message1 =  'MSH|^~&|ADT1|GOOD HEALTH HOSPITAL|GHH LAB, INC.|GOOD HEALTH HOSPITAL|198808181126|SECURITY|ADT^A01^ADT_A01|MSG00001|P|2.8\r'
message1 += 'EVN|A01|200708181123\r'
message1 += 'PID|1PATID1234^5^M11^ADT1^MR^GOOD HEALTH HOSPITAL~123456789^^^USSSA^SSEVERYMAN^ADAM^A^III19610615|MC|2222 HOME STREET^^GREENSBORO^NC^27401-1020|GL|(555) 555-2004|(555)555-2004SPATID12345001^2^M10^ADT1^AN^A|444333333|987654^NC|\r'
message1 += 'NK1|1|NUCLEAR^NELDA^W|SPO^SPOUSE||NK^NEXT OF KIN\r'
message1 += 'PV1|1|I|2000^2012^01004777^ATTEND^AARON^A|SUR||||ADM|A0|\r'

message = 'MSH|^~\&|EPIC|EPICADT|SMS|SMSADT|199912271408|CHARRIS|ADT^A04|1817457|D|2.5|\r'
message +='PID||0493575^^^2^ID 1|454721||DOE^JOHN^^^^|DOE^JOHN^^^^|19480203|M||B|254 MYSTREET AVE^^MYTOWN^OH^44123^USA||(216)123-4567|||M|NON|400003403~1129086|\r'
message +='NK1||ROE^MARIE^^^^|SPO||(216)123-4567||EC|||||||||||||||||||||||||||\r'
message +='PV1||O|168~219~C~PMA^^^^^^^^^||||277^ALLEN MYLASTNAME^BONNIE^^^^|||||||||| ||2688684|||||||||||||||||||||||||199912271408||||||002376853\r'

message0 = 'MSH|^~&|AccMgr|1|||20050110045504||ADT^A01|599102|P|2.3|||\r'
message0 += 'EVN|A01|20171222|20171222|02|ABBOTT^LORI^M|20171222\r' 
message0 += 'PID|1||10006579^^^1^MRN^1||DUCK^DONALD^D||19241010|M||1|111 DUCK ST^^FOWL^CA^999990000^^M|1|8885551212|8885551212|1|2||40007716^^^AccMgr^VN^1|123121234|||||||||||NO\r'
message0 += 'NK1|1|DUCK^HUEY|SO|3583 DUCK RD^^FOWL^CA^999990000|8885552222||Y||||||||||||||\r' 
message0 += 'PV1|1|I|PREOP^101^1^1^^^S|3|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|||01||||1|||37^DISNEY^WALT^^^^^^AccMgr^^^^CI|2|40007716^^^AccMgr^VN|4|||||||||||||||||||1||G|||20050110045253||||||\r'  
message0 += 'DG1|1|I9|71596^OSTEOARTHROS NOS-L/LEG ^I9|OSTEOARTHROS NOS-L/LEG ||A|\r'
message0 += 'OBX|1|NM|^Body Height||1.80|m^Meter^ISO+|||||F\r' 

message_2 ="MSH|^~&|DATICA|DATICA HOSPITAL^^12345^^^DATICA HEALTHCARE|EXTERNAL EMR|EXTERNAL CLINIC|20171031||SIU^S12|1334068|T|2.3|\r"
message_2 +="SCH|4624613|860506||5440109||BOOKED|CHECKUP|COMPLETE|30|MIN|^^^201711011000|73045493^FROST^BRUCE|8195377845|9767 ELM LN^^MADISON^NC^99258|XXPOC^268^3^DATICA HOSPITAL E|44151427^HAYS^MARILYN|8487719912|2126 ELM TER^^MADISON^NH^93493|XXPOC^437^2^DATICA HOSPITAL F|73045493^FROST^BRUCE|8195377845|XXPOC^187^0^DATICA HOSPITAL E|2964510|4752831|BOOKED|\r"
message_2 +="NTE|1|TX|SOME NOTES ABOUT THE PATIENT GO HERE.\r"
message_2 +="PID|1|93816095|38427039|81337786|NOBLE^BENJAMIN|FROST|19410513|M|SKIPPY|H|6188 HAWTHORN LN^^MADISON^UT^99767|99767|8324546834|8745990079|ID|UNK|JEW|991143|994736939|S584096999984789||H|MADISON|Y|3|US||US^UNITED STATES OF AMERICA||N||\r"
message_2 +="PV1|1|P|XXPOC^901^0^DATICA HOSPITAL A|A|234570|XXPOC^852^1^DATICA HOSPITAL B|29763487^CANTRELL^JESSICA^F^^NP|35192786^PHELPS^MARIA^G^^CRNA|92980930^LYNN^MARIA^N^^PA|CAR|XXPOC^649^3^DATICA HOSPITAL A|N||8|B6||64295772^BELTRAN^JASON^X^^MD|U|211419|A23|R|N|G|44|20151212|66.14|1|C|B|||||||||||||||\r"
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
Orm_mess +="PID|1|32427285|73121932|83906432|MUELLER^JACOB|CANTRELL|19350401|M|BOOMER|U|8804 HAWTHORN WAY^^MADISON^VT^92901|92901|8732131395|8198276991|SR|T|MSH|237250|934772637|S110431226262678||N|MADISON|Y|5|US||US^UNITED STATES OF AMERICA||N||\r"
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

message_test = "MSH|^~\&|EPIC|EPICADT|SMS|SMSADT|199912271408|CHARRIS|ADT^A04|1817457|D|2.5|\r"
message_test += "PID||0493575^^^2^ID 1|454721||DOE^JOHN^^^^|DOE^JOHN^^^^|19480203|M||B|254 MYSTREET AVE^^MYTOWN^OH^44123^USA||(216)123-4567|||M|NON|400003403~1129086|999-|\r"
message_test += "NK1||ROE^MARIE^^^^|SPO||(216)123-4567||EC|||||||||||||||||||||||||||\r"
message_test += "NK1||DOE^JOHN^^^^|SPO||(216)123-4567||EC|||||||||||||||||||||||||||\r"
message_test += "NK1||DOE^ROBERT^^^^|SPO||(216)123-4568||EC|||||||||||||||||||||||||||\r"
message_test += "PV1||O|168~219~C~PMA^^df^^^^^^^||||277^ALLEN MYLASTNAME^BONNIE^^^^|||||||||| ||2688684|||||||||||||||||||||||||199912271408||||||002376853\r"


async def message_sorting(message):
    with open ('C:/Users/aubre/OneDrive/Desktop/Software Engineering/OpenSourceEngineProject/engine/Resources/FHIRObjects.json') as f:
        data = json.load(f)
    
    dic = {}
    h = message
    #Sorting through message
        #loop through lines in the message
    #print(len(str(h(11)(0))))
    # print(len(str(h(3)(2)).split('^')))

    # print(len(h(1)))
    # print(h(1))
    # print(h(6))
    # print(h(3)(2)(1))
    abc = {}
    # for seg in range (1,len(h)+1):
    #     if (str(h(seg)(0))) in abc:
    #         abc[str(h(seg)(0))] += 1
            
    #     else: abc[str(h(seg)(0))] = 1
    # print(abc)
    for seg in range (1,len(h)+1):
        
        header = ''.join(e for e in str(h(seg)(0)) if e.isalnum())
        
        if (header) in abc:
            abc[header] += 1
        else: abc[header] = 1
        seg_dict={}  
        seg_length = len(h(seg))
        #loop through field in a segment
        for i in range (1,seg_length):            
            rep_length = len(str(h(seg)(i)).split('~'))   
            if rep_length > 1 and not (header == "MSH" and i == 2):           
                temp = {}
                #loop through component in a field
                for j in range(1,rep_length+1):
                    s = str(h(seg)(i)(j))
                    #print(s,header,i,j)
                    comp_length = len(s.split("^")) 
                    if comp_length > 1:
                        comp_dict = {}
                        for v in range (1,comp_length):
                            comp_val = str(h(seg)(i)(j)(v))
                            #print(comp_val,header,i,j)
                            if comp_val:
                                if (type(data[header][header+'.'+str(i)][header+'.'+str(i)+'.'+str(v)])==dict):
                                    comp_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.'+str(v)][header+'.'+str(i)+'.'+str(v)+'.0']] = comp_val
                                else:
                                    comp_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.'+str(v)]] = comp_val
                        seg_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.0']+"["+str(j)+"]"] = comp_dict
                    else:
                        seg_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.0']+"["+str(j)+"]"]= s
            
            elif len(str(h(seg)(i)).split('^')) > 1 and (header!="MSH" or i != 2):           #check if there exist the component 
                temp = {}
                field_length = len(str(h(seg)(i)).split('^'))
                #loop through component in a field
                for j in range(1,field_length+1):
                    s = str(h(seg)(i)(1)(j))  
                    #print(s,header,i,j)
                    if s:      
                        
                        if (type(data[header][header+'.'+str(i)][header+'.'+str(i)+'.'+str(j)])==dict):
                            temp[data[header][header+'.'+str(i)][header+'.'+str(i)+'.'+str(j)][header+'.'+str(i)+'.'+str(j)+'.0']] = s
                        else:
                            temp[data[header][header+'.'+str(i)][header+'.'+str(i)+'.'+str(j)]] = s
                    j += 1  
                seg_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.0']]=temp
            else:                           
                s = str(h(seg)(i))
                #print(s,header,i)
                if s:
                    
                    
                    if (type(data[header][header+'.'+str(i)])== dict):
                        seg_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.0']]=s
                    else:   
                        seg_dict[data[header][header+'.'+str(i)]]=s
                else:
                    
                    if (type(data[header][header+'.'+str(i)])== dict):
                        seg_dict[data[header][header+'.'+str(i)][header+'.'+str(i)+'.0']]='Empty'   
                        
                    else:
                        seg_dict[data[header][header+'.'+str(i)]]='Empty'            
            i +=1
            if (abc[header] > 1):
                dic[data[header][header+'.0']+str([abc[header]])]=seg_dict
                
            else:
                dic[data[header][header+'.0']]=seg_dict
    return dic 

async def output_To_Json(dic):
    directoryPath = "C:/Users/aubre/OneDrive/Desktop/Software Engineering/OpenSourceEngineProject/engine/TestScripts/"
    jsonFile= time.strftime("%d%m%Y%Hh%Mm%S") + ".json"
    fullJSONPath = directoryPath + jsonFile
    with open(fullJSONPath, 'w') as fp:
        json.dump(dic, fp, indent=4)

    url = "http://10.1.144.91:8090/sendFile"
    files = [('document', (fullJSONPath, open(fullJSONPath, 'rb'), 'application/octet')),]
    fp = requests.post(url, files=files)   
    fp.close()

#output_To_Json(message_sorting(Orm_mess))

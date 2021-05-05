##################################################
## This file authorizes the connection to the database
##################################################
## YearMonthDay: 2021-03-07
## Project: Open Source Engine Integration
## Program Name: S12_test.py
## Author: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel
## Copyright: Copyright 2021
## Credits: Bao Mai, Derek Manchee, Aubrey Nickerson, Joseph Egely, Keaton Canuel, Youry Khmelevsky, Benson Ho
## License: MIT License
## Version: 1.0.0
## Maintainer: Okanagan College Team
## Status: In Development
## Revision History:
## Date        Author             Revision      What was changed?
## 03/07/2021  Joseph Egely       1             Created testing for SIU message format.
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
import json

def confirmS12(message):
    mandatory_segments = ["MSH", "SCH", "TQ1", "PID", "PD1", "PV1", "PV2", "OBX", "DG1"]
    found_segments = []
    for segment in message:
        if segment in mandatory_segments:
            if segment not in found_segments:
                found_segments.append(segment)
            else:
                return False
    if len(found_segments) == len(mandatory_segments):
        return confirmFormat(message, mandatory_segments)
    else:
        print("Segment count incorrect")
        return False


def confirmFormat(message, mandatory_segments):
    for segment in message:
        if segment == "MSH":
            if len(message[segment]) < 22:
                print("MSH too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "SCH":
            if len(message[segment]) <= 27:
                print("SCH too short")
                print(len(message[segment]))
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "PID":
            if len(message[segment]) < 40:
                print("PID too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "TQ1":
            if len(message[segment]) < 15:
                print("TQ1 too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "PD1":
            if len(message[segment]) < 22:
                print("PD1 too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "PV1":
            if len(message[segment]) < 53:
                print("PV1 too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "PV2":
            if len(message[segment]) < 50:
                print("PV2 too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "OBX":
            if len(message[segment]) < 26:
                print("OBX too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False

        elif segment == "DG1":
            if len(message[segment]) < 22:
                print("DQ1 too short")
                return False
            for subseg in segment:
                if not subseg.isalnum():
                    for seg in subseg:
                        if not subseg[seg].isalnum():
                            print("Not text or numbers")
                            return False
        return True


with open("Documentation\\Unit Tests\\S12_Test_Resources\\SIU_S12.json") as file:
    message = json.load(file)

with open("Documentation\\Unit Tests\\S12_Test_Resources\\SIU_S12_False.json") as file:
    message_false = json.load(file)


print(confirmS12(message_false))
print(confirmS12(message))

import re, hashlib
from datetime import datetime
from db import db

msgData = db("msgData")
meetData = db("meetData")

class Parser:
    def __init__(self, Whatsapp):
        self.whatsapp = Whatsapp        


    def parseMessage(self, msg):        
        if(((datetime.now() - msg["time"]).seconds)/3600 < 16 and not self.checkIfParsed(msg)):
            print(msg)
            hash = hashlib.md5((msg["msg"] + msg["time"].strftime("%H:%M:%S %d/%m/%Y") + msg["group"] + str(msg["id"])).encode()).hexdigest()            
            id = msgData.insert([(msg["msg"], msg["time"].strftime("%H:%M:%S %d/%m/%Y"), msg["group"], "True", hash)], True)
            myMsg = msg["msg"].split("\n")

            if(self.checkIfStringInMsg("help", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("help"))                

            elif(self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                pass

            elif(self.checkIfStringInMsg("C:", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                for a in myMsg:
                    if "C:" in a:
                        code = a[2:].strip()

                if(code == "save"):
                    meetID, link = self.saveMeet(msg, id, returnID = True)
                    self.whatsapp.sendMessage("Automation", self.buildMsg(code = "autoRegister", msg = msg, id = id, other = meetID, link = link))

                elif(code == "delete"):
                    for i in myMsg:
                        if "ID:" in i:
                            getid = int(i[3:].strip())
                    meetData.delete(getid)
                    self.whatsapp.sendMessage("Automation", self.buildMsg("deleteMeet", msg, getid))
                
                elif(code == "changeTime"):                    
                    for i in myMsg:
                        if "T:" in i:
                            newTime = (datetime.strptime(i[2:].strip()+ msg["time"].strftime(" %d/%m/%Y"), '%H:%M %d/%m/%Y')).strftime("%H:%M:%S %d/%m/%Y")
                        if "ID:" in i:
                            getid = int(i[3:].strip())
                    
                    meetData.updateTime(newTime, getid)
                    meetData.update(getid, state = "False")
                    self.whatsapp.sendMessage("Automation", self.buildMsg("changeTime", msg=newTime , id = getid))
            
            elif(self.checkIfStringInMsg("getAll", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("getAll"))
                

            elif(self.checkIfStringInMsg("meet.google.com", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                meetID, link = self.saveMeet(msg, id, True, True)                
                self.whatsapp.sendMessage("Automation", self.buildMsg(code = "othergrp", msg = msg, id = id, other = meetID, link = link))

            else:                
                pass
    
        
    def buildMsg(self, code, msg="", id="", other="", link = ""):
        if(code == "help"):
            combination1 = "1. Save Meeting<br>  C: save<br>  T: HH:MM<br>  L: abc-defg-hij<br>  S: mySubject"
            combination2 = "2. Change Meeting Time<br>  C: changeTime<br>  ID: 1234<br>  T: HH:MM"
            combination3 = "3. Delete Saved Meeting<br>  C: delete<br>  ID: 1234"
            superCodes = "*The following codes are available for direct use:*<br>1. help<br>2. getAll"
            return "AUTOMATOR<br><br>" + superCodes + "<br><br>*Structured Requests*<br><br>" + combination1 + "<br><br>" + combination2 + "<br><br>" + combination3 + "<br><br>*Abbreviations*<br>C: Code<br>ID: meeting ID<br>T: Time for meeting<br>L: Link of Meeting<br>S: Subject"

        elif(code == "othergrp"):
            return "AUTOMATOR<br><br>*Meet Link Registered*<br><br>ID: " + str(other) + "<br>Time: " + str(msg["time"].strftime("%H:%M:%S %d/%m/%Y")) + "<br>Group: " + str(msg["group"]) + "<br>Subject: "+str(msg["group"])+"<br>Link: " + re.search("(?P<url>https?://[^\s]+)", link).group("url")

        elif(code == "autoRegister"):
            theData = meetData.get("parentID", id)
            return "AUTOMATOR<br><br>*Meet Link Registered*<br><br>ID: " + str(other) + "<br>Time: " + str(theData[0][5]) + "<br>Group: Automation<br>Subject: "+ theData[0][3] +"<br>Link: " + re.search("(?P<url>https?://[^\s]+)", link).group("url")
        
        elif(code=="deleteMeet"):
            return "AUTOMATOR<br><br>*Meet Link Deleted*<br><br>ID: " + str(id)
        
        elif(code=="changeTime"):
            return "AUTOMATOR<br><br>*Time Changed*<br><br>ID: " + str(id) + "<br>New Time: " + str(msg)
        
        elif(code == "getAll"):
            data = meetData.getAll()
            theMsgToReturn = "AUTOMATOR<br><br>*All registered meetings till date*<br><br>"
            for a in data:
                theMsgToReturn = theMsgToReturn + "ID: " + str(a[0]) + "<br>Time: "+a[5]+"<br>Subject: "+a[3]+"<br>Link: "+a[4]+"<br>Processed: "+str(a[1])+"<br><br>"
            return theMsgToReturn
    
    def saveMeet(self, msg, id, notFromAutomation = False, returnID = False):
        if(notFromAutomation):
            link = re.search("(?P<url>https?://[^\s]+)", msg["msg"]).group("url")
            meetTime = msg["time"].strftime("%H:%M:%S %d/%m/%Y")
            subject = msg["group"]
        else:
            myMsg = msg["msg"].split("\n")
            for i in myMsg:
                if "T:" in i:
                    meetTime = (datetime.strptime(i[2:].strip()+ msg["time"].strftime(" %d/%m/%Y"), '%H:%M %d/%m/%Y')).strftime("%H:%M:%S %d/%m/%Y")
                if "L:" in i:
                    link = "https://meet.google.com/" + i[2:].strip()
                if "S:" in i:
                    subject = i[2:].strip()

        data = [(link, meetTime, subject, id, "False")]
        if returnID:
            return meetData.insert(data, True), link
        else:
            meetData.insert(data)


    
    def checkIfParsed(self, msg):        
        hash = hashlib.md5((msg["msg"] + msg["time"].strftime("%H:%M:%S %d/%m/%Y") + msg["group"] + str(msg["id"])).encode()).hexdigest()                
        getMsg1 = msgData.get("hash", hash)        
        if (len(getMsg1) > 0):
            return True
        else:
            return False
    
    def checkIfStringInMsg(self, string, splittedMsg):
        if string in splittedMsg:
            return True
        for i in splittedMsg:
            if string in i:
                return True        
        return False
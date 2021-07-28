import re, hashlib
from datetime import datetime
from typing import final
from db import db, config
from types import SimpleNamespace

msgData = db("msgData")
meetData = db("meetData")
config = config("configData")

class Parser:
    def __init__(self, Whatsapp):
        self.whatsapp = Whatsapp        


    def parseMessage(self, msg, flags):        
        if(((datetime.now() - msg["time"]).seconds)/3600 < 16 and not self.checkIfParsed(msg)):                        
            hash = hashlib.md5((msg["msg"] + msg["time"].strftime("%H:%M:%S %d/%m/%Y") + msg["group"]).encode()).hexdigest()            
            id = msgData.insert([(msg["msg"], msg["time"].strftime("%H:%M:%S %d/%m/%Y"), msg["group"], "True", hash)], True)
            myMsg = msg["msg"].split("\n")

            if(self.checkIfStringInMsg("help", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("help"))                
            
            elif(self.checkIfStringInMsg("status", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("status", other=flags))                
            
            elif(self.checkIfStringInMsg("all", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("getAll"))
            
            elif(self.checkIfStringInMsg("upcoming", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("getUpcoming"))
            
            elif(self.checkIfStringInMsg("showConfig", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsgNew(code = "config", next = False))
              
            elif(self.checkIfStringInMsg("meet.google.com", myMsg) and not self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                meetID, link = self.saveMeet(msg, id, True, True)                
                self.whatsapp.sendMessage("Automation", self.buildMsg(code = "othergrp", msg = msg, id = id, other = meetID, link = link))

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
                
                elif(code == "changeConfig"):
                    for i in myMsg:
                        if "T:" in i:
                            logout_checker_time = int(float(i[2:].strip())*60)
                            config.update("theValue", logout_checker_time, "theField", "logout_checker_time")
                        if "P:" in i:
                            max_participants_before_logout = int(i[3:].strip())
                            config.update("theValue", max_participants_before_logout, "theField", "min_meet_parti")
                    
                    self.whatsapp.sendMessage("Automation", self.buildMsgNew(code = "config", next = True))
            else:                
                pass
    
        

    def buildMsgNew(self, **kwargs):        
        iniStr = "AUTOMATOR<br><br>"         

        if(kwargs["code"] == "config"):            
            lct = int(config.get("theField", "logout_checker_time")[0][2])
            mmp = config.get("theField", "min_meet_parti")[0][2]            
            finalStr = iniStr + "1. Wait time before starting logout checker: " + str(int(lct/60)) + " minutes<br><br>2. No. of Participants below which meet will exit: " + str(mmp) + ("<br><br><br>Note that these are valid from next meetings" if kwargs["next"] == True else "")            
            return finalStr
            


    def buildMsg(self, code, msg="", id="", other="", link = ""):
        if(code == "help"):
            combination1 = "1. Save Meeting<br>  C: save<br>  T: <Time in HH:MM><br>  L: <link as abc-defg-hij format><br>  S: <Subject>"
            combination2 = "2. Change Meeting Time<br>  C: changeTime<br>  ID: <Meeting ID><br>  T: <time in HH:MM>"
            combination3 = "3. Delete Saved Meeting<br>  C: delete<br>  ID: <Meeting ID>"
            combination4 = "4. Update Configurations<br>  C: changeConfig<br>  T: <optional><Logout checker time in minutes><br>  P: <optional><Min Participant no. b4 exiting meet>"

            sc = {
                "help": "get help",
                "all" : "get all meetings",
                "upcoming": "show upcoming meetings",
                "status": "get ongoing meeting status",
                "showConfig": "show meeting configurations"
            }
            superCodes = "*The following codes are available for direct use:*<br><br>"
            i = 1
            for x in sc:
                superCodes = superCodes + str(i) + ". " + x + " - " + sc[x] + "<br>"
                i += 1

            abbreviations = ""
            return "AUTOMATOR<br><br>" + superCodes + "<br><br>*Structured Requests*<br><br>" + combination1 + "<br><br>" + combination2 + "<br><br>" + combination3 + "<br><br>" + combination4 + "<br><br>" + abbreviations

        elif(code == "othergrp"):
            return "AUTOMATOR<br><br>*Meet Link Registered*<br><br>ID: " + str(other) + "<br>Time: " + str(msg["time"].strftime("%H:%M:%S %d/%m/%Y")) + "<br>Group: " + str(msg["group"]) + "<br>Subject: "+str(msg["group"])+"<br>Link: " + re.search("(?P<url>https?://[^\s]+)", link).group("url")

        elif(code == "autoRegister"):
            theData = meetData.get("id", other)            
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
        
        elif(code == "status"):            
            theMsgToReturn = "AUTOMATOR<br><br>*Ongoing Meeting:*<br>"
            if(other["mRunning"]):
                theMsgToReturn = theMsgToReturn + "    ID: " + str(other["mRunning"]) + "<br>    Participants: " + str(other["mParticipants"])
            else:
                theMsgToReturn = theMsgToReturn + "NONE"
            return theMsgToReturn
        
        elif(code == "getUpcoming"):
            data = meetData.get("visited", "False")
            theMsgToReturn = "AUTOMATOR<br><br>*Upcoming meetings*<br><br>"
            for a in data:
                theMsgToReturn = theMsgToReturn + "ID: " + str(a[0]) + "<br>Time: "+a[5]+"<br>Subject: "+a[3]+"<br>Link: "+a[4]+"<br><br>"
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
        exists = meetData.get("link", link)        
        if(len(exists) > 0):            
            meetData.updateTime(meetTime, exists[0][0])
            meetData.updateParent(exists[0][2], id)
            if returnID:
                return exists[0][0], link
        else:
            if returnID:
                return meetData.insert(data, True), link
            else:
                meetData.insert(data)


    
    def checkIfParsed(self, msg):        
        hash = hashlib.md5((msg["msg"] + msg["time"].strftime("%H:%M:%S %d/%m/%Y") + msg["group"]).encode()).hexdigest()                
        getMsg1 = msgData.get("hash", hash)        
        if (len(getMsg1) > 0):
            return True
        else:
            return False
    
    def checkIfStringInMsg(self, string, splittedMsg):
        if(string in splittedMsg or string in splittedMsg):
            return True
        for i in splittedMsg:
            if(string in i or string in i.lower()):
                return True        
        return False
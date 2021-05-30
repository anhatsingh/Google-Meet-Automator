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
            hash = hashlib.md5((msg["msg"] + msg["time"].strftime("%H:%M:%S %d/%m/%Y") + msg["group"] + str(msg["id"])).encode()).hexdigest()
            id = msgData.insert([(msg["msg"], msg["time"].strftime("%H:%M:%S %d/%m/%Y"), msg["group"], "True", hash)], True)
            myMsg = msg["msg"].split("\n")
            if(self.checkIfStringInMsg("help", myMsg)):
                self.whatsapp.sendMessage("Automation", self.buildMsg("help"))                
            elif(self.checkIfStringInMsg("AUTOMATOR", myMsg)):
                pass
            elif(self.checkIfStringInMsg("C:", myMsg)):
                code = myMsg[0][2:].strip().lower()
                if(code == "save"):
                    self.saveMsg(msg, id)
                    self.whatsapp.sendMessage("Automation", self.buildMsg("autoRegister", msg, id))                    
            elif(self.checkIfStringInMsg("meet.google.com", myMsg) and msg["group"] != "Automation"):
                self.saveMsg(msg, id, True)
                self.whatsapp.sendMessage("Automation", self.buildMsg("othergrp", msg, id))
            else:                
                pass

    def buildMsg(self, code, msg="", id=""):
        if(code == "help"):
            return "AUTOMATOR<br><br>C: Code<save><br>T: Time for meeting<br>L: Link of Meeting<br>S: Subject"
        elif(code == "othergrp"):
            return "AUTOMATOR<br><br>*Meet Link Registered*<br><br>ID: " + str(id) + "<br>Time: " + str(msg["time"].strftime("%H:%M:%S %d/%m/%Y")) + "<br>Group: " + str(msg["group"]) + "<br>Subject: "+str(msg["group"])+"<br>Link: " + re.search("(?P<url>https?://[^\s]+)", msg["msg"]).group("url")
        elif(code == "autoRegister"):
            theData = meetData.get("parentID", id)
            return "AUTOMATOR<br><br>*Meet Link Registered*<br><br>ID: " + str(id) + "<br>Time: " + str(theData[0][5]) + "<br>Group: Automation<br>Subject: "+ theData[0][3] +"<br>Link: " + re.search("(?P<url>https?://[^\s]+)", msg["msg"]).group("url")
    
    def saveMsg(self, msg, id, notFromAutomation = False):
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
                    link = i[2:].strip()
                if "S:" in i:
                    subject = i[2:].strip()

        data = [(link, meetTime, subject, id, "False")]
        meetData.insert(data)
    
    def checkIfParsed(self, msg):        
        hash = hashlib.md5((msg["msg"] + msg["time"].strftime("%H:%M:%S %d/%m/%Y") + msg["group"] + str(msg["id"])).encode()).hexdigest()
        print(hash)
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
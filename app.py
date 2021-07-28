import threading, time, traceback, datetime

from seleniumManager.manager import Manager
from whatsappManager.whatsapp import Whatsapp
from googleMeetManager.meet import Meet

from recording_interactions import obsHandler
from msgParser import Parser
import db

# =========================================== Data ===============================================================
db.doOnce()

config = db.config("configData")
waG_db = db.config("wa_groups")

for z in config.get("theField", "username"):
    if(z[2] == ""):
        usr = input("Enter Google Username: ")       
        config.update("theValue", usr, "id", z[0])        

for y in config.get("theField", "password"):
    if(y[2] == ""):
        pss = input("Enter Google Password: ")
        config.update("theValue", pss, "id", y[0])

gUsr = config.get("theField", "username")[0][2]
gPass = config.get("theField", "password")[0][2]

locationToObsShortcut = config.get("theField", "location_to_obs_shortcut")[0][2]
recordMeetings = config.get("theField", "record_meetings")[0][2]
obsSaveLocation = config.get("theField", "video_save_location")[0][2]

# ================================================================================================================

# flags

f = {    
    "im": False,
    "em": False,
    "mRunning": False,
    "mParticipants": 0,
    "dRunning": True,
    "error": False,
    "eMsg": None,
    "eThread": None
    }

def background_Listener():
    print("Background Service Worker Started")
    si = Manager(r'chromedriver.exe')
    d, k  = si.driver(), si.getKeys()
    wa = Whatsapp(d, k)
    p = Parser(wa)    

    wa.start()
    wa.waitForLogin()
    wa.sendMessage("Automation", "AUTOMATOR<br><br>Yipeee! I am alive :P<br>Multi-Threading is enabled :)")

    while(True):
        try:            
            if(f["em"]):
                wa.sendMessage("Automation", "AUTOMATOR<br><br>Meeting Ended: "+ str(f["em"]))
                f["em"] = False
                f["mRunning"] = False
            
            if(f["im"]):
                wa.sendMessage("Automation", "AUTOMATOR<br><br>Meeting Joined: "+ str(f["im"]))
                f["mRunning"] = f["im"]
                f["im"] = False                
            
            if(f["error"]):
                wa.sendMessage("Automation", "AUTOMATOR<br><br>*Error Occurred:* <br>Thread: " + f["eThread"] + "<br>Msg: " + str(f["eMsg"]))
                f["error"] = False
                f["eMsg"] = None
                f["eThread"] = None

            msgs = []
            for x in waG_db.getAll():
                msgs = msgs + wa.getAllMessages(x[1])        
            for i in msgs:
                p.parseMessage(i, f)                

        except Exception as e:            
            error = traceback.format_exc()
            print(error)
            
            f["error"] = True            
            f["eMsg"] = e
            f["eThread"] = "Whatsapp Service Worker"
            #do error handling here later.
            
def meetInitiator():
    print("Meet Listener Started")
    md = db.db("meetData")

    def startMeet(id, link):
        f["im"] = id
        si = Manager(r'chromedriver.exe')
        d, k = si.driver(), si.getKeys()
        m = Meet(link, d, k, gUsr, gPass)
        o = obsHandler(locationToObsShortcut)

        minParti = int(config.get("theField", "min_meet_parti")[0][2])
        waitTime = int(config.get("theField", "logout_checker_time")[0][2])
        
        def stopper():            
            m.autoLogout(waitTime, minParti)            
            f["dRunning"] = False
            o.stop()            
            f["em"] = id

        def tryToJoin():
            if(m.join()):                
                try:     
                    #o.focusOnMeet() 
                    time.sleep(2)      
                    m.micCamOff()                
                    o.openObs()        
                    o.start()
                    o.focusOnMeet()

                except Exception as e:            
                    error = traceback.format_exc()
                    print(error)            
                    f["error"] = True            
                    f["eMsg"] = e
                    f["eThread"] = "Meet Listener"
                    #do error handling here later.

                md.update(id)

                t3 = threading.Thread(target=stopper, args=())
                t3.start()

                while(f["dRunning"]):
                    #meeting is running
                    f["mParticipants"] = m.numberOfParticipants()
                    if(f["mParticipants"] == -1):
                        f["error"] = True            
                        f["eMsg"] = "Error getting number of participants"
                        f["eThread"] = "Meet Listener"
                    time.sleep(10)

                t3.join()

            else:
                f["error"] = True            
                f["eMsg"] = "Unable to Login"
                f["eThread"] = "Meet Listener"
                tryToJoin()

        tryToJoin()
        
            

    while(True):        
        for x in md.get("visited", "False"):
            delta = (datetime.datetime.now() - datetime.datetime.strptime(x[5], '%H:%M:%S %d/%m/%Y')).seconds
            
            if (delta/60 < 15 and delta/60 > -5):                
                startMeet(x[0], x[4])


if __name__ == "__main__":
    t1 = threading.Thread(target=background_Listener, args=())
    t2 = threading.Thread(target=meetInitiator, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()
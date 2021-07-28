import time, yaml, os
if os.path.exists("main.db"):
      os.remove("main.db")

from datetime import datetime, timedelta

from seleniumManager.manager import Manager
from whatsappManager.whatsapp import Whatsapp

from google_interactions import googleHandler
from recording_interactions import obsHandler
from db import db
from msgParser import Parser

# =========================================== Data ===============================================================

with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

googleUser = cfg["google"]["username"]
googlePass = cfg["google"]["password"]

linkToSearchFor = cfg["meet"]["link_to_search_for_in_whatsapp"]
minimumParticipantsBeforeExiting = cfg["meet"]["minimum_participants_before_exiting_meet"]

linksCanBeThisMuchOld = cfg["time"]["time_in_minutes_to_search_for_messages_in_whatsapp"]
timeToWaitBeforeLogoutChecker = cfg["time"]["time_in_seconds_to_wait_before_logout_checker_starts"]

locationToObsShortcut = cfg["obs"]["location_to_obs_shortcut"]
recordMeetings = cfg["obs"]["record_meetings"]
obsSaveLocation = cfg["obs"]["video_save_location"]

myWhatsappGroups = cfg["whatsapp"]["groups_to_search_in"]
# ================================================================================================================

seleniumInstance = Manager(r'chromedriver.exe')
driver, action, keys = seleniumInstance.driver(), seleniumInstance.action(), seleniumInstance.getKeys()
myWhatsapp = Whatsapp(driver, keys)
google = googleHandler(driver, action, keys)    # instantiate Google class
obs = obsHandler(locationToObsShortcut)         # instantiate OBS class
parser = Parser(myWhatsapp)

meetData = db("meetData")

def meet(id, link):
    myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>*ID:* "+str(id) + "<br>*status:* Meeting Joined")
    
    if(recordMeetings):
        time.sleep(4)
        theTime = obs.startOrStopRecording(True)
        date1 = obsSaveLocation + theTime.strftime("%Y-%M-%d_%H-%M-%S.mkv")
        date2 = obsSaveLocation + (theTime + timedelta(seconds=1)).strftime("%Y-%M-%d_%H-%M-%S.mkv")
        date3 = obsSaveLocation + (theTime + timedelta(seconds=-1)).strftime("%Y-%M-%d_%H-%M-%S.mkv")
        if (os.path.isfile(date1) or os.path.isfile(date2) or os.path.isfile(date3)):
            myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>*ID:* "+str(id) + "<br>*status:* Recording Started")
            
    google.joinMeet(link)
    google.changeMeetLayout()
        
    time.sleep(timeToWaitBeforeLogoutChecker)                                   
    google.checkForLogout(minimumParticipantsBeforeExiting)     # start checking for minimum participants to exit the meet
    
    if(recordMeetings):
        obs.startOrStopRecording()
        myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>*ID:* "+str(id) + "<br>*status:* Recording Ended")
    
    meetData.update(id)
    myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>*ID:* "+str(id) + "<br>*status:* Meeting Ended")
    

def crawl(groups):
    msgs = []
    for a in groups:
        msgs = msgs + myWhatsapp.getAllMessages(a)
    return msgs

def parse(msgs):
    for i in msgs:
        parser.parseMessage(i)

def iniMeet():
    data = meetData.get("visited", "False")    
    for a in data:
        delta = (datetime.now() - datetime.strptime(a[5], '%H:%M:%S %d/%m/%Y')).seconds
        if (delta/60 < 10):
            meet(a[0], a[4])


def main():    
    doLogin = google.login(googleUser, googlePass)  # attempt to login to google using username and password
    time.sleep(1)

    if(doLogin):                                    # Login to google successful, proceed ahead.
        myWhatsapp.start()                    # Open whatsapp and wait for QR Code Scan from User
        myWhatsapp.waitForLogin()
        myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>I am alive :D")
        
        if(recordMeetings):
            obs.openObs()            
            obs.focusOnMeet()            
            

        while(True):   
            try:
                msgs = crawl(myWhatsappGroups)
                parse(msgs)
                iniMeet()
            except:
                try:
                    myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>Error Occured")
                except:
                    pass
    else:
        print(str(datetime.now()) + ": Google: login error, unable to login")   # unable to login to google

main()
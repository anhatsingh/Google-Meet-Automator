import time, yaml, re, os
if os.path.exists("main.db"):
      os.remove("main.db")

from datetime import datetime

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
    myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>*Meeting Joined*<br>ID: "+str(id))
    time.sleep(2)
    google.joinMeet(link)       # Join Google Meet with the Link Found                    

    if(recordMeetings):
        obs.startOrStopRecording(1)                        
    #check for logout here                    
    print(str(datetime.now()) + ": Meet: waiting 10 minutes to start logout checker")
    time.sleep(timeToWaitBeforeLogoutChecker)                                   
    google.checkForLogout(minimumParticipantsBeforeExiting)     # start checking for minimum participants to exit the meet
    
    if(recordMeetings):
        obs.startOrStopRecording(0)
    
    meetData.update(id)
    myWhatsapp.sendMessage("Automation", "AUTOMATOR<br><br>*Meeting Ended*<br>ID: "+str(id))
    

def crawl(groups):
    msgs = []
    for a in groups:
        msgs = msgs + myWhatsapp.getAllMessages(a)
    
    for i in msgs:
        parser.parseMessage(i)

    data = meetData.get("visited", "False")    
    for a in data:
        delta = (datetime.now() - datetime.strptime(a[5], '%H:%M:%S %d/%m/%Y')).seconds
        if (delta/60 < 10):
            meet(a[0], a[4])

def main():    
    doLogin = google.login(googleUser, googlePass)  # attempt to login to google using username and password

    if(doLogin):                                    # Login to google successful, proceed ahead.
        myWhatsapp.start()                    # Open whatsapp and wait for QR Code Scan from User
        myWhatsapp.waitForLogin()
        
        if(recordMeetings):
            obs.openObs()
            time.sleep(4)
            print(str(datetime.now()) + ": OBS: obs opened, going back to Whatsapp")
            obs.focusOn("Whatsapp")            
            

        while(True):                                # Keep Searching for new Links on Whatsapp
            crawl(myWhatsappGroups)   
            time.sleep(60)         
    else:
        print(str(datetime.now()) + ": Google: login error, unable to login")   # unable to login to google


main()
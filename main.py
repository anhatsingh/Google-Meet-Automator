import time
import yaml
from datetime import datetime
from init_selenium import seleniumControl
from whatsapp_interactions import whatsappHandler
from google_interactions import googleHandler
from recording_interactions import obsHandler
import introduction
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

linksSearched = []

driver,action,keys = seleniumControl.igniteSelenium(1)   # instantiate selenium instance
google = googleHandler(driver, action, keys)    # instantiate Google class
messenger = whatsappHandler(driver, action)     # instantiate Whatsapp class
obs = obsHandler(locationToObsShortcut)         # instantiate OBS class

doLogin = google.login(googleUser, googlePass)  # attempt to login to google using username and password

if(doLogin):                                    # Login to google successful, proceed ahead.
    messenger.openWhatsapp()                    # Open whatsapp and wait for QR Code Scan from User
    
    if(recordMeetings):
        obs.openObs()
        time.sleep(4)
        print(str(datetime.now()) + ": OBS: obs opened, going back to Whatsapp")
        obs.focusOn("Whatsapp")
    
    messenger.checkIfloggedIn()

    while(True):                                # Keep Searching for new Links on Whatsapp
        getAllWhatsappLinks = messenger.getLinksFromMultipleChats(myWhatsappGroups, linkToSearchFor, linksCanBeThisMuchOld)        #get a list of all new links from whatsapp
        
        if(len(getAllWhatsappLinks) > 0):       #check whther the list of links has any new links
            for eachLink in getAllWhatsappLinks:    #go Through each link of the list
                count = 0                           
                for i in linksSearched:             # check if we have already visited the link
                    if(eachLink == i):
                        count += 1                    
            
                if(count == 0):                     #  if we have not visited the link, proceed ahead
                    print(str(datetime.now()) + ": Whatsapp: a new link found: " + eachLink.get_attribute("href"))

                    google.joinMeet(eachLink)       # Join Google Meet with the Link Found
                    linksSearched.append(eachLink)  # Add the link to the List of Links visited

                    if(recordMeetings):
                        obs.startOrStopRecording(1)                        

                    #check for logout here                    
                    print(str(datetime.now()) + ": Meet: waiting 10 minutes to start logout checker")
                    time.sleep(timeToWaitBeforeLogoutChecker)                                   
                    google.checkForLogout(minimumParticipantsBeforeExiting, obs, recordMeetings)     # start checking for minimum participants to exit the meet
                else:
                    print(str(datetime.now()) + ": Whatsapp: no new links found") # links found are already visited
        else:
            print(str(datetime.now()) + ": Whatsapp: no new links found")   # no new links found in whatsapp
else:
    print(str(datetime.now()) + ": Google: login error, unable to login")   # unable to login to google
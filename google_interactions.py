import time
from datetime import datetime
class googleHandler:

    def __init__(self, driver, action, keys):
        self.driver = driver
        self.action = action
        self.keys = keys

    def login(self, username, passwd):
        print(str(datetime.now()) + ": Google: initiating login")
        try:            
            self.driver.get(r'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%3Fhs%3D193&_ga=2.2277811.2089757821.1617366170-1054544264.1617366170&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
            self.driver.implicitly_wait(15)

            
            loginBox = self.driver.find_element_by_xpath('//*[@id ="identifierId"]')
            loginBox.send_keys(username)
            print(str(datetime.now()) + ": Google: username ********** filled")
            
            nextButton = self.driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
            nextButton[0].click()
                    
            passWordBox = self.driver.find_element_by_xpath(
                '//*[@id ="password"]/div[1]/div / div[1]/input')
            passWordBox.send_keys(passwd)
            print(str(datetime.now()) + ": Google: password ********** filled")
        
            nextButton = self.driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
            nextButton[0].click()

            print(str(datetime.now()) + ": Google: login successful")
            return 1            
        except:
            print(str(datetime.now()) + ": Google: login failed")
            return 0


    def joinMeet(self, possibleLink):
        print(str(datetime.now()) + ": Meet: initiating meeting")

        possibleLink.click()
        window_after = self.driver.window_handles[1]
        self.driver.switch_to_window(window_after)
        self.driver.implicitly_wait(100)

            
        self.driver.find_element_by_css_selector('body').send_keys(self.keys.CONTROL + 'd')
        print(str(datetime.now()) + ": Meet: mic turned off")
        self.driver.find_element_by_css_selector('body').send_keys(self.keys.CONTROL + 'e')
        print(str(datetime.now()) + ": Meet: camera turned off")

        #time.sleep(5)
        print(str(datetime.now()) + ": Meet: joining now")
        self.driver.find_element_by_css_selector('div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()        
        print(str(datetime.now()) + ": Meet: waiting to join")

        waitingToJoin = 1
        while(waitingToJoin):
            try:                
                if(self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e')):
                    waitingToJoin = 0
                    print(str(datetime.now()) + ": Meet: joining successful")
            except:
                print(str(datetime.now()) + ": Meet: waiting to join")



    def checkForLogout(self, minParticipants, obs, wantToRecord):
        count = 0
        try:
            print(str(datetime.now()) + ": Meet: logout checker initiated")
            time.sleep(20)
            numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text
            print(str(datetime.now()) + ": Meet: number of participants are " + numOfParticipants)

            while(int(numOfParticipants) >= minParticipants):            
                numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text
                print(str(datetime.now()) + ": Meet: number of participants are " + numOfParticipants)
                time.sleep(5)
            
            print(str(datetime.now()) + ": Meet: participants (" + numOfParticipants + ") less than the minimum required to attend meet (" + str(minParticipants) + ")")

            if(wantToRecord):
                obs.startOrStopRecording(0)
            print(str(datetime.now()) + ": Meet: exiting meeting")
            self.driver.close()        

            window_after = self.driver.window_handles[0]
            self.driver.switch_to_window(window_after)
            time.sleep(2)

            print(str(datetime.now()) + ": Meet: exit successful")
            print(str(datetime.now()) + ": Whatsapp: reinitiating link checker")

        except:
            print(str(datetime.now()) + ": Meet: error finding number of participants (" + str(count) + ")")
            count += 1
            time.sleep(5)
            if(count <= 20):
                print(str(datetime.now()) + ": Meet: reinitiating logout checker")
                self.checkForLogout(minParticipants, obs, wantToRecord)
            else:
                print(str(datetime.now()) + ": Meet: unable to initiate logout checker, contact dev")
            
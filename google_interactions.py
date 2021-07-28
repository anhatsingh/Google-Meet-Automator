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


    def joinMeet(self, link):
        self.driver.execute_script('window.open("'+link+'","_blank");')   
        self.driver.implicitly_wait(100)
        time.sleep(3)
        self.driver.switch_to_window(self.driver.window_handles[1])     
        time.sleep(1)

            
        buttons = self.driver.find_elements_by_css_selector('.U26fgb.JRY2Pb.mUbCce.kpROve.uJNmj.QmxbVb.HNeRed.M9Bg4d')
        buttons[0].click()
        buttons[1].click()

        #time.sleep(5)        
        self.driver.find_element_by_css_selector('div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()        
        print(str(datetime.now()) + ": Meet: waiting to join")

        waitingToJoin = 1
        while(waitingToJoin):
            try:                
                if(self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e')):
                    waitingToJoin = 0
                    time.sleep(2)                    
                    print(str(datetime.now()) + ": Meet: joining successful")
            except:
                print(str(datetime.now()) + ": Meet: waiting to join")

    def changeMeetLayout(self):
        self.driver.find_element_by_css_selector('.U26fgb.c7fp5b.FS4hgd.nByyte').click()
        self.driver.find_elements_by_css_selector('.z80M1')[1].click()        
        self.driver.find_elements_by_css_selector('.E5wxQe')[3].click()                

    def checkForLogout(self, minParticipants):
        count = 0
        try:
            numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text            
            while(int(numOfParticipants) >= minParticipants):            
                numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text                
                time.sleep(5)
                        
            self.driver.close()
            time.sleep(2)
            self.driver.switch_to_window(self.driver.window_handles[0])            

        except:
            count += 1
            time.sleep(5)
            if(count <= 20):
                self.checkForLogout(minParticipants)
            else:
                print(str(datetime.now()) + ": Meet: unable to initiate logout checker, contact dev")
            
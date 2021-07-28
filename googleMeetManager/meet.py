import time, urllib, traceback

def localLogger(msg):
    print(msg)

class Meet:

    def __init__(self, meetLink, driver, keys, username, passwd, logger = ""):
        if(logger == ""):
            #self.log = localLogger
            pass
        else:
            #self.log = logger
            pass
        
        self.driver = driver
        self.keys = keys
        self.link = meetLink
        self.username = username
        self.passwd = passwd
            
    def join(self, newTab = False):  
        c = 0      
        try:
            #self.log.write("Signing in to Google")        
            redirect_url = urllib.parse.quote(self.link, safe='')
            loginLink = r'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue='+ redirect_url+'&_ga=2.2277811.2089757821.1617366170-1054544264.1617366170&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
            
            if(newTab):
                self.driver.execute_script('window.open("' + loginLink + '","_blank");')               
                self.driver.implicitly_wait(100)
                time.sleep(2)
                self.driver.switch_to_window(self.driver.window_handles[1])     
            else:
                self.driver.get(loginLink)        
                self.driver.implicitly_wait(15)
            
            loginBox = self.driver.find_element_by_xpath('//*[@id ="identifierId"]')
            loginBox.send_keys(self.username)            
            
            nextButton = self.driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
            nextButton[0].click()
                    
            passWordBox = self.driver.find_element_by_xpath('//*[@id ="password"]/div[1]/div / div[1]/input')
            passWordBox.send_keys(self.passwd)            
        
            nextButton = self.driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
            nextButton[0].click()

            self.driver.implicitly_wait(15)
            #self.log.write("Signed in")

            return True            

        except Exception as e:
            #self.log("Error Occured, check logs")
            error = traceback.format_exc()
            #do error handling here later.

            #self.log.write("Failed")
            if(c<=20):
                c += 1
                self.join(newTab)                
            else:
                return False
    
    def micCamOff(self):
        try:    
            buttons = self.driver.find_elements_by_css_selector('.U26fgb.JRY2Pb.mUbCce.kpROve.uJNmj.QmxbVb.HNeRed.M9Bg4d')
            buttons[0].click()
            buttons[1].click()

            #time.sleep(5)        
            self.driver.find_element_by_css_selector('div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()                

            waitingToJoin = 1
            while(waitingToJoin):
                try:                
                    if(self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e')):
                        waitingToJoin = 0
                        #self.log.write("Meeting Joined")
                        time.sleep(2)                                        
                except:
                    pass
        except Exception as e:
            #self.log("Error Occured, check logs")
            error = traceback.format_exc()
            #do error handling here later.

            self.micCamOff()
    
    def logout(self):
        self.driver.close()        
        #self.log.write("Meeting Left")
    
    def getParticipants(self):
        try:
            #self.log.write("Getting Participants from meeting")
            time.sleep(2)
            
            self.driver.find_element_by_css_selector(".uArJ5e.UQuaGc.kCyAyd.QU4Gid.foXzLb.IeuGXd.M9Bg4d").click() #open Participants List
            time.sleep(2)
            participants = self.driver.find_elements_by_class_name("ZjFb7c")

            theList = []        
            for i in participants:
                theList.append(i.get_attribute("innerText"))

            self.driver.find_element_by_css_selector(".VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.IWtuld.wBYOYb").click() #close button
            return theList
        
        except Exception as e:
            #self.log("Error Occured, check logs")
            error = traceback.format_exc()
            #do error handling here later.

            return self.getParticipants()

    def changeLayout(self, layout = 3):
        self.driver.find_element_by_css_selector('.U26fgb.c7fp5b.FS4hgd.nByyte').click()
        self.driver.find_elements_by_css_selector('.z80M1')[1].click()        
        self.driver.find_elements_by_css_selector('.E5wxQe')[layout].click()                

    def waitForParti(self, waitTime, maxParticipants = 15):
        time.sleep(waitTime)        
        try:
            numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text            
            while(int(numOfParticipants) >= maxParticipants):            
                numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text                
                time.sleep(5)
                        
            return True
            
        except Exception as e:
            #self.log("Error Occured, check logs")
            error = traceback.format_exc()
            #do error handling here later.

            self.waitForParti(maxParticipants)

    def autoLogout(self, waitTime, maxParticipants):
        if(self.waitForParti(waitTime, maxParticipants)):
            self.driver.close()

            
    def sendMsg(self, msg):
        self.driver.find_element_by_css_selector(".uArJ5e.UQuaGc.kCyAyd.QU4Gid.foXzLb.M9Bg4d").click() #open msgbar
        time.sleep(2)
        textArea = self.driver.find_element_by_css_selector(".KHxj8b.tL9Q4c")

        msg = msg.split("<br>")        
        for i in msg:
            textArea.send_keys(i)
            textArea.send_keys(self.keys.SHIFT + self.keys.ENTER)
        
        self.driver.find_element_by_css_selector(".uArJ5e.Y5FYJe.cjq2Db.IOMpW.Cs0vCd.M9Bg4d").click() #send button
        time.sleep(1)
        self.driver.find_element_by_css_selector(".VfPpkd-Bz112c-LgbsSe.yHy1rc.eT1oJ.IWtuld.wBYOYb").click() #close button

    def numberOfParticipants(self):        
        try:
            numOfParticipants = self.driver.find_element_by_css_selector('span.wnPUne.N0PJ8e').text
            return int(numOfParticipants)
        
        except Exception as e:
            #self.log("Error Occured, check logs")
            error = traceback.format_exc()
            #do error handling here later.
            return -1        
import time, re, traceback
from datetime import datetime
from seleniumManager.LocalStorage import LocalStorage as ls

class Whatsapp:
    def __init__(self, driver, keys):
        self.driver = driver
        self.storage = ls(driver)
        self.keys = keys

    def start(self):
        self.driver.get('https://web.whatsapp.com')
        self.driver.implicitly_wait(100)

    def loggedin(self):        
        if self.storage.get("Z0Gmg72LLOEpnd2wuGqKcw==") != None:
            return True
        else:
            return False

    def waitForLogin(self):        
        #if(self.loggedin() == False):
            #print("Whatsapp not Logged in")

        while(self.loggedin() == False):            
            time.sleep(2)
        print("Whatsapp Logged in")
        self.driver.implicitly_wait(100)

    def getAllNames(self, returnElements = True):        
        try:
            elements = self.driver.find_elements_by_class_name("_3-8er")
            listOfPeople = []
            for i in elements:
                listOfPeople.append(i.get_attribute("title"))
            if(returnElements):
                return elements
            else:
                return listOfPeople
        
        except Exception as e:            
            error = traceback.format_exc()
            print(error)
            #do error handling here later.
    
    def getName(self, name, returnElement = True):        
        elements = self.getAllNames()
        for i in elements:
            if(i.get_attribute("title") == name):
                if(returnElement):
                    return i
                else:
                    return i.get_attribute("title")            
        return None

    def openConvo(self, name, sleep = 5):
        nameElement = self.getName(name)
        parent = nameElement.find_element_by_xpath("./ancestor::div[contains(concat(' ', @class, ' '), ' _2aBzC ')][1]")
        parent.click()
        time.sleep(sleep)
    
    def getAllMessages(self, name):
        time.sleep(1)
        self.openConvo(name)        
        parent = self.driver.find_elements_by_class_name("_3ExzF")

        self.driver.implicitly_wait(10)
        messages = []
        a = 1        
        for i in parent:        
            try:
                message = i.find_element_by_xpath("./span/span").text
                theTime = i.find_element_by_xpath('..').get_attribute("data-pre-plain-text")
                
                theTime = re.findall(r'\[.*?\]', theTime)
                theTime = datetime.strptime(theTime[0], '[%I:%M %p, %m/%d/%Y]')

                eachMsg = {
                    "id": a,
                    "msg": message,
                    "time": theTime,
                    "group": name
                }
                messages.append(eachMsg)
                a+=1
            except Exception as e:            
                error = traceback.format_exc()
                print(error)
            #do error handling here later.

        return messages
        
    def sendMessage(self, name, msg):
        time.sleep(1)
        self.openConvo(name)
        textarea = self.driver.find_elements_by_class_name("_2_1wd")[-1]

        msg = msg.split("<br>")        
        for i in msg:
            textarea.send_keys(i)
            textarea.send_keys(self.keys.SHIFT + self.keys.ENTER)

        self.driver.implicitly_wait(100)
        time.sleep(1)        
        sendButton = self.driver.find_element_by_class_name("_1E0Oz")        
        sendButton.click()
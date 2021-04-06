import time
import re
from datetime import datetime
class whatsappHandler:

    def __init__(self, driver, action):
        self.driver = driver        
        self.action = action

    def openWhatsapp(self):
        print(str(datetime.now()) + ": Whatsapp: starting whatsapp")

        self.driver.get('https://web.whatsapp.com')
        self.driver.implicitly_wait(10)        
        
    def checkIfloggedIn(self):
        print(str(datetime.now()) + ": Whatsapp: waiting to scan QR code")
        checkIfLoggedIn = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div').get_attribute("class")

        while(checkIfLoggedIn == "landing-wrapper"):
            try:            
                checkIfLoggedIn = self.driver.find_element_by_xpath('//*[@id="app"]/div[1]/div').get_attribute("class")
                print(str(datetime.now()) + ": Whatsapp: waiting to scan QR code")
                time.sleep(2)
            except:
                break

        print(str(datetime.now()) + ": Whatsapp: QR code accepted, logging in")
        
    def searchInWhatsapp(self, title, linkToSearchFor, timeInMinutesToCheckMessageFor):
        try:
            print(str(datetime.now()) + ": Whatsapp: searching in the group '" + title + "'")
            content = self.driver.find_element_by_css_selector('[title="' + title + '"]')
            parent1 = content.find_element_by_xpath('./../../../../..')

            parent1.click()
            time.sleep(7)

            allSuitableLinks = self.driver.find_elements_by_partial_link_text(linkToSearchFor)

            if(len(allSuitableLinks) > 0):
                theTime = allSuitableLinks[-1].find_element_by_xpath('./../../../..').get_attribute("data-pre-plain-text")
                theTime = re.findall(r'\[.*?\]', theTime)
                date_diff = datetime.now() - datetime.strptime(theTime[0], '[%I:%M %p, %d/%m/%Y]')
                
                if(date_diff.seconds/60 <= timeInMinutesToCheckMessageFor):
                    return allSuitableLinks
                else:
                    return 0
            else:
                return 0
        except:
            print(str(datetime.now()) + ": Whatsapp: Error occured while searching for links through the group: '" + title + "'; is the group archived?")
            return 0


    def getLinksFromMultipleChats(self, listOfGroupsToCheck, linkToSearchFor, timeToSearchForLink):
        print(str(datetime.now()) + ": Whatsapp: collecting all links")
        listOfLinks = []

        for eachGroup in listOfGroupsToCheck:
            getLink = self.searchInWhatsapp(eachGroup, linkToSearchFor, timeToSearchForLink)
            if(getLink):
                listOfLinks.append(getLink[-1])

        return listOfLinks
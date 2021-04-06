from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from datetime import datetime

class seleniumControl:
    def __init__(self, instanceNumber):
        self.instanceNumber = instanceNumber

    def igniteSelenium(self):
        print(str(datetime.now()) + ": Selenium: initiating selenium library")
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block

        print(str(datetime.now()) + ": Selenium: setting chrome preferences")
        opt.add_experimental_option("prefs", { \
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0, 
            "profile.default_content_setting_values.notifications": 1,            
        })
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        #driver = webdriver.Chrome(chrome_options=opt, executable_path=r'C:\Utility\BrowserDrivers\chromedriver.exe')
        print(str(datetime.now()) + ": Selenium: starting chrome browser")
        driver = webdriver.Chrome(chrome_options = opt, executable_path=r'chromedriver.exe')
        action = ActionChains(driver)

        print(str(datetime.now()) + ": Selenium: selenium started successfully")
        return(driver,action, Keys)
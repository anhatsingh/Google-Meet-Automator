from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options
from datetime import datetime

class Manager:
    def __init__(self, driverLocation):
        self.loc = driverLocation
        self.dri = ""
        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        # Pass the argument 1 to allow and 2 to block
        
        opt.add_experimental_option("prefs", { \
            "profile.default_content_setting_values.media_stream_mic": 1, 
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0, 
            "profile.default_content_setting_values.notifications": 1,            
        })
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.myOptions = opt


    def driver(self):        
        self.dri = webdriver.Chrome(chrome_options = self.myOptions, executable_path=self.loc)
        return self.dri

    def action(self):
        if self.dri != "":
            return ActionChains(self.dri)
        else:
            return False
    
    def getKeys(self):
        return Keys
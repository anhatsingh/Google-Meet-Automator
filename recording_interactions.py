import os
import pygetwindow as gw
import pyautogui
import time
from datetime import datetime


class obsHandler:

    def __init__(self, locationToObsShortcut):
        self.location = locationToObsShortcut
    
    def focusOnObs(self):
        time.sleep(5)
        obsWindow = gw.getWindowsWithTitle('OBS')[0]
        pyautogui.hotkey('win', '5')
        obsWindow.resizeTo(1095, 794)
        obsWindow.moveTo(0,0)            
        time.sleep(2)
    
    def focusOnMeet(self):        
        pyautogui.hotkey('win', '8')        

    def openObs(self):        
        #os.startfile(self.location)
        pyautogui.hotkey('win', '5')
        time.sleep(3)
        self.focusOnMeet()
    
    def startOrStopRecording(self, returnName=False):        
        self.focusOnObs()            
        pyautogui.click(1050, 620)        
        if(returnName):
            return datetime.now()        
    
    def start(self, returnName = False):
        if returnName: 
            return self.startOrStopRecording(returnName)
        else:
            self.startOrStopRecording(returnName)
    
    def stop(self, returnName = False):
        if returnName: 
            return self.startOrStopRecording(returnName)
        else:
            self.startOrStopRecording(returnName)
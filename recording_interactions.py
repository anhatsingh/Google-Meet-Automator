import os
import pygetwindow as gw
import pyautogui
import time
from datetime import datetime

class obsHandler:

    def __init__(self, locationToObsShortcut):
        self.location = locationToObsShortcut
    
    def focusOnObs(self):        
        obsWindow = gw.getWindowsWithTitle('OBS')[0]         
        #obsWindow.maximize()
        obsWindow.activate()
        obsWindow.resizeTo(1095, 794)
        obsWindow.moveTo(0,0)            
    
    def focusOn(self, keyword):
        meetWindow = gw.getWindowsWithTitle(keyword)[0]        
        meetWindow.activate()
        meetWindow.maximize()

    def openObs(self):
        print(str(datetime.now()) + ": OBS: starting obs")
        os.startfile(self.location)
        #se_ret = shell.ShellExecuteEx(fMask=0x140, lpFile=r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OBS Studio\\OBS Studio (64bit).lnk", nShow=1)
        #win32event.WaitForSingleObject(se_ret['hProcess'], -1)            
    
    def startOrStopRecording(self, state):
        if(state):
            print(str(datetime.now()) + ": OBS: getting obs")
            self.focusOnObs()
            time.sleep(5)
            pyautogui.click(1050, 620)            
            print(str(datetime.now()) + ": OBS: recording started")
            time.sleep(1)           
            print(str(datetime.now()) + ": OBS: going back to meet")
            self.focusOn("Meet")
        
        if(not state):
            print(str(datetime.now()) + ": OBS: getting obs")
            self.focusOnObs()
            time.sleep(5)
            pyautogui.click(1050, 620)
            print(str(datetime.now()) + ": OBS: recording stopped")
            print(str(datetime.now()) + ": OBS: going back to whatsapp")
            self.focusOn("Whatsapp")
        
        

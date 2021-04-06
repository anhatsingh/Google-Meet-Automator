from datetime import datetime
theTime = ['[5:47 PM, 2/04/2021]']
date_time_obj = datetime.now() - datetime.strptime(theTime[0], '[%I:%M %p, %d/%m/%Y]')
print(date_time_obj.seconds/60)
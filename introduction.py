import yaml


with open("config.yml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

linkToSearchFor = cfg["meet"]["link_to_search_for_in_whatsapp"]
minimumParticipantsBeforeExiting = cfg["meet"]["minimum_participants_before_exiting_meet"]

linksCanBeThisMuchOld = cfg["time"]["time_in_minutes_to_search_for_messages_in_whatsapp"]
timeToWaitBeforeLogoutChecker = cfg["time"]["time_in_seconds_to_wait_before_logout_checker_starts"]

locationToObsShortcut = cfg["obs"]["location_to_obs_shortcut"]
recordMeetings = cfg["obs"]["record_meetings"]

myWhatsappGroups = cfg["whatsapp"]["groups_to_search_in"]

print("==================================================== Meet Auto-Joiner v1.0 ====================================================")
print("Created by: Anhat Singh")
print("Last build Date: 06-04-2021")
print("Build Number: 1.150.2")
print(" ")
print("Configurations:")
print("\tGmail:")
print("\t\tGmail Username: *********")
print("\t\tGmail Password: *********")
print("\tMeet:")
print("\t\tLink to Search For: " + linkToSearchFor)
print("\t\tMin Participants allowed in class: " + str(minimumParticipantsBeforeExiting))
print("\tOBS:")
print("\t\tIs Recording: " + str(recordMeetings))
if(recordMeetings): print("\t\tOBS Shortcut Link: " + locationToObsShortcut)
print("\tWhatsapp:")
print("\t\tTime before a link is considered expired: " + str(linksCanBeThisMuchOld) + " minutes")
print("\t\tGroups to Look for Links: ")
for i in myWhatsappGroups:
    print("\t\t ---- " + i)
print("===============================================================================================================================")

from time import time
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error, requests
import ssl
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import pytz
import json

print("\n{}\n".format('Family Guy')+"*"*50)  #name


#with ssl verification:
def soup_recipe(url): #return soup
    #ssl certificate
    ctx=ssl.create_default_context()
    ctx.check_hostname=False
    ctx.verify_mode=ssl.CERT_NONE

    # #without ssl verification:
    # fhand=urllib.request.urlopen(url).decode()
    # soup=BeautifulSoup(fhand,'html.parser') #soup object

    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup=BeautifulSoup(webpage,'html.parser') #soup_object
    return soup
    
#converting timezones
def EDTtoNPT(timestamp): #return Nepal Time stamp
    EDT_timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

    new_timezone = pytz.timezone("Asia/Kathmandu")
    old_timezone = pytz.timezone("America/New_York")

    NPT_timestamp = (old_timezone.localize(EDT_timestamp).astimezone(new_timezone))
    # NPT_timestamp = datetime.strptime(NPT_timestamp,'%Y %B %d || %H:%M:%S')

    # NPT_timestamp = datetime.strptime(NPT_timestamp,'%Y-%m-%d %H:%M:%S')
    return (NPT_timestamp)

def formatTimeStamp(oldTimeStamp):    
     NPT_timestamp_formatted=(oldTimeStamp.strftime("%Y %b %d || %H:%M:%S"))
     return(NPT_timestamp_formatted)


url="https://yourcountdown.to/family-guy"
soup=soup_recipe(url)

#write in file
# with open ('/home/saimon_ghimire010/sAIMON/toBeAdded/Work/familyGuy/main.html',"w+") as newfile:
#     for lines in soup:
#         newfile.write(str(lines))

#timestamps
div = soup.find("div", {"class": "countdown"})
data_date = (div['data-date']) #timestamp 2022-05-01 21:30:00 NY
NPT_timestamp=EDTtoNPT(data_date)
NPT_timestamp_formatted=formatTimeStamp(NPT_timestamp)
#INFO#
##########################################################################################################
###########################################################################################
#######################################################################
###################################################
###################################


div = soup.find("h2", {"class": "subtitle"})
keywords=(div.contents[0]).split()
infoURL="https://www.rottentomatoes.com/tv/family_guy/s"+keywords[1]+"/e"+keywords[3]
prevEpInfoURL="https://www.rottentomatoes.com/tv/family_guy/s"+keywords[1]+"/e"+str(int(keywords[3])-1)
def info(infoURL,rank):
    soup= soup_recipe(infoURL)
    div = soup.find("script", {"type": "application/ld+json"})
    jsonLine=div.contents[0]
    dict=json.loads(jsonLine)
    try:
        name=dict['name']
        description=dict['description']
    except:
        name='Not confirmed'
        description=dict['description']

    if (rank=="Previous "):
        printPart(rank,name,description)
    else:
        printPart(rank,name,NPT_timestamp_formatted,NPT_timestamp,description)

def printPart(*args):
    try:
        print("\n"+"*"*100)
        #LATEST
        NPT_timestamp=args[3]
        now=datetime.now()
        now=now.replace(tzinfo=timezone.utc)
        if (now>NPT_timestamp):
            print("\n{} episode:\nTitle: {}\nTime: {} (GO WATCH IT)\n{}".format(args[0],args[1],args[2],args[4]))
        else:
            # currentTime=f"{datetime.datetime.now():%Y %B %d || %H:%M:%S}"
            print("\n{} episode:\nTitle: {}\nTime: {}  (Current time:: {})\n{}".format(args[0],args[1],args[2],now.strftime('%Y %B %d || %H:%M:%S'),args[4]))
        
    except:
        #PREVIOUS
        print("\n{} episode:\nTitle: {}\n{}".format(args[0],args[1],args[2]))


        
info(prevEpInfoURL,'Previous ')
info(infoURL,'Latest ')

#this is the change done

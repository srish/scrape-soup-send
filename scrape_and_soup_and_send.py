# #!/usr/bin/env python
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
from bs4 import BeautifulSoup
from datetime import datetime
from twilio.rest import Client
import schedule
import time

#Twilio credentials..obtain from https://www.twilio.com/console
twilio_account_sid = 'enter_account_sid'
twilio_auth_token = 'enter_auth_token'
twilio_from_num = 'from_number'
twilio_to_num = 'to_number'

#visa appointment details 
targeturl = 'enter_the_url_here'
i_am_going_to_Barcelona_on = "Day MM dd YYYY"

def scrapeSelectedDate(url): 
	browser = webdriver.Firefox(executable_path=r'/path_to_geckodriver')
	browser.get(url)   
	time.sleep(50)  #50 is too much..but the page I'm trying to scrape loads quite slow
	html_source = browser.page_source  
	soup = BeautifulSoup(html_source,'html.parser') 

	#For debugging purpose only
	# with open("Output.html", "w") as text_file:
	# 	text_file.write(str(soup))

	date = soup.find(id="idDivBktDatetimeSelectedDate").text
	browser.quit()
	return date

def sendMsg(diff, date, msg):
	client = Client(twilio_account_sid, twilio_auth_token)
	client.messages.create(from_=twilio_from_num, 
		to=twilio_to_num, 
		body=msg)

def checkIfThereIsAnAvailability():
    date = scrapeSelectedDate(targeturl)
    firstAptAvail = datetime.strptime(date, '%A %B %d %Y')
    iAmGoingOn = datetime.strptime(i_am_going_to_Barcelona_on, '%A %b %d %Y')
    diff = (iAmGoingOn - firstAptAvail).days
    if diff > 20:
		message = "There is a visa appointment available on " + str(date) + ", " + str(diff) + " days before your trip to Barcelona. " 
		sendMsg(diff, date, msg)

schedule.every(30).minutes.do(checkIfThereIsAnAvailability)

while True:
    schedule.run_pending()
    time.sleep(1)
#!/usr/bin/env python
"""
    Scrapes the appointment page of a visa website and
    notifies of an early availability than the usual booking!

    MIT license

    :author: Srishti Sethi <ssethi@wikimedia.org>
"""

import time
import schedule
from selenium import webdriver
from bs4 import BeautifulSoup
from twilio.rest import Client

# Twilio credentials..obtain from https://www.twilio.com/console
TWILIO_ACCOUNT_SID = 'enter_account_sid'
TWILIO_AUTH_TOKEN = 'enter_auth_token'
TWILIO_FROM_NUM = 'from_number'
TWILIO_TO_NUM = 'to_number'

# visa appointment details
TARGET_URL = 'enter_the_url_here'
I_AM_GOING_TO_BARCELONA_ON = "Day MM dd YYYY"


def scrape_selected_date(url):
    """ Scrapes the appointment date on the appointment page
    """
    browser = webdriver.Firefox(executable_path=r'/path_to_geckodriver')
    browser.get(url)
    # 50 is too much..but the page I'm trying to scrape loads quite slow
    time.sleep(50)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    date = soup.find(id="idDivBktDatetimeSelectedDate").text
    browser.quit()
    return date


def send_msg(msg):
    """ Sends message via Twilio
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    client.messages.create(from_=TWILIO_FROM_NUM, to=TWILIO_TO_NUM, body=msg)


def check_for_availability():
    """ Check if there is an availability few weeks prior to the travel
    """
    date = scrape_selected_date(TARGET_URL)
    first_apt_avail = datetime.strptime(date, '%A %B %d %Y')
    i_am_going_on = datetime.strptime(I_AM_GOING_TO_BARCELONA_ON, '%A %b %d %Y')
    diff = (i_am_going_on - first_apt_avail).days
    if diff > 20:
        message = "There is a visa appointment available on " + \
            str(date) + ", " + str(diff) + " days before your trip to Barcelona. "
        send_msg(message)


schedule.every(30).minutes.do(check_for_availability)

while True:
    schedule.run_pending()
    time.sleep(1)


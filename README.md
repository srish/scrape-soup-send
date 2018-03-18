Scrape, Soup & Send
===================
Schpeel for the motivation behind writing this script: 

I am going to Barcelona in May this year. I was planning to book an appointment for a visa through the Consulate of Spain in San Francisco. I still have two months before my trip, but there is no booking available until early June. 
Since past one or two days, I've frequently been going to the website to check if a slot has become available. I really don't want to go all the way to Los Angeles to apply for the VISA :-/ 

So, here goes a script that will run in the background on my local machine every 30 minutes. It will scrape the appointment page of the visa website, and check for an early availability. If so, I will get a text message.. better than reloading browser about 12 times in a day for about a month :-) 

For the scraping part, the script uses a combination of Selenium and BeautifulSoup with help from Geckodriver. For sending a text message, it is using Twilio's API. For the cron job part, it relies on the schedule module. Links below:
* https://pypi.python.org/pypi/selenium
* https://github.com/mozilla/geckodriver/releases
* https://pypi.python.org/pypi/beautifulsoup4
* https://www.twilio.com/docs/api/messaging/send-messages

To run the script in the background, run: 
```
python scrape-and-soup-and-send.py &
```

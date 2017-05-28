# WebShrinker API Key: Dtyq1tE7tyISKmVngc78
# Secret: fUIdiIWTtF1R6jPWG8NO


import os
import sqlite3
from collections import OrderedDict
import operator
import matplotlib.pyplot as plt

entertainment = ['youtube.com' , 'in.bookmyshow.com' ,'freshseries.net' , 'watchnaruto.tv' , 'paytm.com'];
sports = ['m.cricbuzz.com'];
social_networking = ['facebook.com' , 'linkedIn.com' ];
educational = ['udacity.com' , 'edx.org' , 'coursera.org' , 'quora.com' , 'w3schools.com' , 'tutorialspoint.com' , 'github.com' , 'localhost' , 'in.udacity.com' , 'classroom.udacity.com' , 'stackoverflow.com' , 'en.wikipedia.org'];

data_path = "C:/Users/nikhilvp/AppData/Local/Google/Chrome/User Data/Default"
files = os.listdir(data_path)
history_db = os.path.join(data_path, 'history')

c = sqlite3.connect(history_db)
cursor = c.cursor()

historyQuery = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(historyQuery)
historyResult = cursor.fetchall()
downloadQuery = "SELECT datetime(downloads.start_time), downloads.target_path, downloads_url_chains.url, downloads.received_bytes, downloads.total_bytes FROM downloads, downloads_url_chains WHERE downloads.id = downloads_url_chains.id;"
cursor.execute(downloadQuery)
downloadResult = cursor.fetchall()

def parse(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/', 1)
		domain = sublevel_split[0].replace("www.", "")
		return domain
	except IndexError:
		print("URL format error!")

sites_count = {} 

for url, count in historyResult:
	url = parse(url)
	if url in sites_count:
		sites_count[url] += 1
	else:
		sites_count[url] = 1

sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))
sites_count_sorted = {k: v for k, v in sites_count_sorted.items() if v >= 50}

plt.bar(range(len(sites_count_sorted)), sites_count_sorted.values(), align='edge')
plt.xticks(rotation=45)
plt.xticks(range(len(sites_count_sorted)), sites_count_sorted.keys())
plt.savefig('histogram.png')

#Pie Chart Showing the category of website visited
eCount=0
sCount=0
eduCount=0
sportCount=0
for key, value in sites_count_sorted.items():
	if key in entertainment:
		eCount +=value
	if key in social_networking:
		sCount +=value
	if key in educational:
		eduCount +=value
	if key in sports:
		sportCount +=value

total = eCount+sCount+eduCount+sportCount;
labels = 'Entertainment', 'Sports', 'Educational', 'Social Networking'
sizes = [(eCount/total)*100,(sportCount/total)*100,(eduCount/total)*100,(sCount/total)*100]
explode = (0, 0, 0, 0)  

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
ax1.axis('equal') 
plt.savefig('testplot.png')
 
data=0
for received_bytes in downloadResult:
	data += int(received_bytes[4])
data = data/(1024*1024*1024)
print("Total Data Downloaded: ")
print(data)
#plt.show()
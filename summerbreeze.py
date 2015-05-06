from lxml import html
import requests
import re
import csv
import os.path
import time

summer_breeze_tickets = []
if os.path.isfile('test.csv'):
	f = open('test.csv','rb')
	reader = csv.reader(f)
	for row in reader:
		desc = row[0]
		cost = row[1]
		times = row[2]
		entry = {"id": desc, "price": cost, "time": times}
		summer_breeze_tickets.append(entry)
	f.close()

next_page = True
def search_marketplace(number):
	global next_page
	string_to_visit = "http://marketplace.uchicago.edu/?commit=Search&mode=&order=&page=" + str(number) + "&q%5Bcategories_id_positive_and_eq%5D=0&q%5Bdetails_or_description_cont_any%5D=summer+breeze+ticket"
	page = requests.get(string_to_visit)
	tree = html.fromstring(page.text)

	ids = tree.xpath("//tr[@class='compact listing row']/@id")
	items = tree.xpath("//div[@class='description']/a/text()")
	times = tree.xpath("//td/time/@datetime")
	prices = tree.xpath("//td[@class='price twocol last']/text()")

	for index, item in enumerate(items):
		if re.search(r"(.ummer)\W(.reeze)",item) and not re.search(r"wanted",item, re.IGNORECASE):
			if prices[index+1] != "Free" and not any(entry['id'] == ids[index] for entry in summer_breeze_tickets):
				listing = {"id": ids[index], "price": prices[index+1], "time": times[index]}
				summer_breeze_tickets.append(listing)
				print ids[index], prices[index+1], times[index]
				with open('test.csv', 'a') as fp:
					a = csv.writer(fp)
					a.writerows([[ids[index], prices[index+1], times[index]]])
				fp.close()
	if not tree.xpath("//span[@class='next']/a"):
		next_page = False

while True:
	time.sleep(10)
	i = 1
	while next_page == True:
		print i
		search_marketplace(i)
		i = i + 1
	next_page = True

search_marketplace(11)
#print prices
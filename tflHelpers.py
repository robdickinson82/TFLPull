# -*- coding: utf-8 -*-
from config import *

import json
from string import split

from httpHelpers import *

from bsHelpers import *


opener = getCookieOpener()

def login():
	url = LOGINURL + "Login"

	data = {
		"UserName" : USERNAME,
		"Password" : PASSWORD
	}
	
	#response = opener.open (url)
	response = openUrl(url, data)

	return response


def open_tfl_url(path, data = None, headers = None):
	url = BASEURL + path
	response = openUrl(url, data, headers)
	return response	

def get_cards():
	cards = {}
	response = open_tfl_url("MyCards")	
		
	cards["original_html"] = response

	cards_soup = getSoupFromHtml(response.read())

	card_infos = cards_soup.findAll(attrs = {"data-pageobject" : "mycards-card-cardinfo"})

	cards["card_list"] = []
	cards["card_index"] = {}
	index = 0 
	for card_info in card_infos:
		card = {}
		card["links"] = {}
		card["links"]["card"] = card_info.find("a",attrs = {"data-pageobject" : "mycards-card-cardlink"})["href"]
		card["pi_ref"] = split(card["links"]["card"],"=")[1]
		card["card_type"] = card_info.find(attrs = {"data-pageobject" : "mycards-card-cardtype"}).string
		card["card_last_4"] = card_info.find(attrs = {"data-pageobject" : "mycards-card-cardnumber"}).string[13:17]
		card["card_status"] = card_info.find(attrs = {"data-pageobject" : "mycards-card-status"}).stripped_strings.next()
		cards["card_list"].append(card)
		cards["card_index"][card["pi_ref"]] = index
		get_links(card)
		index = index + 1
	print cards["card_index"]
	return cards

def get_card_details(card):
	url = "/Card/view?pi=" + card["pi_ref"]
	response = open_tfl_url(url)

def get_links(card):
	url = "Statements/ShowStatement?pi=" + card["pi_ref"]
	response = open_tfl_url(url)
	statement_soup = getSoupFromHtml(response.read())

	csv_container = statement_soup.find(id = 'travelstatement-csv-container')
	card["links"]["statement_csv"] = csv_container.a["href"]

	pdf_container = statement_soup.find(id = 'travelstatement-pdf-container')
	card["links"]["statement_pdf"] = pdf_container.a["href"]
	return

def download_statement_for_card(card, month = None, year = None, num_months = 0):
	get_links(card)	
	statement = download_statement(card["links"]["statement_csv"], month, year, num_months )
	print (statement)
	return statement

def download_statement(link, month = None, year = None, num_months = 0):
	statement = {}
	statement["end_year"] = year
	statement["end_month"] = month
	statement["num_months"] = num_months
	statement["entries"] = []
	end_months_since_0bc = 12 * year + month
	current_months_since_0bc = end_months_since_0bc - num_months
	while current_months_since_0bc <= end_months_since_0bc:
		url = link + "&sp="+ str(((current_months_since_0bc - 1) % 12) + 1) + "%7c" + str((current_months_since_0bc - 1) / 12)
		print (url)
		response = open_tfl_url(url)
		first_line = response.readline()
		# print(first_line[0], first_line)
		if first_line[0] == "D":
			for line in response.readlines():
				parts = split(line, ",")
				date_parts = split(parts[0], "/")
				entry = {
					"date": parts[0],
					"day": date_parts[0],
					"month": date_parts[1],
					"year": date_parts[2],
					"amount": parts[1].strip()
				}
				statement["entries"].append(entry)
		else:
			print ("problem getting CSV")
		current_months_since_0bc = current_months_since_0bc + 1
	return statement

#login()
#cards = get_cards()

#for card in cards["card_list"]:
#	get_links(card)
#	card["statement"] = download_statement(card["links"]["statement_csv"], 2, 2016, 0)
#	# print (card)
#	print (card["statement"])
#	for entry in card["statement"]["entries"]:
#		print (entry["date"], entry["amount"])



#__RequestVerificationToken:Xir254s6_d5KOzWjyZJxhyxk0Bu22_NsPTqYwcXRdeDCJAj4qF1Bq_CJ_yVBgssdGHb4JCJPF30Uj0HGkEfj_Om21eADDowgEFI64KqqAKI1
#PaymentCardId:PItZFRvMu28Tffqy6ivCxTXFHks-
#SelectedStatementType:Payments
#SelectedStatementPeriod:2|2016
# "/Statements/DownloadCsv?pi=PItZFRvMu28Tffqy6ivCxTXFHks-&amp;ti=xbaSUEjZLMCZFtmBeyTBSJTfW~U-&amp;st=Payments&amp;sp=2%7C2016&amp;doc=Payments"

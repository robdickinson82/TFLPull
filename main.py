# -*- coding: utf-8 -*-
from config import *

import json

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
		card["card_link"] = card_info.find("a",attrs = {"data-pageobject" : "mycards-card-cardlink"})["href"]
		card["card_type"] = card_info.find(attrs = {"data-pageobject" : "mycards-card-cardtype"}).string
		card["card_number"] = card_info.find(attrs = {"data-pageobject" : "mycards-card-cardnumber"}).string
		card["card_status"] = card_info.find(attrs = {"data-pageobject" : "mycards-card-status"}).stripped_strings.next()
		cards["card_list"].append(card)
		cards["card_index"][card["card_number"]] = index
		index = index + 1
	return cards

login()
cards = get_cards()

print (cards)



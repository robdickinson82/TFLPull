# -*- coding: utf-8 -*-
from config import *

from httpHelpers import *

from bsHelpers import *

from tflHelpers import *

from  flaskHelpers import *


login()
start_server()

#cards = get_cards()

#for card in cards["card_list"]:
#	get_links(card)
#	card["statement"] = download_statement(card["links"]["statement_csv"], 2, 2016, 0)
#	# print (card)
##	print (card["statement"])
#	for entry in card["statement"]["entries"]:
#		print (entry["date"], entry["amount"])



#__RequestVerificationToken:Xir254s6_d5KOzWjyZJxhyxk0Bu22_NsPTqYwcXRdeDCJAj4qF1Bq_CJ_yVBgssdGHb4JCJPF30Uj0HGkEfj_Om21eADDowgEFI64KqqAKI1
#PaymentCardId:PItZFRvMu28Tffqy6ivCxTXFHks-
#SelectedStatementType:Payments
#SelectedStatementPeriod:2|2016
# "/Statements/DownloadCsv?pi=PItZFRvMu28Tffqy6ivCxTXFHks-&amp;ti=xbaSUEjZLMCZFtmBeyTBSJTfW~U-&amp;st=Payments&amp;sp=2%7C2016&amp;doc=Payments"

from flask import Flask
from flask import render_template, request

from tflHelpers import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/download/')
def statement(card_pi):
	statement = download_statement_for_card(card, month = None, year = None, num_months = 0)
	return download_statement(card["links"]["statement_csv"], 2, 2016, 0)

@app.route('/cards/')
def cards():
	cards = get_cards()
	html = render_template('cards.html', cards = cards)
	return html

@app.route('/card/<pi_ref>')
def card(pi_ref):
	cards = get_cards()
	card = cards["card_list"][cards["card_index"][pi_ref]] 
	html = render_template('card.html', card = card)
	return html

@app.route('/card/<pi_ref>/csv_statement/<int:year>/<int:month>')
def csv_statement(pi_ref, month, year):
	num_months = int(request.args.get('num_months', 0))
	cards = get_cards()
	selected_card = cards["card_list"][cards["card_index"][pi_ref]] 
	statement = download_statement_for_card(selected_card, month, year, num_months)
	print (statement)
	html = render_template('statement.html', statement = statement)
	return html

def start_server():
	app.debug = DEBUG
	app.run()
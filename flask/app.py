from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from flask import make_response
from flask import g
from flask import session, escape
from flask import jsonify
from datetime import datetime
from elasticsearch import Elasticsearch
from src import Pylastic_Interface as searcher


es = Elasticsearch(timeout=300)

class CustomFlask(Flask):
	jinja_options = Flask.jinja_options.copy()
	jinja_options.update(dict(
	block_start_string='$$',
	block_end_string='$$',
	variable_start_string='$',
	variable_end_string='$',
	comment_start_string='$#',
	comment_end_string='#$',
	))

app = CustomFlask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/q')
def query():
	queryString = request.args.get('queryString')
	raw_results = searcher.execute_pylastic_search(queryString, type = 'bool')
	results = []
	for single_result in raw_results:
		dict_form = {}
		dict_form['datasetName'] = single_result['datasetName']
		dict_form['datasetDescription'] = single_result['datasetDescription']
		dict_form['score'] = single_result['score']
		dict_form['datasetDistribution'] = single_result['datasetDistribution']
		results.append(dict_form)
	print len(results)
	return jsonify(results)







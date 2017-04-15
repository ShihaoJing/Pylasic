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
	res = es.search(index="baseindex", body={"_source": ["description", "title", "downloadURL", "keyword"], 
		"query": {"match": {"description": queryString}}})
	source = []
	for hit in res['hits']['hits']:
		source.append(hit["_source"])
	print len(source)
	return jsonify(source)







from flask import Flask
from flask import render_template
from flask import request
from flask import abort, redirect, url_for
from flask import make_response
from flask import g
from flask import session, escape
from flask import jsonify
import requests
import hashlib
import random
import string
import os
import re
import base64
import dropbox
import json
import ssl

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








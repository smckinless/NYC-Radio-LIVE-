from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.utils import secure_filename
import jinja2
import os
import json
import re

from datetime import datetime
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId, InvalidId

from flask.ext.login import LoginManager , login_user ,logout_user, current_user, login_required, UserMixin


import time
from datetime import datetime

import os

#UPLOAD_FOLDER = 'uploads/'	
#ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg','PDF','PNG','JPG','JPEG'])


#MongoDB Set Up
connection = MongoClient('ds059821.mongolab.com', 59821)
db = connection["nycradiolive"]
db.authenticate("admin.nycradiolive","McKindo12345")

#Collections
PODCASTS = db.Podcasts

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
	if request.method == 'POST':
		form = request.form
	else:
		return render_template('admin.html', error="Please fill in all fields properly.")

	Podcasts = {}
	Podcasts['title'] = form['title']
	Podcasts['genre'] = form['genre']
	Podcasts['artist'] = form['artist']
	Podcasts['text'] = form['text']
	Podcasts['author'] = form['author']
	Podcasts['tags'] = form['tags']
	Podcasts['image'] = form['image']
	Podcasts['date'] = datetime.date

	PODCASTS.insert(Podcasts)

	#file = request.form['image']
	#filename = secure_filename(file.filename)
	#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

	return render_template('admin.html')


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')

#def email(to, from_email, subject, info, template):
#	Email = {}
#	Email['name'] = form['name']
#	Email['email'] = form['email']
#	Email['phone'] = form['phone']
#	Email['message'] = form['message']

#	email("smckinless@gmail.com", Email['name'], "Website Question", Email['message'], "hi")

@app.route('/blog', methods=['GET','POST'])
def blog():
	genres = PODCASTS.distinct("genre")
	results = PODCASTS.find()
	tags = PODCASTS.distinct("tags")
	artists = PODCASTS.distinct("artist")
	#for i in range(0, len(results)):
	

	return render_template('blog.html', results=results, total=PODCASTS.find().count(), genres=genres, tags=tags, artists=artists)
	#posts = PODCASTS.find_one({'_id' : ObjectId(id)})

@app.route('/archives', methods=['GET', 'POST'])
def archives():
	genres = PODCASTS.distinct("genre")
	results = PODCASTS.find()
	tags = PODCASTS.distinct("tags")
	artists = PODCASTS.distinct("artist")
	return render_template('archive_page.html', results=results, total=PODCASTS.find().count(), genres=genres, tags=tags, artists=artists)

if __name__ == '__main__':
#	if 'DYNO' in os.environ:
#	    debug = False
	app.run()

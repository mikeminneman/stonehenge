from flask import Flask, request, render_template
app = Flask(__name__)

# Console Copy Start
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import config

Base = automap_base()
engine = create_engine(config.pgsql["string"])
Base.prepare(engine, reflect=True)
Posts = Base.classes.posts
session = Session(engine)

import re
import binascii
import base64
from Crypto.Cipher import DES3
from Crypto.Hash import MD5

from shdecoders import *
# Console Copy End

@app.errorhandler(500)
def pageNotFound(error):
	print(error)
	return "500: "+str(error)
	
@app.route('/')
def display_index():
	posts=session.query(Posts).limit(100).all()
	return render_template('show_posts.html',posts=posts)
	
@app.route('/post/<int:post_id>')
@app.route('/id/<int:post_id>')
def show_id(post_id):
	post=session.query(Posts).filter_by(id=post_id).first()
	return display_post(post)

@app.route('/post/<string:post_shortcode>')
@app.route('/shortcode/<string:post_shortcode>')
def show_shortcode(post_shortcode):
	post=session.query(Posts).filter_by(shortcode=post_shortcode).first()
	return display_post(post)

@app.route('/title/<string:post_title>')
def show_title(post_title):
	post=session.query(Posts).filter_by(title=post_title).first()
	return display_post(post)

def get_shortcode(post_link):
	shortcodematch = re.compile("(?:comments\/=?)([a-z0-9]*)(\/[0-9]*)").search(post_link)
	shortcode = "" if shortcodematch == None else shortcodematch.group(1)
	return shortcode
	
def get_soulsphere(post_shortcode):
	soulsphere_start = "http://a858.soulsphere.org/?id="
	return soulsphere_start+post_shortcode
	
def get_redditwiki(post_title):
	redditwiki_start = "https://www.reddit.com/r/Solving_A858/wiki/"
	return redditwiki_start+post_title

def display_post(post):
	post.soulsphere = get_soulsphere(post.shortcode)
	post.redditwiki = get_redditwiki(post.title)
	post.unhex = unhex(post.content)
	post.unb64 = unb64(post.unhex)
	post.unb64_ascii = unb64codec(post.unb64,'ascii')
	post.unb64_ascii_unhex = unhex(post.unb64_ascii)
	post.unb64_utf8 = unb64codec(post.unb64, 'utf-8')
	post.b64 = b64(post.content)
	md5a858 = "34a14a42e98ff96095af56604e290cae"
	md5a858des3 = des3decrypt(post.content,md5a858)
	md5a858des3cbc = des3decryptcbc(post.content,md5a858,"0000000000000000")
	post.md5a858des3 = md5a858des3
	post.md5a858des3_ascii = unb64codec(md5a858des3,'ascii')
	post.md5a858des3_utf8 = unb64codec(md5a858des3,'utf8')
	post.md5a858des3cbc = str(md5a858des3cbc)
	return render_template('show_one_post.html',post=post)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
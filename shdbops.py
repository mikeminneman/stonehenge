from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import config

Base = automap_base()
engine = create_engine(config.pgsql["string"])
Base.prepare(engine, reflect=True)
Posts = Base.classes.posts
session = Session(engine)

from shinfo import *

def getbyid(post_id):
	post=session.query(Posts).filter_by(id=post_id).first()
	return post
	
def getbyshortcode(post_shortcode):
	post=session.query(Posts).filter_by(shortcode=post_shortcode).first()
	return post
	
def getbytitle(post_title):
	post=session.query(Posts).filter_by(title=post_title).first()
	return post
	
def getlimitedposts(limit):
	posts=session.query(Posts).limit(limit).all()
	return posts
	
def getallposts():
	posts=session.query(Posts).all()
	return posts
	
def populate_shortcodes():
	posts=getallposts()
	for post in posts:
		if hasattr(post, 'shortcode'):
			post.shortcode = get_shortcode(post.link)
		else:
			return False
	session.commit()
	return True
	
def populate_lengths():
	posts=getallposts()
	for post in posts:
		if hasattr(post, 'length'):
			post.length = get_length(post.content)
		else:
			return False
	session.commit()
	return True
	
import binascii
def getbytes(post_shortcode):
	post=getbyshortcode(post_shortcode)
	return binascii.unhexlify(post.content.replace(" ",""))
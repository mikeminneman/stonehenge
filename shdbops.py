from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

import config

Base = automap_base()
engine = create_engine(config.pgsql["string"])
Base.prepare(engine, reflect=True)
if hasattr(Base.classes,'posts'):
	Posts = Base.classes.posts
if hasattr(Base.classes,'keys'):
	Keys = Base.classes.keys
session = Session(engine)

from shinfo import *
import binascii

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
	
def getbytes(post_shortcode):
	post=getbyshortcode(post_shortcode)
	return binascii.unhexlify(post.content.replace(" ",""))
	
def getkeys():
	keylist=[]
	# if hasattr(Base.classes,'keys'):
		# keys = session.query(Keys).all()
		# for key in keys:
			# keylist.append(bytes(key.key,encoding='utf-8'))
	posts = getallposts()
	for post in posts:
		keylist.append(bytes(post.title,encoding='utf-8'))
	keylist+=[b'A858DE45F56D9BC9',b'A858DE45F56D9BC9A858DE45F56D9BC9',b'0000DE45',b'f8278df7c61e8ed0b77cb19c2b0e6e20',b'34A14A42E98FF96095AF56604E290CAE']
	return keylist
	
def getivs(): # should be replaced by db table
	ivs=[b'\0\0\0\0\0\0\0\0',b'ff4e00a2']
	return ivs
	

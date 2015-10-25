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
from Crypto.Hash import MD5

def getbyid(post_id):
	post=session.query(Posts).filter_by(id=post_id).first()
	return post
	
def getbyshortcode(post_shortcode):
	post=session.query(Posts).filter_by(shortcode=post_shortcode).first()
	return post
	
def getbytitle(post_title):
	post=session.query(Posts).filter_by(title=post_title).first()
	return post

def getbymd5(post_md5):
	post=session.query(Posts).filter_by(md5=post_md5).first()
	return post

def gettitlefrommd5(post_md5):
	post=getbymd5(post_md5)
	if hasattr(post,'title'):
		return getbymd5(post_md5).title
	else:
		return ''
	
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
	
def populate_md5():
	posts=getallposts()
	for post in posts:
		if hasattr(post, 'md5'):
			content = "" if not(type(post.content)==str) else post.content
			m=MD5.new()
			m.update(content.encode('utf-8'))
			post.md5 = binascii.hexlify(m.digest()).decode('utf-8')
		else:
			return False
	session.commit()
	return True
	
def getbytes(post_shortcode):
	post=getbyshortcode(post_shortcode)
	return binascii.unhexlify(post.content.replace(" ",""))
	
def getkeys(md5=''):
	keylist=[]
	# if hasattr(Base.classes,'keys'):
		# keys = session.query(Keys).all()
		# for key in keys:
			# keylist.append(bytes(key.key,encoding='utf-8'))
	keylist+=[b'A858DE45F56D9BC9',b'A858DE45F56D9BC9A858DE45F56D9BC9',b'0000DE45',b'f8278df7c61e8ed0b77cb19c2b0e6e20',b'34A14A42E98FF96095AF56604E290CAE']
	if md5!='':
		title=gettitlefrommd5(md5)
		for i in range(0,len(keylist)):
			keylist.append(keylist[i]+title.encode('utf-8'))
			keylist.append(title.encode('utf-8')+keylist[i])
		keylist.append(title.encode('utf-8'))
	return keylist
	
def getivs(): # should be replaced by db table
	ivs=[b'\0\0\0\0\0\0\0\0',b'ff4e00a2',binascii.unhexlify(b'cf40ad098ec6a4a8')]
	return ivs
	

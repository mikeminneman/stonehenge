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
	keylist+=[b'A858DE45F56D9BC9',b'A858DE45F56D9BC9A858DE45F56D9BC9',b'0000DE45',b'f8278df7c61e8ed0b77cb19c2b0e6e20',b'34A14A42E98FF96095AF56604E290CAE',b'493a512bedb2d671',b'03201255f2bdd9f9',b'2ae6f840218074a5',b"cf95370b70ea1508",b"03201255f2bdd9f9",b"12bd9a8e5a7752c0",b"4fd521f3b5f224bf",b"493a512bedb2d671",b"a9c7eccc70639090",b"2ae6f840218074a5",b"00000000000000000000000000000000",b"0000000000004000000000000000000E",b"00000000000040000000000000000018",b"00000000000000000000000000000000",b"00000000000000000000000000000000",b"0000000000004000000000000000000C",b"00000000000000000000000000000000",b"00000000000040000000000000000008",b"00000000000040000000000000000008",b"00000000000000000000000000000000",b"0000000000004000000000000000002C",b"00000000000040000000000000000004",b"00000000000000000000000000000000",b"0000000000257959",b"00000000000040000000000000000000",b"00000000000040000000000000000004",b"F8E2417DCC2CC99C9E1804CF1A268158",b"d89c1f56a137da47",b"ee3564084657aa64",b"2976317d8d6471ab",b"37fa4273319ebbe2",b"309355b4ce05a0de",b"0cd1675e7b42dafb",b"497f49c86a164139",b"a8af029209951494",b"edbff341849d8d94",b"82d71c4af1efe43c",b"1d6961e8c13f35ef",b"55548a0c7a62f4d6",b"97e43514c2c8d821",b"0fbb3d5ff812bb0a",b"668413aa493ac237",b"ff132db816f14c0f",b"c7b57e5b98602c3b",b"0000000000000000",b"0000000000000000",b"83c00f67acbf8eb3",b"0000000000000000",b"87516c5f160edde5",b"5bc76a64a8e7b611",b"a9d9c2358a0bcad3",b"b05c2b4083b39a51",b"e08c595739e3ecec",b"3efeb7f62ece89da",b"cc0ffd21b4e9f778",b"9ad90edbd61773dd",b"3ddfea78870d93dd",b"8258d028b35d4a45",b"25f7bb2735443b00",b"22fbe4951d2855f1",b"53ff593d5acd1014",b"98303fecc3e044f8",b"488f704f57cce3a6",b"e63d37a8220fe3f2",b"512b7e620f745313",b"2cf72b0f5df118f8",b"50e8df5dcc614a65",b"c21e773482dd63e7",b"d2cda661ac72e6f6",b"7e9f175869d0fd12",b"f0bb6943914a961f",b"666bf9be34f2273e",b"0ed3df86eb975cf6",b"d47b280787e36bf1",b"ad831d44d263fe8a",b"4a79680f573a8e98",b"c9e7a7d1a9531461",b"b13cf45340c19e8b",b"fbf1ae880534e348",b"cf95370b70ea1508",b"03201255f2bdd9f9",b"12bd9a8e5a7752c0",b"4fd521f3b5f224bf",b"493a512bedb2d671",b"a9c7eccc70639090",b"2ae6f840218074a5",b"00000000000000000000000000000000",b"0000000000004000000000000000000E",b"00000000000040000000000000000018",b"00000000000000000000000000000000",b"00000000000000000000000000000000",b"0000000000004000000000000000000C",b"00000000000000000000000000000000",b"00000000000040000000000000000008",b"00000000000040000000000000000008",b"00000000000000000000000000000000",b"0000000000004000000000000000002C",b"00000000000040000000000000000004",b"00000000000000000000000000000000",b"0000000000257959",b"00000000000040000000000000000000",b"00000000000040000000000000000004",b"F8E2417DCC2CC99C9E1804CF1A268158",b"9E1804CF1A268158",b"F8E2417DCC2CC99C",b"d89c1f56a137da47",b"ee3564084657aa64",b"2976317d8d6471ab",b"37fa4273319ebbe2",b"309355b4ce05a0de",b"0cd1675e7b42dafb",b"497f49c86a164139",b"a8af029209951494",b"edbff341849d8d94",b"82d71c4af1efe43c",b"1d6961e8c13f35ef",b"55548a0c7a62f4d6",b"97e43514c2c8d821",b"0fbb3d5ff812bb0a",b"668413aa493ac237",b"ff132db816f14c0f",b"c7b57e5b98602c3b",b"0000000000000000",b"0000000000000000",b"83c00f67acbf8eb3",b"0000000000000000",b"87516c5f160edde5",b"5bc76a64a8e7b611",b"a9d9c2358a0bcad3",b"b05c2b4083b39a51",b"e08c595739e3ecec",b"3efeb7f62ece89da",b"cc0ffd21b4e9f778",b"9ad90edbd61773dd",b"3ddfea78870d93dd",b"8258d028b35d4a45",b"25f7bb2735443b00",b"22fbe4951d2855f1",b"53ff593d5acd1014",b"98303fecc3e044f8",b"488f704f57cce3a6",b"e63d37a8220fe3f2",b"512b7e620f745313",b"2cf72b0f5df118f8",b"50e8df5dcc614a65",b"c21e773482dd63e7",b"d2cda661ac72e6f6",b"7e9f175869d0fd12",b"f0bb6943914a961f",b"666bf9be34f2273e",b"0ed3df86eb975cf6",b"d47b280787e36bf1",b"ad831d44d263fe8a",b"4a79680f573a8e98",b"c9e7a7d1a9531461",b"b13cf45340c19e8b",b"fbf1ae880534e348"]
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
	

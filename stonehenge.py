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

def unhex(post_content):
	try:
		post_nospace = post_content.replace(" ", "")
		post_unhex = binascii.unhexlify(post_nospace).decode('ascii')
	except:
		post_unhex = ""
		pass
	return post_unhex
	
def unb64(post_base64):
	try:
		post_unb64 = base64.b64decode(post_base64)
	except:
		post_unb64 = ""
		pass
	return post_unb64
	
def unb64codec(post_b64, codec):
	try:
		post_unb64_text = post_b64.decode(codec)
	except:
		post_unb64_text = ""
		pass
	return post_unb64_text
	
def b64(post_content):
	try:
		post_nospace = post_content.replace(" ", "")
		post_unhex_noascii = binascii.unhexlify(post_nospace)
		base64_bin = base64.b64encode(post_unhex_noascii)
		base64_ascii = base64_bin.decode('ascii')
	except:
		base64_ascii = ""
		pass
	return str(base64_ascii)
	
def des3decrypt(post_content,key):
	try:
		post_nospace = post_content.replace(" ", "")
		post_unhex_noascii = binascii.unhexlify(post_nospace)
		ct = post_unhex_noascii
		key_unhex = binascii.unhexlify(key)
		obj = DES3.new(key_unhex,DES3.MODE_ECB)
		pt = obj.decrypt(ct)
	except:
		pt = ""
		pass
	return pt

def des3decryptcbc(post_content,key,iv):
	try:
		post_nospace = post_content.replace(" ", "")
		post_unhex_noascii = binascii.unhexlify(post_nospace)
		ct = post_unhex_noascii
		key_unhex = binascii.unhexlify(key)
		iv_unhex = binascii.unhexlify(iv)
		obj = DES3.new(key_unhex,DES3.MODE_CBC,iv_unhex)
		pt = obj.decrypt(ct)
	except:
		pt = ""
		pass
	return pt

def display_post(post):
	returnstring  = "<html>\n"
	returnstring += "<head><title>"+post.shortcode+" "+post.title+"</title>\n"
	returnstring += "<body style='font-family: monospace;'>\n"
	returnstring += "Id: "+str(post.id)+"<br />\n"
	returnstring += "Link: <a href='"+post.link+"'>"+post.link+"</a><br />\n"
	returnstring += "Autologger: <a href='"+get_soulsphere(post.shortcode)+"'>"+get_soulsphere(post.shortcode)+"</a><br />\n"
	returnstring += "Wiki: <a href='"+get_redditwiki(post.title)+"'>"+get_redditwiki(post.title)+"</a><br />\n"
	returnstring += "Shortcode: "+post.shortcode+"<br />\n"
	returnstring += "Title: "+post.title+"<br /><br />\n"
	returnstring += "Content: <br />\n"+str(post.content)+"<br /><br />\n"
	post_unhex = unhex(post.content)
	returnstring += "Unhexed: <br />\n"+post_unhex+"<br /><br />\n"
	post_unb64 = unb64(post_unhex)
	post_unb64_ascii = unb64codec(post_unb64, 'ascii')
	post_unb64_utf8 = unb64codec(post_unb64, 'utf-8')
	returnstring += "Base 64 Decode as ASCII: <br />\n"+post_unb64_ascii+"<br /><br />\n"
	returnstring += "Base 64 Decode as ASCII and Unhexed: <br />\n"+unhex(post_unb64_ascii)+"<br /><br />\n"
	returnstring += "Base 64 Decode as UTF-8: <br />\n"+post_unb64_utf8+"<br /><br />\n"
	post_b64 = b64(post.content)
	md5a858 = "34a14a42e98ff96095af56604e290cae"
	md5a858des3 = des3decrypt(post.content,md5a858)
	md5a858des3cbc = des3decryptcbc(post.content,md5a858,"0000000000000000")
	returnstring += "A858 DES-EDE-ECB as ASCII: <br />\n"+unb64codec(md5a858des3,'ascii')+"<br /><br />\n"
	returnstring += "A858 DES-EDE-ECB as UTF-8: <br />\n"+unb64codec(md5a858des3,'utf-8')+"<br /><br />\n"
	returnstring += "A858 DES-EDE-CBC with IV 0: <br />\n"+str(md5a858des3cbc)+"<br /><br />\n"
	returnstring += "Images: <br />\n<img src='data:image/gif;base64,"+post_b64+"' /><br /><br />\n"
	returnstring += "</body>\n</html>\n"
	return returnstring

if __name__ == '__main__':
    app.run(host='0.0.0.0')
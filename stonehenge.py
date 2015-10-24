from flask import Flask, request, render_template
app = Flask(__name__)

from shdecoders import *
from shdbops import *

@app.errorhandler(500)
def pageNotFound(error):
	print(error)
	return "500: "+str(error)
	
@app.route('/')
def display_index():
	posts=getlimitedposts(100)
	return render_template('show_posts.html',posts=posts)
	
@app.route('/post/<int:post_id>')
@app.route('/id/<int:post_id>')
def show_id(post_id):
	post=getbyid(post_id)
	return display_post(post)

@app.route('/post/<string:post_shortcode>')
@app.route('/shortcode/<string:post_shortcode>')
def show_shortcode(post_shortcode):
	post=getbyshortcode(post_shortcode)
	return display_post(post)

@app.route('/title/<string:post_title>')
def show_title(post_title):
	post=getbytitle(post_title)
	return display_post(post)

def display_post(post):
	post.shortcode = get_shortcode(post.link) if not(hasattr(post, 'shortcode')) else post.shortcode
	post.length = get_length(post.content) if not(hasattr(post, 'length')) else post.length
	post.soulsphere = get_soulsphere(post.shortcode)
	post.redditwiki = get_redditwiki(post.title)
	post.unhex = unhex(post.content)
	post.unb64 = unb64(post.unhex)
	post.unb64_utf8 = unb64codec(post.unb64, 'utf-8')
	#post.unb64_utf8_ascii = utf2ascii(post.unb64_utf8)
	post.unb64_utf8_unhex = unhex(post.unb64_utf8)
	post.b64 = b64(post.content)
	md5a858 = "34a14a42e98ff96095af56604e290cae"
	md5a858des3 = des3decrypt(post.content,md5a858)
	md5a858des3cbc = des3decryptcbc(post.content,md5a858,"0000000000000000")
	post.md5a858des3 = md5a858des3
	post.md5a858des3_utf8 = unb64codec(md5a858des3,'utf-8')
	try:
		post.md5a858des3cbc = str(md5a858des3cbc,encoding='utf-8',errors='replace')
	except:
		post.md5a858des3cbc = md5a858des3cbc
		pass
	return render_template('show_one_post.html',post=post)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
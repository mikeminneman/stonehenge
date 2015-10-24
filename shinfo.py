#import string
import re

def get_shortcode(post_link):
	shortcodematch = re.compile("(?:comments\/=?)([a-z0-9]*)(\/[0-9]*)").search(post_link)
	shortcode = "" if shortcodematch == None else shortcodematch.group(1)
	return shortcode
	
def get_length(post_content):
	try:
		length = len(post_content.replace(" ",""))
	except:
		length = 0
		pass
	return length
	
def get_soulsphere(post_shortcode):
	soulsphere_start = "http://a858.soulsphere.org/?id="
	return soulsphere_start+post_shortcode
	
def get_redditwiki(post_title):
	redditwiki_start = "https://www.reddit.com/r/Solving_A858/wiki/"
	return redditwiki_start+post_title

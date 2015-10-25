import string
from decoders import *

def detect_spaces(text): # returns boolean
	if type(text) == bytes:
		return (b' ' in text) or (b'\r' in text) or (b'\n' in text) or (b'\t' in text)
	elif type(text) == str:
		return (' ' in text) or ('\r' in text) or ('\n' in text) or ('\t' in text)
	return False

def detect_hex(text): # returns boolean
	if type(text) == bytes:
		return all(c in bytes(string.hexdigits,encoding='utf-8') for c in text)
	elif type(text) == str:
		return all(c in string.hexdigits for c in text)
	return False
	
def detect_hex_w_spaces(text):
	return detect_spaces(text) and detect_hex(remove_spaces(text))
	
def detect_hex_replaced_3A(text):
	if detect_spaces(text):
		text=remove_spaces(text)
	if type(text) == bytes:
		return all(c in bytes(string.hexdigits+'#Vv',encoding='utf-8') for c in text)
	elif type(text) == str:
		return all(c in string.hexdigits+'#Vv' for c in text)
	return False
	
def detect_base64(text):
	validchars=string.ascii_letters+string.digits+'+/='
	validbytes=bytes(validchars,encoding='utf-8')
	if type(text) == bytes:
		return len(text)%4==0 and all(c in validbytes for c in text)
	elif type(text) == str:
		return len(text)%4==0 and all(c in validchars for c in text)
	return False
	
def detect_ascii(val): # returns boolean
	try:
		result = str(val,encoding='ascii')
	except UnicodeDecodeError:
		result = ''
	return len(result)>0

def detect_utf8(val): # returns boolean
	try:
		result = str(val,encoding='utf-8')
	except UnicodeDecodeError:
		result = ''
	return len(result)>0



	
	

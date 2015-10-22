import string
import re
import binascii
import base64
from Crypto.Cipher import DES3
from Crypto.Hash import MD5

def detect_spaces(text): # returns boolean
	return (' ' in text)

def remove_spaces(text): # returns string
	return text.replace(" ","")
	
def detect_hex(text): # returns boolean
	return all(c in string.hexdigits for c in text)

def hex2num(text): # returns value
	return binascii.unhexlify(text)

def detect_ascii(val): # returns boolean
	try:
		result = str(val,encoding='ascii')
	except UnicodeDecodeError:
		result = ''
	return len(result)>0

def decode_ascii(val): # returns string
	try:
		result = str(val,encoding='ascii')
	except UnicodeDecodeError:
		result = ''
	return result

def encode_ascii(text): # returns value
	return text.encode('ascii')

def detect_utf8(val): # returns boolean
	try:
		result = str(val,encoding='utf-8')
	except UnicodeDecodeError:
		result = ''
	return len(result)>0

def decode_utf8(val): # returns string
	try:
		result = str(val,encoding='utf-8')
	except UnicodeDecodeError:
		result = ''
	return result
	
def encode_utf8(text): # returns value
	return text.encode('utf-8')

def decode_b64(val): # returns value
	return base64.b64decode(val)
	
def encode_b64(val): # returns value
	return base64.b64encode(val)
	
def encode_md5(val): # returns value
	m = MD5.new()
	m.update(val)
	return m.digest()

def decode_des3_ecb(ct, key): # takes values, returns value
	d = DES3.new(key,DES3.MODE_ECB)
	return d.decrypt(ct)

def decode_des3_cbc(ct, key, iv): # takes values, returns value
	d = DES3.new(key,DES3.MODE_CBC, iv)
	return d.decrypt(ct)

def add_n_after_20(text): # returns string
	result = ""
	for i in range(0, len(text)):
		result+=text[i]
		if (i+1)%20 == 0:
			result+='\n'
	return result
	
	
#Legacy

def unhex(post_content):
	try:
		post_nospace = remove_spaces(post_content)
		post_unhex = hex2num(post_nospace)
		post_utf8 = decode_utf8(post_unhex)
	except:
		post_utf8=""
	return post_utf8
	
def unb64(post_base64):
	post_unb64 = decode_b64(post_base64)
	return post_unb64
	
def unb64codec(post_b64, codec):
	try:
		post_unb64_text = post_b64.decode(codec)
	except:
		post_unb64_text = ""
		pass
	return post_unb64_text
	
def b64(post_content):
	post_nospace = remove_spaces(post_content)
	post_unhex = hex2num(post_nospace)
	base64_bin = encode_b64(post_unhex)
	base64_utf8 = decode_utf8(base64_bin)
	return base64_utf8
	
def des3decrypt(post_content,key_hex):
	try:
		post_nospace = remove_spaces(post_content)
		post_unhex_noascii = hex2num(post_nospace)
		ct = post_unhex_noascii
		key = hex2num(key_hex)
		pt = decode_des3_ecb(ct,key)
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

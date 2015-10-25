import binascii
import base64
from unidecode import unidecode
from Crypto.Cipher import DES3
from Crypto.Hash import MD5
from detectors import *


	
def decode_hexlike(content):
	if type(content) == bytes:
		nosp = b''
		for i in range(0,len(content)):
			if content[i:i+1]==b'#':
				nosp+=b'3'
			elif content[i:i+1]==b'V':
				nosp+=b'A'
			elif content[i:i+1]==b'v':
				nosp+=b'a'			
			else:
				nosp+=content[i:i+1]
		return nosp
	elif type(content) == str:
		return content.replace("#","3").replace("V","A").replace("v","a")
	return b''

def decode_hex(content):
	if type(content) == bytes:
		return binascii.unhexlify(content)
	elif type(content) == str:
		return binascii.unhexlify(bytes(content,encoding='utf-8'))
	return b''

def decode_base64(content):
	if type(content) == bytes:
		try:
			return base64.b64decode(content)
		except:
			return b""
			pass
	elif type(content) == str:
		try:
			return base64.b64decode(bytes(content,encoding='utf-8'))
		except:
			return ""
			pass
	return b''

def getkeys(): # should be replaced by db table
	keys=[b'A858DE45F56D9BC9',b'0000DE45']
	return keys
	
def getivs(): # should be replaced by db tabl
	ivs=[b'\0\0\0\0\0\0\0\0']
	return ivs
	
def decode_des3ecb(content):
	keys=getkeys()
	pt=b''
	for key in keys:
		m=encode_md5(key)
		pt=decode_des3_ecb(content,m)
		if detect_utf8(pt):
			return pt
	return b''
	
def decode_des3ecb_title(content):
	pt=b''
	key=b'post title' #but how to get this
	m=encode_md5(key)
	pt=decode_des3_ecb(content,m)
	if detect_utf8(pt):
		return pt
	return b''
	
def decode_des3cbc(content):
	keys=getkeys()
	ivs=getivs()
	pt=b''
	for key in keys:
		m=encode_md5(key)
		for iv in ivs:
			pt=decode_des3_cbc(content,m,iv)
			if detect_utf8(pt):
				return pt
		if detect_utf8(remove_first8(pt)):
			return pt
	return b''
	
def decode_des3cbc_title(content):
	pt=b''
	key=b'post title' #but how to get this
	m=encode_md5(key)
	ivs=getivs();
	for iv in ivs:
		pt=decode_des3_cbc(content,m,iv)
		if detect_utf8(pt):
			return pt
	if detect_utf8(remove_first8(pt)):
		return(pt)
	return b''
	
	
	
	
def decode_ascii(val): # returns string
	try:
		result = str(val,encoding='ascii')
	except UnicodeDecodeError:
		result = ''
	return result

def encode_ascii(text): # returns value
	return text.encode('ascii')

def decode_utf8(val): # returns string
	try:
		result = str(val,encoding='utf-8')
	except UnicodeDecodeError:
		result = ''
	return result
	
def encode_utf8(text): # returns value
	return text.encode('utf-8')

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

def add_n_after_x(text,x):
	if type(text)=='bytes':
		result=b''
		for i in range(0, len(text)):
			result+=text[i]
			if (i+1)%x == 0:
				result+=b'\n'
	elif type(text)=='str':
		result = ""
		for i in range(0, len(text)):
			result+=text[i]
			if (i+1)%x == 0:
				result+='\n'
	else:
		result=b''
	return result
	
def utf2ascii(text): # returns text
	return unidecode(text)
	

	
#Legacy

def hex2num(text): # returns value
	return decode_hex(text)

def decode_b64(val): # returns value
	return decode_base64(val)
	


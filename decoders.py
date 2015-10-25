import binascii
import base64
from unidecode import unidecode
from Crypto.Cipher import DES3
from Crypto.Hash import MD5
from detectors import *
from shdbops import *

	
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
	if len(content)%2==0:
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

def decode_des3ecb(content,md5=''):
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	key=find_key_des3ecb(content,md5)
	pt=try_key_des3ecb(content,key,md5)
	if detect_utf8(pt):
		return pt		
	return b''
	
def find_key_des3ecb(content,md5=''):
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	keys=getkeys(md5)
	pt=b''
	for key in keys:
		pt=try_key_des3ecb(content,key,md5)
		if len(pt)>0:
			return key
	return b'0000000000000000'
	
def try_key_des3ecb(content,key,md5=''):
	print("Trying key: "+str(key))
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	returnpt=b''
	if len(key)==16:
		m=key
		pt=decode_des3_ecb(content,m)
		if detect_utf8(pt):
			returnpt=pt
	if len(key)==32 and detect_hex(key):
		m=binascii.unhexlify(key)
		pt=decode_des3_ecb(content,m)
		if detect_utf8(pt):
			returnpt=pt
	if True:
		m=encode_md5(key)
		pt=decode_des3_ecb(content,m)
		if detect_utf8(pt):
			returnpt=pt
	return returnpt
	
def decode_des3cbc(content,md5=''):
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	key=find_key_des3cbc(content,md5)
	pt=try_key_des3cbc(content,key,md5)
	if detect_utf8(pt) or detect_utf8end(pt):
		return pt		
	return b''
	
def find_key_des3cbc(content,md5=''):
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	keys=getkeys(md5)
	pt=b''
	for key in keys:
		pt=try_key_des3cbc(content,key,md5)
		if len(pt)>0:
			return key
	return b'0000000000000000'
	
def try_key_des3cbc(content,key,md5=''):
	print("Trying key: "+str(key))
	if md5=='':
		md5=binascii.hexlify(encode_md5(content)).decode('utf-8')
	returnpt=b''
	ivs=getivs()
	if len(key)==16:
		m=key
		for iv in ivs:
			pt=decode_des3_cbc(content,m,iv)
			if detect_utf8(pt):
				returnpt=pt
		if detect_utf8(remove_first8(pt)):
			returnpt=pt
	if len(key)==32 and detect_hex(key):
		m=binascii.unhexlify(key)
		for iv in ivs:
			pt=decode_des3_cbc(content,m,iv)
			if detect_utf8(pt):
				returnpt=pt
		if detect_utf8(remove_first8(pt)):
			returnp =pt
	if True:
		m=encode_md5(key)
		for iv in ivs:
			pt=decode_des3_cbc(content,m,iv)
			if detect_utf8(pt):
				returnpt=pt
		if detect_utf8(remove_first8(pt)):
			returnpt=pt
	return returnpt
	
def rotate_breaks(content):
	content_str=content.decode('utf-8')
	content_arr=content_str.split('\r\n')
	num_col=len(content_arr[0])
	num_row=len(content_arr)
	result=''
	for col in range(0,num_col):
		for row in range(0,num_row):
			result+=content_arr[row][col]
	return result.encode('utf-8')
	
def decode_binary(content):
	if len(content)%8!=0:
		return b''
	byte_len=int(len(content)/8)
	content_hex=b''
	for i in range(0,byte_len):
		bits=content[i*8:(i+1)*8]
		content_hex+=hex(int(bits,base=2))[2:].encode('utf-8')
	return content_hex
	
	
	
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
	


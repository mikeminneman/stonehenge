import binascii
import base64
from unidecode import unidecode
from Crypto.Cipher import DES3
from Crypto.Hash import MD5

def remove_spaces(content): # returns string
	if type(content) == bytes:
		nosp = b''
		for i in range(0,len(content)):
			if content[i:i+1]!=b' ' and content[i:i+1]!=b'\r' and content[i:i+1]!=b'\n' and content[i:i+1]!=b'\t':
				nosp+=content[i:i+1]
		return nosp
	elif type(content) == str:
		return content.replace(" ","").replace("\n","").replace("\r","").replace("\t","")
	return b''
	
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
	
def get_first8(val): # returns value
	return val[:8]

def remove_first8(val): # returns value
	return val[len(val)-8:]
	
#Legacy

def hex2num(text): # returns value
	return decode_hex(text)

def decode_b64(val): # returns value
	return decode_base64(val)
	


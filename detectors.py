import string

def remove_spaces(content): # returns string
	spacechars=' \r\n\t\x04\x05\x08\x02'
	spacebytes=bytes(spacechars,encoding='utf-8')
	if type(content) == bytes:
		nosp = b''
		for i in range(0,len(content)):
			if not(content[i:i+1] in spacebytes):
				nosp+=content[i:i+1]
		return nosp
	elif type(content) == str:
		nosp = b''
		for i in range(0,len(content)):
			if not(content[i:i+1] in spacechars):
				nosp+=content[i:i+1]
		return nosp
	return b''
	
def detect_spaces(content): # returns boolean
	spacechars=' \r\n\t\x04\x05\x08\x02'
	spacebytes=bytes(spacechars,encoding='utf-8')
	if type(content) == bytes:
		nosp = False
		for i in range(0,len(content)):
			if content[i:i+1] in spacebytes:
				nosp = True
				return nosp
		return nosp
	elif type(content) == str:
		nosp = False
		for i in range(0,len(content)):
			if content[i:i+1] in spacechars:
				nosp = True
				return nosp
		return nosp
	return False

def detect_hex(text): # returns boolean
	if type(text) == bytes:
		return all(c in bytes(string.hexdigits,encoding='utf-8') for c in text)
	elif type(text) == str:
		return all(c in string.hexdigits for c in text)
	return False
	
def detect_hex_w_spaces(text):
	return detect_spaces(text) and detect_hex(remove_spaces(text))

def detect_hexlike(text):
	extrachars='#Vv'
	if type(text) == bytes:
		return not(detect_hex(text)) and all(c in bytes(string.hexdigits+extrachars,encoding='utf-8') for c in text)
	elif type(text) == str:
		return not(detect_hex(text)) and all(c in string.hexdigits+extrachars for c in text)

def detect_hexlike_w_spaces(text):
	return detect_spaces(text) and detect_hexlike(remove_spaces(text))
	
def detect_base64(text):
	validchars=string.ascii_letters+string.digits+'+/='
	validbytes=bytes(validchars,encoding='utf-8')
	if type(text) == bytes:
		return len(text)%4==0 and all(c in validbytes for c in text)
	elif type(text) == str:
		return len(text)%4==0 and all(c in validchars for c in text)
	return False

def detect_mult4(text):
	return len(text)%4==0 and len(text)>0
	
def detect_mult8(text):
	return len(text)%8==0 and len(text)>0

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

def detect_utf8end(text):
	return not(detect_utf8(text)) and detect_utf8(remove_first8(text))
	
def get_first8(val): # returns value
	return val[:8]

def remove_first8(val): # returns value
	return b"" if len(val)<8 else val[8:len(val)]


	
	

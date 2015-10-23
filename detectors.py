def detect_spaces(text): # returns boolean
	return (' ' in text)

def detect_hex(text): # returns boolean
	return all(c in string.hexdigits for c in text)

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


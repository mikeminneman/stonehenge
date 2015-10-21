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

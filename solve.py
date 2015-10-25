from detectors import *
from decoders import *

def find_approach(content,l=0):
	nl=l+1
	if l>10:
		print("Too deep.")
		return []
	if type(content)==str:
		content=content.encode('utf-8')
	types = detect(content)	
	methods = lookup_method(types)
	print(str(l)+indent(l)+" Types: "+str(types))
	print(str(l)+indent(l)+" Methods: "+str(methods))
	if methods==[]:
		approach = []
	else:
		for method in methods:
			print(str(l)+indent(l)+" Working with method: "+method)
			if "solved" in method:
				approach = [method]
				break
			else:
				newcontent = decode(content, method)
				if newcontent == b'':
					approach = []
				else:
					newapproach = find_approach(newcontent,nl)
					print(str(l)+indent(l)+" New approach: "+str(newapproach))
					if solvedapproach(newapproach):
						approach = [method]+newapproach
						break
					else:
						approach = [method]+newapproach #does not matter
	print(str(l)+indent(l)+ " Returning: "+str(approach))
	return approach
	
def solve(content, approach):
	if solvedapproach(approach):
		if type(content)==str:
			content=content.encode('utf-8')
		solution = content
		for method in approach:
			solution = decode(solution, method)
	else:
		solution=b""
	return solution
	
def detect(content):
	types = []
	if detect_hex_w_spaces(content):
		types.append("hex_w_spaces")
	if detect_hex(content):
		types.append("hex")
	if detect_hexlike_w_spaces(content):
		types.append("hexlike_w_spaces")
	if detect_hexlike(content):
		types.append("hexlike")	
	if detect_base64(content):
		types.append("base64")
	if detect_utf8(content):
		types.append("utf8")
	if detect_utf8end(content):
		types.append("utf8end")
	if detect_mult8(content):
		types.append("mult8")
	return types

def lookup_method(types):
	methods=[]
	if ("utf8" in types) and not("hexlike_w_spaces" in types) and not("hexlike" in types) and not("hex_w_spaces" in types) and not("hex" in types) and not("base64" in types):
		methods=["solved"]
	elif ("utf8end" in types):
		methods=["solved-neediv"]
	else:
		for type in types:
			if type=="hex_w_spaces" or type=="hexlike_w_spaces":
				methods.append("remove_spaces")
			if type=="hex":
				methods.append("decode_hex")
			if type=="hexlike":
				methods.append("decode_hexlike")
			if type=="base64":
				methods.append("decode_base64")
			if type=="mult8":
				methods.append("decode_des3ecb")
				methods.append("decode_des3ecb_title")
				methods.append("decode_des3cbc")
				methods.append("decode_des3cbc_title")
	return methods
	
def decode(content, method):
	if "solved" in method:
		return content
	if method=="remove_spaces":
		return remove_spaces(content)
	if method=="decode_hex":
		return decode_hex(content)
	if method=="decode_hexlike":
		return decode_hexlike(content)
	if method=="decode_base64":
		return decode_base64(content)
	if method=="decode_des3ecb":
		return decode_des3ecb(content)
	if method=="decode_des3ecb_title":
		return decode_des3ecb_title(content)
	if method=="decode_des3cbc":
		return decode_des3cbc(content)
	if method=="decode_des3cbc":
		return decode_des3cbc_title(content)
	return ""
	
def solvedapproach(approach):
	return len(approach)>0 and ("solved" in approach[len(approach)-1])
	
	
	
	
	
def indent(l):
	indent=""
	for i in range(0,l):
		indent+="\t"
	return indent
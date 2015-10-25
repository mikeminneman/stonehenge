from detectors import *
from decoders import *

def find_approach(content,l=0):
	nl=l+1
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
			if method == "solved":
				approach = ["solved"]
				break
			else:
				newcontent = decode(content, method)
				if newcontent == b'':
					approach = []
				else:
					newapproach = find_approach(newcontent,nl)
					print(str(l)+indent(l)+" New approach: "+str(newapproach))
					if len(newapproach)>0 and newapproach[len(newapproach)-1]=="solved":
						approach = [method]+newapproach
						break
					else:
						approach = [method]+newapproach #does not matter
	print(str(l)+indent(l)+ " Returning: "+str(approach))
	return approach
	
def solve(content, approach):
	if len(approach)>0 and approach[len(approach)-1]=="solved":
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
	if detect_spaces(content):
		types.append("spaces")
	if detect_hex_w_spaces(content):
		types.append("hex_w_spaces")
	if detect_hex_replaced_3A(content):
		types.append("hex_replaced_3A")
	if detect_hex(content):
		types.append("hex")
	if detect_base64(content):
		types.append("base64")
	if detect_utf8(content):
		types.append("utf8")
	return types

def lookup_method(types):
	methods=[]
	if ("utf8" in types) and not("hex_w_spaces" in types) and not("hex" in types) and not("base64" in types):
		methods=["solved"]
	else:
		for type in types:
			if type=="spaces":
				methods.append("remove_spaces")
			if type=="hex_w_spaces":
				methods.append("remove_spaces")
			if type=="hex_replaced_3A":
				methods.append("replace_3A")
			if type=="hex":
				methods.append("decode_hex")
			if type=="base64":
				methods.append("decode_base64")
	return methods
	
def decode(content, method):
	if method=="remove_spaces":
		return remove_spaces(content)
	if method=="decode_hex":
		return decode_hex(content)
	if method=="decode_base64":
		return decode_base64(content)
	if method=="solved":
		return content
	return ""
	
	
	
	
	
	
	
def indent(l):
	indent=""
	for i in range(0,l):
		indent+="\t"
	return indent
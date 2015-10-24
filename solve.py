from detectors import *
from decoders import *

def find_approach(content):
	if type(content)==str:
		content=content.encode('utf-8')
	types = detect(content)	
	methods = lookup_method(types)
	if methods==[]:
		approach = []
	else:
		for method in methods:
			if method == "solved":
				approach = ["solved"]
				return approach
			else:
				newcontent = decode(content, method)
				if newcontent == "":
					approach = []
				else:
					newapproach = find_approach(newcontent)
					if len(newapproach)>1 and newapproach[len(newapproach)-1]=="solved":
						approach = [method]+newapproach
						return approach
					else:
						approach = [method]+newapproach #does not matter
	return approach
	
def solve(content, approach):
	if type(content)==str:
		content=content.encode('utf-8')
	solution = content
	for method in approach:
		solution = decode(solution, method)
	return solution
	
def detect(content):
	if detect_hex_w_spaces(content):
		return ["hex_w_spaces"]
	return []

def lookup_method(types):
	methods=[]
	for type in types:
		if type=="hex_w_spaces":
			methods.append("remove_spaces")
	return methods
	
def decode(content, method):
	if method=="remove_spaces":
		return remove_spaces(content)
	return ""
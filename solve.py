from detectors import *
from decoders import *

def find_approach(content):
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
					newapproach = append(find_method(newcontent))
					if newapproach[len(newapproach)-1]=="solved":
						approach = [method].append(newapproach)
						return approach
					else:
						approach = [method].append(newapproach) #does not matter
	return approach
	
def solve(content, approach):
	return ""
	
def detect(content):
	return []

def lookup_method(types):
	return []
	
def decode(content, method):
	return ""
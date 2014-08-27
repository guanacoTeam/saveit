from siNode import *
from siSet import *

def getJson_nice(object, depth = 0):
	'''
	Returns object encoded to json
	Returnable string not so nice, but possible to read
	'''
	if type(object) == str:
		return "'" + object + "'"
	elif type(object) in [int, float]:
		return str(object)
	elif type(object) in [list, set]:
		return "[" + ", ".join([getJson_nice(elem, depth + 2) for elem in object]) + "]"
	elif type(object) == dict:
		return "{\n" + (" " * depth) + (",\n" + " " * depth).join(["'" + key + "': " + getJson_nice(object[key], depth + 2) for key in object]) + "\n" + " " * (depth) + "}\n"
	else:
		return "{\n" + (" " * depth) + (',\n' + " " * depth).join(["'" + key + "': " + getJson_nice(getattr(object, key), depth + 2) for key in vars(object)]) + "\n" + " " * (depth) + "}\n"

def getJson(object):
	'''
	Returns object encoded to json
	Returnable string not containes symbols like " ", "\\n"
	'''
	if type(object) == str:
		return "'" + object + "'"
	elif type(object) in [int, float]:
		return str(object)
	elif type(object) == list:
		return "[" + ", ".join([getJson(elem) for elem in object]) + "]"
	elif type(object) == set:
		if object == set():
			return "set()"
		else:
			return "{" + ", ".join([getJson(elem) for elem in object]) + "}"
	elif type(object) == dict:
		return "{" + ",".join(["'" + key + "':" + getJson(object[key]) for key in object]) + "}"
	else:
		return "{" + ','.join(["'" + key + "':" + getJson(getattr(object, key)) for key in vars(object)]) + "}"

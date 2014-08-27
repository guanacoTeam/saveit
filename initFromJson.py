from siCore import *

def initFromJson(json):
	'''
	Returns object with type equals to "ftype" in json
	Works with siNode, siSet
	'''
	d = eval(json)
	if d.get("ftype") == "siNode":
		return siNode("", d)
	elif d.get("ftype") == "siSet":
		elems = d["elems"]
		for id in elems:
			elems[id] = siNode("", elems[id])
		d.pop("elems")
		return siSet(elems, d)
	return None
from siNode import *


class siSet:

	'''
	Basic class for siObjects, siTags. Contains siNode-s
	'''

	def __init__(self, elems = {}, *props, **kprops):
		'''
		"elems" - dictionary, where key is siNode.id and value is siNode

		"ftype" - formal type, just name of class
		'''
		self.elems = elems
		self.ftype = "siSet"
		for dprop in props:
			if type(dprop) == dict:
				for prop in dprop:
					setattr(self, prop, dprop[prop])
		for prop in kprops:
			setattr(self, prop, kprops[prop])

	def getElems(self):
		'''
		Returns sorted by id list of siNode-s from "elems"
		'''
		return sorted(self.elems.values())

	def addElem(self, elem):
		'''
		Adds siNode "elem"
		Returns False if "elem" is already in "elems", True otherwise
		'''
		if elem.id in self.elems:
			return False
		self.elems[elem.id] = elem
		return True

	def delElem(self, elemID):
		'''
		Deletes siNode with id equals to "elemID"
		Returns False if there is no elemID in elems keys
		'''
		if elemID not in self.elems:
			return False
		self.elems.pop(elemID)
		return True

	def addAttrToElem(self, attr, elemID):
		'''
		Calls function "addAttr" of siNode with id equals to "elemID"
		If there is no siNode if elems with id "elemID" returns False
		'''
		if elemID not in self.elems:
			return False
		return self.elems[elemID].addAttr(attr)

	def delAttrFromElem(self, attr, elemID):
		'''
		Calls function "delAttr" of siNode with id equals to "elemID"
		If there is no siNode if elems with id "elemID" returns False
		'''
		if elemID not in self.elems:
			return False
		return self.elems[elemID].delAttr(attr)

	def union(self, other):
		'''
		Returns union of siSet-s "self", "other"
		'''
		return siSet(dict(set(self.elems.items()) | set(other.elems.items())))

	def intersection(self, other):
		'''
		Returns intersection of siSet-s "self", "other"
		'''
		return siSet(dict(set(self.elems.items()) & set(other.elems.items())))

	def difference(self, other):
		'''
		Returns difference of siSet-s "self", "other"
		'''
		return siSet(dict(set(self.elems.items()) - set(other.elems.items())))

	def symmetric_difference(self, other):
		'''
		Returns symmetric difference of siSet-s "self", "other"
		'''
		return siSet(dict(set(self.elems.items()) ^ set(other.elems.items())))

	def __or__(self, other):
		return siSet(dict(set(self.elems.items()) | set(other.elems.items())))

	def __and__(self, other):
		return siSet(dict(set(self.elems.items()) & set(other.elems.items())))

	def __iand__(self, other):
		self.elems = dict(set(self.elems.items()) & set(other.elems.items()))

	def __sub__(self, other):
		return siSet(dict(set(self.elems.items()) - set(other.elems.items())))

	def __isub__(self, other):
		self.elems = dict(set(self.elems.items()) - set(other.elems.items()))

	def __xor__(self, other):
		return siSet(dict(set(self.elems.items()) ^ set(other.elems.items())))

	def __ixor__(self, other):
		self.elems = dict(set(self.elems.items()) ^ set(other.elems.items()))

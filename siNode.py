class siNode:

	'''
	Basic class for siObject, siTag
	'''

	def __init__(self, id = "_noname_", *props, **kprops):
		'''
		"id" - identification for object, _noname_ by default
		"attrs" - set of attributes, empty by default
		"props", "kprops" - dictionaries of properties
		"ftype" - formal type, just name of class
		'''
		self.id = id
		self.attrs = set()
		self.ftype = "siNode"
		for dprop in props:
			if type(dprop) == dict:
				for prop in dprop:
					setattr(self, prop, dprop[prop])
		for prop in kprops:
			setattr(self, prop, kprops[prop])

	def addAttr(self, attr):
		'''
		Adds attribute "attr" into "attrs"
		Returns False if "attr" is already in "attrs", True otherwise
		'''
		if attr in self.attrs:
			return False
		self.attrs.add(attr)
		return True

	def delAttr(self, attr):
		'''
		Deletes attribute "attr" from "attrs"
		Returns False if there is nothing to delete, True otherwise
		'''
		if attr not in self.attrs:
			return False
		self.attrs.remove(attr)
		return True

	def __lt__(self, other):
		'''
		Compares by "id"
		'''
		return self.id < other.id

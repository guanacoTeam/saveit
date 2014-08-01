from siNode import *
from siSet import *
from getJson import *
from initFromJson import *

TYPES = {"siNode": siNode, "siSet": siSet}

if __name__ == "__main__":
	s = siSet()
	s.addElem(siNode("n1", type="siObject"))
	s.addElem(siNode("n2", type="siObject"))
	s.addElem(siNode("n3", type="siObject"))
	s.addElem(siNode("n4", type="siObject"))
	print "NICE"
	print getJson_nice(s)
	print "SIMPLE"
	print getJson(s)

	t = getJson(s)
	t = initFromJson(t)
	print getJson(t)
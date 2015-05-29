from ctypes import *
import requests
import kerberos

import sys, atexit, getopt, os
import urlparse, httplib, json, urllib
import getpass, base64
import hashlib, mimetypes, gzip, tempfile
import xml.etree.ElementTree as ET
import webbrowser
from BaseHTTPServer import *


def md5(f):
	"""
	md5(f) -> md5sum
	Counts md5 hash sum of the file with path f
	"""
	fi = open(f, 'rb')
	out = hashlib.md5()
	char = fi.read(1)
	while char != '':
		out.update(char)
		char = fi.read(1)
	fi.close()
	return out.hexdigest()


def sha256(f):
	"""
	sha256(f) -> sha256sum
	Counts sha256 hash sum of the file with path f
	"""
	fi = open(f, 'rb')
	out = hashlib.sha256()
	char = fi.read(1)
	while char != '':
		out.update(char)
		char = fi.read(1)
	fi.close()
	return out.hexdigest()

#Neon init
neon = CDLL("libneon.so")
if neon.ne_sock_init():
	sys.stderr.write("WARNING!!!\nGlobal neon error has been occured.\n")
	sys.exit(-1)
atexit.register(neon.ne_sock_exit)
#prototypes of callbacks
NeAuth = CFUNCTYPE(c_int, c_void_p, c_char_p, c_int, c_char_p, c_char_p)
NePropView = CFUNCTYPE(None, c_void_p, c_void_p, c_void_p)
NePropIter = CFUNCTYPE(c_int, c_void_p, c_char_p, c_void_p)
NeCertVer = CFUNCTYPE(c_int, c_void_p, c_int, c_void_p)

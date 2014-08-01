#!/usr/bin/python
import sys, os, urllib, mimetypes
from siCore import *
import guanaco.webdav
import multiprocessing


def run(arg):
	session, args, kargs = arg[0]
	res = session.run(args, kargs, inter = False)
	#return session.run(arg, kargs, inter = False) if arg[1]['do'] else arg[1]['default']
	if arg[1].get('do', True):
		return res
	else:
		return arg[1].get('default')


class siSession(guanaco.webdav.webDAV):
	"""
	interface for SaveIt application.
	"""
	__id = '5133bf48714e4a3da5973000cd1e1397'  # id of SaveIt.dev
	__secret = 'b28d9d937c6e46c9b4f95da4f7b68903'  # its secret
	#clouds
	spaceHost = 'webdav.yandex.ru'
	#for debug
	#spaceHost = 'localhost:8180'

	def __init__(self, **args):
		"""
		siSession.__init__(inp = <file-obj>, out = <file-obj>, err = <file-obj>, oauth = <boolean>, SaveIt = <boolean>, login = <str>, password = <str>)
		Constructor. Have only key arguments:
		inp -- file-like object to read from it
		out -- file-like object to write to it
		err -- file-like object to write errors to it
		oauth -- True if oauth2 should be used, False otherwise (default).
		SaveIt -- True if SaveIt app should be started (default), False otherwise.
		verbose -- True if debug information should be written to err, False otherwise (default).
		login -- string with login
		password -- string with password

		This method start SaveIt app:
		1) adds 'siFile/config' MIME type fo .si extension
		2) finds or create /SaveItDir at server
		3) finds or create /SaveItDir/files.si and /SaveItDir/tags.si
		4) builds siSets self.files and self.tags
		"""
		guanaco.webdav.webDAV.__init__(self, **args)
		mimetypes.add_type('siFile/config', '.si')  # adds siFile/config MIME type
		#looks for /SaveItDir, /SaveItDir/files.si and /SaveItDir/tags.si
		cont = self.listDir('SaveItDir')
		if not cont:  # magic code. True if SaveItDir not exists
			self.mkcol('SaveItDir')
		if not cont and len([i for i in xrange(len(cont)) if cont[i]['href']
				 == '/SaveItDir/files.si']) == 0:  # True if files.si not exists
			toRunF = [[self, ['upload', getJson(siSet())], {'fromString':True}], {'do' : False, 'default' : getJson(siSet())}]
		else:
			toRunF = [[self, ['download', 'SaveItDir/files.si'], {'toString':True}], {}]
		if not cont and len([i for i in xrange(len(cont)) if cont[i]['href']
				== '/SaveItDir/tags.si']) == 0:  # True if tags.si not exists
			toRunT = [[self, ['upload', getJson(siSet())], {'fromString':True}], {'do' : False, 'default' : getJson(siSet())}]
		else:
			toRunT = [[self, ['download', 'SaveItDir/tags.si'], {'toString':True}], {}]
		pool = multiprocessing.Pool(10)
		l = pool.map(run, [toRunF, toRunT])
		self.files = initFromJson(l[0])
		self.tags = initFromJson(l[1])

	def addFile(self, path, *args, **kargs):
		"""
		addFile('path/to/f'[, mime = 'text/plain', remote = False]) -> boolean of result
		Adds f to application ( uploads or copies to SaveItDir ).
		Set remote to True if f is remote file. By default f is local file.
		Returns True if f has been added, False otherwise.
		"""
		#parses location of file
		fromString = kargs.get('fromString', False)
		local = not kargs.get('remote', False)
		mimeT = kargs.get('mime', mimetypes.guess_type(path)[0])  # tries to guess mime type
		group = kargs.get('group', False)
		if mimeT == None:  # if failed it will be mean, that file has no .ext
			mimeT = 'text/plain'  # if file has no .ext it is text file
		tTag, smth = mimeT.split('/')
		#parse props for siNode 
		name = os.path.basename(path)
		href = '/SaveItDir/' + urllib.quote(name)
		if self.files.addElem(siNode(id = name, href = href, type = mimeT)):  # if siNode has been added
			if fromString:
				self.upload(args[0], 'SaveItDir/' + path, fromString = True)
			elif local:
				self.upload(path, 'SaveItDir')
			else:
				self.copy(path, 'SaveItDir/')
			if tTag == 'application':
				if 'vnd' in smth or smth or {'msword', 'pdf', 'ps', 'rtf', 'x-dvi'}:
					tTag = 'doc' 
			self.tagFile(name, tTag, group = group)
			return True
		else:
			return False

	def delFile(self, f, **kargs):
		"""
		delFile('name')
		Deletes file f from SaveItDir.
		"""
		group = kargs.get('group', False)
		for tag in self.files.elems[f].attrs:  # deletes f from attrs of its tags
			self.tags.delAttrFromElem(f, tag)
		self.files.delElem(f)
		self.delete('SaveItDir/' + f)
		if not group:
			self.update()

	def delTag(self, tag, **kargs):
		"""
		delTag('tag')
		Deletes #tag from database.
		"""
		group = kargs.get('group', False)
		for f in self.tags.elems[tag].attrs:  # deletes #tag from attrs of its files
			self.files.delAttrFromElem(tag, f)
		self.tags.delElem(tag)
		if not group:
			self.update()

	def untagFile(self, f, tag, **kargs):
		"""
		untagFile('name', 'tag')
		Disconnects #tag and f, if they were connected earlier, do nothing otherwise
		"""
		group = kargs.get('group', False)
		self.files.delAttrFromElem(tag, f)
		self.tags.delAttrFromElem(f, tag)
		if not group:
			self.update()

	def listTags(self, **kargs):
		"""
		listTags([file = 'name'])
		Lists tags connected with f, if file argument is set, all tags otherwise.
		"""
		f = kargs.get('file')
		out = self.tags.elems.keys() if f is None else list(self.files.elems[f].attrs)
		if kargs.get('inter', False):
			self.out.write('\n'.join(out) + '\n')
		else:
			return out

	def listFiles(self, **kargs):
		"""
		listFiles([tag = 'tag'])
		Lists files connected with #tag, if tag argument is set, all files otherwise.
		"""
		tag = kargs.get('tag')
		out = self.files.elems.keys() if tag is None else list(self.tags.elems[tag].attrs)
		if kargs.get('inter', False):
			self.out.write('\n'.join(out) + '\n')
		else:
			return out

	def addTag(self, tag, **kargs):
		"""
		addTag('tag')
		Adds #tag tag to tag database.
		"""
		group = kargs.get('group', False)
		if self.tags.addElem(siNode(id = tag)):
			if not group:
				self.updateTags()
			return True
		else:
			return False

	def tagFile(self, f, tag, **kargs):
		"""
		tagFile(f, tag)
		Tag file f with #tag.
		f should exists and #tag may axists.
		"""
		group = kargs.get('group', False)
		if f in self.files.elems:
			self.files.elems[f].addAttr(tag)
			if tag not in self.tags.elems:
				self.addTag(tag)
			self.tags.elems[tag].addAttr(f)
			if not group:
				self.update()

	def updateFiles(self, **kargs):
		"""
		updates files database in files.si file
		"""
		self.upload(getJson(self.files), 'SaveItDir/files.si', fromString = True)

	def updateTags(self, **kargs):
		"""
		updates tags database in tags.si file
		"""
		self.upload(getJson(self.tags), 'SaveItDir/tags.si', fromString = True)

	def update(self):
		"""
		updates both tags.si and files.si files.
		Should be called after every SaveIt opperation.
		"""
		pool = multiprocessing.Pool(10)
		toRunF = [[self, ['updateFiles'], {}], {}]
		toRunT = [[self, ['updateTags'], {}], {}]
		pool.map(run, [toRunF, toRunT])

	@staticmethod
	def getId(self):
		"""
		return id of app
		"""
		return siSession.__id

	@staticmethod
	def __getSecret(self):
		"""
		return secret od app
		"""
		return siSession.__secret

	def getToken(self):
		"""
		return your access token ( only for oauth2 protocol )
		"""
		return self.token

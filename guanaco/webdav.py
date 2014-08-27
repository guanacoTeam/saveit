#!/usr/bin/python
"""
Flags:
-i file -- read from file-like object file
-o file -- write to file-like object file
-e file -- write errors to file-like object file
-v -- make client verbose
--oauth -- force client to use ouath2 protocol to authorization. Not recomended.
"""
# -*- coding : utf8 -*-
import sys, getopt, os
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


class webDAV:
	"""
	full WebDAV client.
	"""
	#clouds
	spaceHost = 'webdav.yandex.ru'
	#for debug
	#spaceHost = 'localhost:8180'

	def __init__(self, **args):
		"""
		webDAV.__init__(inp = <file-obj>, out = <file-obj>, err = <file-obj>, verbose = <boolean>, oauth = <boolean>, login = <str>, password = <str>)
		Constructor. Have only key arguments:
		inp -- file-like object to read from it
		out -- file-like object to write to it
		err -- file-like object to write errors to it
		oauth -- True if oauth2 should be used, False otherwise (default).
		verbose -- True if debug information should be written to err, False otherwise (default).
		login -- string with login
		password -- string with password
		"""
		#From this starts parsing of the arguments
		self.inp = args.get('inp', sys.stdin)
		self.out = args.get('out', sys.stdout)
		self.err = args.get('err', sys.stderr)
		self.oauth = args.get('oauth', False)
		self.verbose = args.get('verbose', False)
		self.authHeader = args.get('authHeader', '')
		self.user = args.get('login')
		passwd = args.get('password')
		#End of parsing
		self.login(oauth = self.oauth, login = self.user, password = passwd)

	def login(self, **kargs):
		"""
		login([login = <str>, password = <str>, authHeader = <str>])
		Sets self.authHeader, which is string used as value of 'Authorization' header.
		You can login from authHeader if you have one, or with login, password pair (dict).
		With empty arguments will start two dialogs to build self.authHeader.
		In all cases you can set oauth = True to use oauth2 protocol.
		"""
		user = kargs.get('login')
		passwd = kargs.get('password')
		oauth = kargs.get('oauth', False)
		if len(self.authHeader) == 0:
			if oauth:  # Try to use ouath protocol
				webbrowser.open_new('https://oauth.yandex.ru/authorize?response_type=code&client_id=' + self.getId())
				code = self.catchCode()
				req = dict()
				req['Content-type'] = 'application/x-www-form-urlencoded'
				gateway = httplib.HTTPSConnection('oauth.yandex.ru')
				gateway.request('POST', '/token', body = 'grant_type=authorization_code&code=%s&client_id=%s&client_secret=%s' % (code, self.getId(), self.__getSecret()))
				self.token = getaway.getresponse().read()["access_token"]
				self.authHeader = "OAuth " + self.token
			else:
				if user is None:  # if login argument isn't passed to constructor, try to take it from dialog
					self.out.write('Login: ')
					user = self.inp.readline()[:-1]
				if passwd is None:  # if password argument isn't passed to constructor, try to take it from dialog
					passwd = getpass.getpass(stream = self.out)
				self.authHeader = "Basic " + base64.encodestring(user + ':' + passwd).rstrip()  # make authHeader

	def catchCode(self):
		"""
		catchCode() -> oauth2 code
		Catches oauth2 code.
		See http://api.yandex.ru/oauth/doc/dg/reference/obtain-access-token.xml for more info
		"""
		class Server(HTTPServer):
			def __init__(self, *args):
				HTTPServer.__init__(self, *args)
				self.code = 0
		class Handler(BaseHTTPRequestHandler):
			def do_GET(self):
				self.send_response(200, 'OK')
				self.server.code = int(urlparse.parse_qs(urlparse.urlsplit(self.path).query)['code'][0])
		httpd = Server(('localhost.localdomain', 8179), Handler)
		httpd.handle_request()
		return httpd.code

	def run(self, arg, kargs = {}, inter = True):
		"""
		run(arg)
		Runs commands.
		For example self.run(['listDir', 'myCol']) will be parsed to self.listDir('myCol', inter = True)
		"""
		if len(arg) != 0:
			func = arg[0]  # first of all comes function name
			arg.pop(0)
			if len(arg) > 0 and not os.path.isfile(arg[-1]):  # last one comes remote path but not always
				path = arg[-1]
				arg.pop()
			else:
				path = ''
			if self.verbose and not self.err.closed:
				self.err.write(str(path) + '\n')
			if len(arg) > 0:  # if there is any another arguments function should be called separately
				for f in arg:
					com = 'self.%s("%s", %s' % (func, f, '\'' + path + '\', ' if path != '' else '')
					for item in kargs.items():
						com += str(item[0]) + ' = ' + str(item[1]) + ', '
					com += 'inter = ' + str(inter) + ')'
					if self.verbose:
						self.err.write(com + '\n')
					com = 'r = ' + com
					exec(com)
			else:
				com = 'self.%s(%s' % (func, '"' + path + '", ' if path != '' else '')
				for item in kargs.items():
					com += str(item[0]) + ' = ' + str(item[1]) + ', '
				com += 'inter = ' + str(inter) + ')'
				if self.verbose:
					self.err.write(com + '\n')
				com = 'r = ' + com
				exec(com)
			return r

	def listDir(self, *args, **kargs):
		"""
		listDir('remote/path'[, inter = False]) -> content of /remote/path
		List content /remote/path.
		If /remote/path is collection 'content' is files and collection located in it, /remote/path object otherwise.
		If inter = True plain list of content will be written to self.out 'one-by-line',
		list of dictionaries with 'hame', 'mime' and 'href' fields will be returned otherwise.
		For elem in result:
		elem['name'] is display name
		elem['href'] is absolute path in the server
		elem['type'] is MIME type of elem
		"""
		path = args[0] if len(args) > 0 else '/'  # parse remote path from the args
		if path[0] != '/':  # path should be start from /
			path = '/' + path
		if path[-1] != '/':  # and ends to /
			path += '/'
		inter = kargs.get('inter', False)
		gateway = httplib.HTTPSConnection(self.spaceHost)  # connect to spaceHost
		method = 'PROPFIND'  # use PROPFIND WebDAV method
		headers = dict()  # init headers
		headers['Authorization'] = self.authHeader  # Authorization, used to recognized user by server
		headers['Depth'] = '1'  # Depth
		headers['Accept'] = '*/*'  # Accept. This and Depth headers should set as they set now, otherwise raised error
		gateway.request(method, urllib.quote(path), headers = headers)  # send request to the spaceHost
		response = gateway.getresponse()  # and take response
		if response.status == 401:
			self.err.write('User. U make this bug. U have to debug.\nPls, write tru password next time.\n')
			self.err.flush()
			raise FloatingPointError
		root = ET.parse(response).getroot()  # as XML doc, so it should be parsed
		gateway.close()  # close connection
		obj = dict()  # start to build "preview" of first object
		obj['href'] = root[0].find('{DAV:}href').text
		prop = root[0][1][1]
		obj['name'] =  prop.find('{DAV:}displayname').text
		if prop.find('{DAV:}getcontenttype') is None:
			obj['mime'] = 'collection/directory'
		else:
			obj['mime'] = prop.find('{DAV:}getcontenttype').text
		if obj['mime'] == 'collection/directory':  # if first object is collection it shouldn't be displayed
			contents = list()
		else:
			contents = [obj]
		for response in root[1:]:  # all other objects should be displayed
			obj = dict()
			obj['href'] = response.find('{DAV:}href').text
			prop = response[1][1]
			obj['name'] =  prop.find('{DAV:}displayname').text
			if prop.find('{DAV:}getcontenttype') is None:
				obj['mime'] = 'collection/directory'
			else:
				obj['mime'] = prop.find('{DAV:}getcontenttype').text
			contents.append(obj)
		if inter:  # if inter write result to self.out
			for obj in contents:
				self.out.write(obj['name'] + '\n')
		else:
			return contents

	def download(self, *args, **kargs):
		"""
		download('remote/path/to/f', 'local/path'[, toString = False])
		Downloads file from remote/path/to/f as local/path/f.
		If toString = True content of remote/path/to/f will be returned as string.
		"""
		toString = kargs.get('toString', False)
		remote = args[0]  # parse remote path
		if remote[0] != '/':  # path should be start from '/'
			remote = '/' + remote
		if not toString:
			path = args[1]  if len(args) > 1 else '.'  # parse local path
			if os.path.isdir(path) and path[-1] != '/':  # path should ends to '/'
				path += '/'
		inter = kargs.get('inter', False)
		gateway = httplib.HTTPSConnection(self.spaceHost)  # connect to spaceHost
		method = 'GET'  # use GET WebDAV method
		headers = dict()  # init headers
		headers['Authorization'] = self.authHeader  # Authorization header
		headers['Accept'] = '*/*'  # Accept header. Should be '*/*'
		if self.verbose and not toString:  # if verbose, verbose about file
			self.err.write(path + os.path.basename(remote) + '\n')
		gateway.request(method, urllib.quote(remote), headers = headers)  # send request to server
		response = gateway.getresponse() # and get response
		if self.verbose: # and, of course, verbose about it
			self.err.write(str(response.status) + ' ' + str(response.reason) + '\n')
			if response.status == 200:  # 200 is OK status in our case
				self.err.write('Done' + '\n')
		if toString:
			down = response.read()
		else:
			fo = open(path + os.path.basename(remote), 'wb')
			fo.write(response.read())
			fo.close()
		response.close()
		gateway.close()
		if toString:
			return down

	def upload(self, *args, **kargs):
		"""
		upload('local/path/to/f', 'remote/path'[, fromString = False])
		Uploads file from local/path/to/f as remote/path/f.
		If fromString = True first argument will be uploaded as remote/path.
		"""
		if self.verbose:
			self.err.write('self.upload(%s)\n' % ', '.join(args))
		f = args[0]  # parse local path
		path = args[1]  if len(args) > 1 else '/'  # parse remote path
		if path[0] != '/':  # path should be start from '/'
			path = '/' + path
		if os.path.exists(f) and path[-1] != '/':  # and ends to '/', if it is path to collextion
			path += '/'
		inter = kargs.get('inter', False)
		mimeT = kargs.get('mime')
		fromString = kargs.get('fromString', False)
		gateway = httplib.HTTPSConnection(self.spaceHost)  # connect to spaceHost
		method = 'PUT'  # use PUT WebDAV method
		headers = dict()  # init headers
		headers['Authorization'] = self.authHeader  # Authorization header
		headers['Accept'] = '*/*'  # Accept header. Should be '*/*'
		if not fromString:
			headers['Etag'] = md5(f)  # md5 sum of file
			headers['Sha256'] = sha256(f)  # sha256 sum of file
			if mimeT is None:
				mimeT = mimetypes.guess_type(f)[0]  # tries to guess mime type
				if mimeT == None:  # if failed it will be mean, that file has no .ext
					mimeT = 'text/plain'  # if file has no .ext it is text file
			headers['Content-Type']  = mimeT
			#headers['Transfer-Encoding'] = 'chunked'
			headers['Content-Length'] = os.path.getsize(f)  # count the size of file
			if self.verbose:  # if verbose, verbose about file
				self.err.write(path + os.path.basename(f) + '\n')
				self.err.write(md5(f) + '\n')
				self.err.write(sha256(f) + '\n')
			#send file to server
			fi = open(f, 'rb')
			gateway.request(method, urllib.quote(path + os.path.basename(f)), body = fi.read(), headers = headers)
			fi.close()
		else:
			f = str(f)
			md5sum = hashlib.md5(f).hexdigest()  # md5 sum of file
			headers['Etag'] = md5sum
			sha256sum = hashlib.sha256(f).hexdigest()  # sha256 sum of file
			headers['Sha256'] = sha256sum
 			if mimeT is None:
				mimeT = mimetypes.guess_type(path)[0]  # tries to guess mime type
				if mimeT == None:  # if failed it will be mean, that file has no or unknown .ext suffix
					mimeT = 'text/plain'  # if file has no .ext it is text file
			headers['Content-Type']  = mimeT
			#headers['Transfer-Encoding'] = 'chunked'
			headers['Content-Length'] = len(f)  # count the size of file
			if self.verbose:  # if verbose, verbose about file
				self.err.write(path + '\n')
				self.err.write(md5sum + '\n')
				self.err.write(sha256sum + '\n')
			gateway.request(method, urllib.quote(path), body = f, headers = headers)  # send file to server
		response = gateway.getresponse() # and get response
		if self.verbose: # and, of course, verbose about it
			self.err.write(str(response.status) + ' ' + str(response.reason) + '\n')
		if response.status == 201:  # 201 is OK status in our case
			if not self.err.closed:
				self.err.write('Done' + '\n')
		response.close()
		gateway.close()

	def copy(self, *args, **kargs):
		"""
		copy('remote/path/to/f', 'another/location/path')
		Copies file from remote/path/to/f to another/location/path/.
		"""
		f = args[0]  # parse source path
		if f[0] != '/':  # path should start with '/'
			f = '/' + f
		path = args[1]  if len(args) > 1 else '/'  # parse destination path
		if path[0] != '/':  # path should start with '/'
			path = '/' + path
		if f[-1] != '/':
			path += '/' if path[-1] != '/' else ''
			path += os.path.basename(f)
		inter = kargs.get('inter', False)
		gateway = httplib.HTTPSConnection(self.spaceHost)  # connect to spaceHost
		method = 'COPY'  # use COPY WebDAV method
		headers = dict()  # init headers
		headers['Authorization'] = self.authHeader  # Authorization header
		headers['Accept'] = '*/*'  # Accept header. Should be '*/*'
		headers['Destination'] = path  # Destination header
		gateway.request(method, urllib.quote(f), headers = headers)  # send file to server
		response = gateway.getresponse() # and get response
		if self.verbose: # and, of course, verbose about it
			self.err.write(str(response.status) + ' ' + str(response.reason) + '\n')
		if response.status == 201:  # 201 is OK status in our case
			self.err.write('Done' + '\n')
		response.close()
		gateway.close()

	def mkcol(self, path, inter = False):
		"""
		mkcol('path/to/new/directory/col')
		Makes collection col in server at /path/to/new/directory which exist.
		"""
		if path[0] != '/':  # path should start with /
			path = '/' + path
		if path[-1] != '/':  # and ends to /
			path += '/'
		gateway = httplib.HTTPSConnection(self.spaceHost)  # connect to spaceHost
		method = 'MKCOL'  # use MKCOL WebDAV method
		headers = dict()  # init headers
		headers['Authorization'] = self.authHeader  # Authorization header
		headers['Accept'] = '*/*'  # Accept header. Should be '*/*'
		if self.verbose:  # if verbose, verbose about file
			self.err.write(path + '\n')
		gateway.request(method, urllib.quote(path), headers = headers)  # send file to server
		response = gateway.getresponse() # and get response
		if self.verbose: # and, of course, verbose about it
			self.err.write(str(response.status) + ' ' + str(response.reason) + '\n')
		if response.status == 201:  # 201 is OK status in our case
			self.err.write('Done' + '\n')
		response.close()
		gateway.close()

	def delete(self, path, inter = False):
		"""
		delete('path/to/new/directory/col')
		Deletes /path/to/smth.
		"""
		if path[0] != '/':  # path should start with /
			path = '/' + path
		gateway = httplib.HTTPSConnection(self.spaceHost)  # connect to spaceHost
		method = 'DELETE'  # use DELETE WebDAV method
		headers = dict()  # init headers
		headers['Authorization'] = self.authHeader  # Authorization header
		headers['Accept'] = '*/*'  # Accept header. Should be '*/*'
		if self.verbose:  # if verbose, verbose about file
			self.err.write(path + '\n')
		gateway.request(method, urllib.quote(path), headers = headers)  # send file to server
		response = gateway.getresponse() # and get response
		if self.verbose: # and, of course, verbose about it
			self.err.write(str(response.status) + ' ' + str(response.reason) + '\n')
		if response.status == 200:  # 200 is OK status in our case
			self.err.write('Done' + '\n')
		response.close()
		gateway.close()

	def getId(self):
		"""
		return id of app
		"""
		return 0

	def __getSecret(self):
		"""
		return secret od app
		"""
		return 0

	def getToken(self):
		"""
		return your access token ( only for oauth2 protocol )
		"""
		return self.token

	def getDisk(self):
		"""
		return adress of cloud
		"""
		return self.spaceHost


if __name__ == '__main__':  # this part of program exec only if webDAV runs from terminal, konsole, cmd, etc.
	longopts = ['oauth', 'verbose']  # long flags with two minuses
	optlist, arg = getopt.gnu_getopt(sys.argv[1:], 'vi:o:e:', longopts)  # parse flags
	optlist = dict(optlist)  # make from optlist a dict
	#parse streams names from optlist
	inpName = optlist.get('-i', None)
	outName = optlist.get('-o', None)
	errName = optlist.get('-e', None)
	#parse other flags
	oauth = True if '--oauth' in optlist.keys() else False
	verbose = True if '--verbose' in optlist.keys() or '-v' in optlist.keys() else False
	#get streams to read, write and errors
	inp = open(inpName) if not (inpName is None) else sys.stdin
	out = open(outName, 'w') if not (outName is None) else sys.stdout
	err = open(errName, 'w') if not (errName is None) else sys.stderr
	#make webDAV instance
	ses = webDAV(inp = inp, out = out, err = err, oauth = oauth, verbose = verbose)
	#run command
	ses.run(arg)

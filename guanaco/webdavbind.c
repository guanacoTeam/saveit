#include<Python.h>
#include<structmember.h>
#include<ne_socket.h>
#include<ne_utils.h>
#include<ne_session.h>
#include"getpass.h"

static int status;

//webDAV class
//Don't worry if it isn't working. It is normal state
typedef struct {
	PyObject_HEAD
	//self.inp = args.get('inp', sys.stdin)
	//self.out = args.get('out', sys.stdout)
	//self.err = args.get('err', sys.stderr)
	long int oauth; //oauth flag
	long int verbose; //verbosity flag
	size_t authL; //authHeader length
	char *authHeader; //authHeader
	size_t userL; //username length
	char *user; //username
	size_t spaceL; //cloud address length
	char *spaceHost; //cloud address
	ne_session *neonSes; //neon session
} webDAV;

static int webDAV_init(webDAV *self, PyObject *args, PyObject *kwds) {
	int passL = 0;
	char *password = NULL;
	char *kwlist[] = {"verbose", "oauth", "authHeader", "login"};
	self->oauth = 0L;
	self->verbose = 0L;
	self->authL = 0;
	self->authHeader = "";
	self->userL = 0;
	self->user = "";
	self->spaceL = 17;
	self->spaceHost = "webdav.yandex.ru";
	self->neonSes = NULL;
	//passwd = args.get('password')
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiz#z#z#", kwlist, 
				&self->verbose, &self->oauth, &self->authHeader,
				&self->authL, &self->user, &self->userL, &password, &passL))
		return -1;
	if (!status && ne_sock_init()) { //trying to init neon
		printf("%d\n", status);
		perror("Global neon error!");
		exit(-1);
	}
	++status;
	//End of parsing
	//Init of all
	//self->
	//self.login(oauth = self.oauth, login = self.user, password = passwd)
	//webDAV_login(self, Py_BuildValue("{s:s, s:}"))
	return 0;
}

static int webDAV_login(webDAV *self , char *user, size_t userL, char *password, size_t passL) {
	//TODO
	getpasswd(&user, &userL, &password, &passL);
	return 1;
}

static PyObject *webDAV_PyLogin(webDAV *self, PyObject *args, PyObject *kwds) {
	int oauth = 0;
	size_t userL = 0, passL = 0;
	char *user = "", *password = "";
	char *kwlist[] = {"oauth", "login", "password"};
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iz#z#", kwlist, &oauth, &user, &userL, &password, &passL)) {
		return NULL;
	}
	if (!oauth)
		if (webDAV_login(self, user, userL, password, passL))
			Py_RETURN_TRUE;
		else
			Py_RETURN_FALSE;
	else {
		fprintf(stderr, "Oauth2 protocol is not implemented yet!\n");
		Py_RETURN_NONE;
	}
}

static PyObject *webDAV_catchCode(webDAV *self) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_run(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_listDir(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_download(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_upload(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_copy(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_mkcol(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_delete(webDAV *self, PyObject *arg, PyObject *kwds) {
	Py_RETURN_NONE;
}

static PyObject *webDAV_verbose(webDAV *self) {
	return PyBool_FromLong(self->verbose);
}

static PyObject *webDAV_getId(webDAV *self) {
	return Py_BuildValue("i", 0);
}

static PyObject *webDAV_getSecret(webDAV *self) {
	return Py_BuildValue("i", 0);
}

static void webDAV_dealloc(webDAV *self) {
	--status;
	if (!status)
		ne_sock_exit();
	self->ob_type->tp_free((PyObject*)self);
}

static PyMemberDef webDAV_members[] = {
	{"oauth",  T_INT, offsetof(webDAV, oauth), 0, "True if oauth2 should be used, False otherwise (default)"},
	{"user", T_STRING, offsetof(webDAV, user), 0, "string with login"},
	{"authHeader", T_STRING, offsetof(webDAV, authHeader), 0, 
		"string with encrypted login-password pair(should be secured or obsoleted)"},
	{"spaceHost", T_STRING, offsetof(webDAV, spaceHost), 0,
		"adress of cloud"},
	{NULL}
};

static PyMethodDef webDAV_methods[] = {
	{"verbose",  (PyCFunction) webDAV_verbose, METH_NOARGS,
		"True if debug information should be written to err, False otherwise (default)."},
	{"login", (PyCFunction) webDAV_PyLogin, METH_VARARGS|METH_KEYWORDS,
		"login([login = <str>, password = <str>, authHeader = <str>])\n\
			Sets self.authHeader, which is string used as value of 'Authorization' header.\n\
			You can login from authHeader if you have one, or with login, password pair (dict).\n\
			With empty arguments will start two dialogs to build self.authHeader.\n\
			In all cases you can set oauth = True to use oauth2 protocol."
	},
	{"catchCode", (PyCFunction) webDAV_catchCode, METH_NOARGS,
			"catchCode() -> oauth2 code\n\
				Catches oauth2 code.\n\
				See http://api.yandex.ru/oauth/doc/dg/reference/obtain-access-token.xml for more info."
	},
	{"run", (PyCFunction) webDAV_run, METH_KEYWORDS,
			"run(arg)\n\
				Runs commands.\n\
				For example self.run(['listDir', 'myCol']) will be parsed to self.listDir('myCol', inter = True)"
	},
	{"listDir", (PyCFunction) webDAV_listDir, METH_KEYWORDS,
		"listDir('remote/path'[, inter = False]) -> content of /remote/path\n\
			List content /remote/path.\n\
			If /remote/path is collection 'content' is files and collection located in it, /remote/path object otherwise.\n\
			If inter = True plain list of content will be written to self.out 'one-by-line',\n\
			list of dictionaries with 'name', 'mime' and 'href' fields will be returned otherwise.\n\
			For elem in result:\n\
			elem['name'] is display name\n\
			elem['href'] is absolute path in the server\n\
			elem['type'] is MIME type of elem"
	},
	{"download", (PyCFunction) webDAV_download, METH_KEYWORDS,
		"download('remote/path/to/f', 'local/path'[, toString = False])\n\
			Downloads file from remote/path/to/f as local/path/f.\n\
			If toString = True content of remote/path/to/f will be returned as string."
	},
	{"upload", (PyCFunction) webDAV_upload, METH_KEYWORDS,
		"upload('local/path/to/f', 'remote/path'[, fromString = False])\n\
			Uploads file from local/path/to/f as remote/path/f.\n\
			If fromString = True first argument will be uploaded as remote/path."
	},
	{"copy", (PyCFunction) webDAV_copy, METH_KEYWORDS,
		"copy('remote/path/to/f', 'another/location/path')\n\
		Copies file from remote/path/to/f to another/location/path/."
	},
	{"mkcol", (PyCFunction) webDAV_mkcol, METH_KEYWORDS,
		"mkcol('path/to/new/directory/col')\n\
			Makes collection col in server at /path/to/new/directory which exist."
	},
	{"delete", (PyCFunction) webDAV_delete, METH_KEYWORDS,
		"delete('path/to/smth')\n\
			Deletes /path/to/smth."
	},
	{"getId", (PyCFunction) webDAV_getId, METH_NOARGS,
		"return id of app."
	},
	{"__getSecret", (PyCFunction) webDAV_getSecret, METH_NOARGS,
		"return secret of app."
	},
	{NULL}  /* Sentinel */
};

static PyTypeObject webDAVType = {
	PyObject_HEAD_INIT(NULL)
	0,						/*ob_size*/
	"webdavbind.webDAV",				/*tp_name*/
	sizeof(webDAV),					/*tp_basicsize*/
	0,						/*tp_itemsize*/
	(destructor)webDAV_dealloc,			/*tp_dealloc*/
	0,						/*tp_print*/
	0,						/*tp_getattr*/
	0,						/*tp_setattr*/
	0,						/*tp_compare*/
	0,						/*tp_repr*/
	0,						/*tp_as_number*/
	0,						/*tp_as_sequence*/
	0,						/*tp_as_mapping*/
	0,						/*tp_hash */
	0,						/*tp_call*/
	0,						/*tp_str*/
	0,						/*tp_getattro*/
	0,						/*tp_setattro*/
	0,						/*tp_as_buffer*/
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,	/*tp_flags*/
	"webDAV objects",				/* tp_doc */
	0,						/* tp_traverse */
	0,						/* tp_clear */
	0,						/* tp_richcompare */
	0,						/* tp_weaklistoffset */
	0,						/* tp_iter */
	0,						/* tp_iternext */
	webDAV_methods,					/* tp_methods */
	webDAV_members,					/* tp_members */
	0,						/* tp_getset */
	0,						/* tp_base */
	0,						/* tp_dict */
	0,						/* tp_descr_get */
	0,						/* tp_descr_set */
	0,						/* tp_dictoffset */
	(initproc)webDAV_init,				/* tp_init */
};

static PyMethodDef module_methods[] = {
	{NULL}  /* Sentinel */
};

void initwebdav(void) {
	PyObject* m;
	status = 0;

	webDAVType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&webDAVType) < 0)
		return;

	m = Py_InitModule3("webdav", module_methods, "Binding of neon lib for us.");

	if (m == NULL)
		return;

	Py_INCREF(&webDAVType);
	PyModule_AddObject(m, "webDAV", (PyObject *)&webDAVType);
}

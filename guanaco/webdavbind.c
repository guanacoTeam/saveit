#include<Python.h>
#include<structmember.h>
#include<ne_socket.h>

//webDAV class
typedef struct {
		PyObject_HEAD
		//self.inp = args.get('inp', sys.stdin)
		//self.out = args.get('out', sys.stdout)
		//self.err = args.get('err', sys.stderr)
		int oauth; //oauth flag
		int verbose; //verbosity flag
		char *authHeader; //authHeader
		char *login; //username
		//char *spaceHost = "webdav.yandex.ru"; //spaceHost
} webDAV;

static int webDAV_init(webDAV *self, PyObject *args, PyObject* kwds)
{
	//static char *kwlist[] = {"inp", "out", "err", "verbose", "oauth", "login", "password"};
	static char *kwlist[] = {"verbose", "oauth", "authHeader", "login"};
	//self.inp = args.get('inp', sys.stdin)
	//self.out = args.get('out', sys.stdout)
	//self.err = args.get('err', sys.stderr)
	self->oauth = 0;
	self->verbose = 0;
	self->authHeader = NULL;
	self->login = NULL;
	//passwd = args.get('password')
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "|iiss", kwlist, &self->verbose, &self->oauth, &self->authHeader, &self->login))
		return -1;
	//End of parsing
	//self.login(oauth = self.oauth, login = self.user, password = passwd)
	return 0;
}

static void webDAV_dealloc(webDAV *self)
{
	self->ob_type->tp_free((PyObject*)self);
}

static PyMemberDef webDAV_members[] = {
	{ "oauth",  T_INT, offsetof(webDAV, oauth), 0, "True if oauth2 should be used, False otherwise (default)"},
	{ "verbose",  T_INT, offsetof(webDAV, verbose), 0, "True if debug information should be written to err, False otherwise (default)."},
	{"login", T_STRING, offsetof(webDAV, login), 0, "string with login"},
	{"authHeader", T_STRING, offsetof(webDAV, authHeader), 0, "string with crypted login-password pair(should be secureted or obsoleted)"},
	{NULL}
};

static PyMethodDef webDAV_methods[] = {
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

void initwebdavbind(void){
	PyObject* m;

	webDAVType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&webDAVType) < 0)
		return;

	m = Py_InitModule3("webdavbind", module_methods, "Binding of neon lib for us.");

	if (m == NULL)
		return;

	Py_INCREF(&webDAVType);
	PyModule_AddObject(m, "webDAV", (PyObject *)&webDAVType);
}

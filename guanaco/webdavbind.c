#include<Python.h>
#include<structmember.h>
#include<ne_socket.h>

typedef struct {
		PyObject_HEAD
		//self.inp = args.get('inp', sys.stdin)
		//self.out = args.get('out', sys.stdout)
		//self.err = args.get('err', sys.stderr)
		//self.oauth = args.get('oauth', False)
		//self.verbose = args.get('verbose', False)
		//self.authHeader = args.get('authHeader', '')
		//self.user = args.get('login')
		char *name;
} webDAV;

static int webDAV_init(webDAV *self, PyObject *args, PyObject* kwds)
{
    PyArg_ParseTuple(args, "s", &self->name);
    return 0;
}

static void webDAV_dealloc(webDAV *self)
{
    self->ob_type->tp_free((PyObject*)self);
}

static PyMemberDef webDAV_members[] = {
    { "name",  T_STRING, offsetof(webDAV, name), 0,
                "The name of the obj."},
    {NULL}
};

static PyMethodDef webDAV_methods[] = {
    {NULL}  /* Sentinel */
};

static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

static PyTypeObject webDAVType = {
    PyObject_HEAD_INIT(NULL)
    0,						/*ob_size*/
    "webdavbind.webDAV",			/*tp_name*/
    sizeof(webDAV),				/*tp_basicsize*/
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
    webDAV_methods,				/* tp_methods */
    webDAV_members,				/* tp_members */
    0,						/* tp_getset */
    0,						/* tp_base */
    0,						/* tp_dict */
    0,						/* tp_descr_get */
    0,						/* tp_descr_set */
    0,						/* tp_dictoffset */
    (initproc)webDAV_init,			/* tp_init */
};

void initwebdavbind(void){
    PyObject* m;

    webDAVType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&webDAVType) < 0)
        return;

    m = Py_InitModule3("webdavbind", module_methods,
                       "Binding of neon lib for us.");

    if (m == NULL)
      return;

    Py_INCREF(&webDAVType);
    PyModule_AddObject(m, "webDAV", (PyObject *)&webDAVType);
}

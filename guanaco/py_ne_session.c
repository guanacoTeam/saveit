#include"py_neon.h"

static int PyNeSession_init(PyNeSession *self, PyObject *args, PyObject *kwds) {
	char *scheme = NULL, *hostname = NULL;
	unsigned int port = 0;
	char *kwlist[] = {"scheme", "hostname", "port"};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "ssI", kwlist, &scheme, &hostname, &port))
		return -1;

	self->ne_ses = ne_session_create(scheme, hostname, port); 
	return 0;
}

static void PyNeSession_dealloc(PyNeSession *self) {
	--neon_status;
	if (!neon_status)
		ne_sock_exit();
	self->ob_type->tp_free((PyObject*)self);
}

void initpyneon(void) {
	PyObject* module;
	neon_status = 0;

	if (!neon_status && ne_sock_init()) { //trying to init neon
		printf("%d\n", neon_status);
		perror("Global neon error!");
		exit(-1);
	}
	++neon_status;

	PyNeSessionType.tp_new = PyType_GenericNew;
	if (PyType_Ready(&PyNeSessionType) < 0)
		return;

	module = Py_InitModule3("pyneon", module_methods, "Binding of neon lib.");

	if (module == NULL)
		return;

	Py_INCREF(&PyNeSessionType);
	PyModule_AddObject(module, "NeSession", (PyObject *)&PyNeSessionType);
}

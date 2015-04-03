#include"py_neon.h"
//TODO: It crashes with SIGSEV after attempts of initialization

int PyNeSession_init(PyNeSession *self, PyObject *args, PyObject *kwds) {
	char *scheme = NULL, *hostname = NULL;
	unsigned int port = 0;
	char *kwlist[] = {"scheme", "hostname", "port"};
	
	if (!PyArg_ParseTupleAndKeywords(args, kwds, "ssI", kwlist, &scheme, &hostname, &port))
		return -1;

	ne_sock_init();
	self->ne_sess = ne_session_create(scheme, hostname, port);
	++neon_status;
	return 0;
}

void PyNeSession_dealloc(PyNeSession *self) {
	ne_session_destroy(self->ne_sess);

	--neon_status;
	ne_sock_exit();

	self->ob_type->tp_free((PyObject*)self);

	return ;
}

void PyNeSession_close_connection(PyNeSession *self) {
	ne_close_connection(self->ne_sess);

	return ;
}

void PyNeSession_destroy(PyNeSession *self) {
	ne_session_destroy(self->ne_sess);

	return ;
}

void PyNeSession_set_flag(PyNeSession *self, PyObject *args, PyObject *kwds) {
	int flag = 0, value = 0;
	char *kwlist[] = {"flag", "value"};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "ii", kwlist, &flag, &value))
		return ;

	ne_set_session_flag(self->ne_sess, flag, value);
	return ;
}

PyObject *PyNeSession_get_flag(PyNeSession *self, PyObject *args, PyObject *kwds) {
	int flag = 0;
	char *kwlist[] = {"flag"};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "i", kwlist, &flag))
		return 0;

	return Py_BuildValue("i", ne_get_session_flag(self->ne_sess, flag));
}

PyMemberDef PyNeSession_members[] = {
	{NULL}
};

PyMethodDef PyNeSession_methods[] = {
	{"closeConnection", (PyCFunction) PyNeSession_close_connection, METH_NOARGS,
		"Prematurely force the connection to be closed for the given session."},
	{"destroy", (PyCFunction) PyNeSession_destroy, METH_NOARGS,
		"Finish an HTTP session"},
	{"setFlag", (PyCFunction) PyNeSession_set_flag, METH_KEYWORDS,
		"The NeSession.setFlag function enables or disables a session flag.\n"
		"Passing a non-zero value argument enables the flag, and zero disables it.\n"
		"The following flags are defined:\n"
		"	persist		0\n"
		"		disable this flag to prevent use of persistent connections\n"
  		"	icy		1\n"
		"		enable this flag to enable support for non-HTTP ShoutCast-style \"ICY\" responses\n"
		"	ssl2		2\n"
		" 		disable this flag to disable support for the SSLv2 protocol\n"
		"	rfc4918		3\n"
		"		enable this flag to enable support for RFC4918-only WebDAV features;\n"
		"		losing backwards-compatibility with RFC2518 servers\n"
  		"	connauth	4\n"
		"		enable this flag if an RFC-violating connection-based HTTP authentication scheme is in use\n"
		"	tlssni		5\n"
		"		disable this flag if a server is used which does not correctly support the TLS SNI extension\n"
		"	expect100	6\n"
		"		enable this flag to enable the request flag req100 for new requests\n"},
	{"getFlag", (PyCFunction) PyNeSession_get_flag, METH_KEYWORDS, 
		"NSession.getFlag function returns zero if a flag is disabled,\n"
		"less than zero if the flag is not supported,\n"
		"or greater than zero if the flag is enabled.\n"},
	{NULL}
};

PyTypeObject PyNeSessionType = {
	PyObject_HEAD_INIT(NULL)
	.tp_name = "pyneon.NeSession",
	.tp_basicsize = sizeof(PyNeSession),
	.tp_dealloc = (destructor) PyNeSession_dealloc,
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
	.tp_methods = PyNeSession_methods,
	.tp_members = PyNeSession_members,
	.tp_init = (initproc) PyNeSession_init,
	.tp_doc = 
		"An NeSession object represents an HTTP session\n"
			"- a logical grouping of a sequence of HTTP requests made to a certain server.\n"
		"Any requests made using the session can use a persistent connection,\n"
			"share cached authentication credentials and any other common attributes.\n\n"

		"A new HTTP session is created using the NeSession.create function;\n"
			"the hostname and port parameters specify the origin server to use,\n"
			"along with the scheme (usually \"http\").\n"
		"Before the first use of NeSession.create in a process,\n"
			"NeSock.init must have been called to perform any global initialization\n"
			"needed by any libraries used by neon.\n\n"

		"To enable SSL/TLS for the session,\n"
			"pass the string \"https\" as the scheme parameter,\n"
			"and either register a certificate verification function (see NeSsl.setVerify)\n"
			"or trust the appropriate certificate (see NeSsl.trustCert, NeSsl.trustDefaultCa).\n\n"

		"To use a proxy server for the session,\n"
			"it must be configured (see NeSession.proxy)\n"
			"before any requests are created from session object.\n\n"

		"Further per-session options may be changed using the NeSession.setFlag interface.\n\n"

		"If it is known that the session\n"
			"will not be used for a significant period of time,\n"
			"NeSession.closeConnection can be called to close the connection,\n"
			"if one remains open.\n"
		"Use of this function is entirely optional,\n"
			"but it must not be called\n"
			"if there is a request active using the session.\n\n"

		"Once a session has been completed,\n"
			"NeSession.destroy must be called\n"
			"to destroy the resources associated with the session.\n"
		"(Not for Python): Any subsequent use of the session pointer produces undefined behaviour.\n"
		"The NeSession object must not be destroyed\n"
			"until after all associated request objects have been destroyed.\n\n"
};

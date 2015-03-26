#ifndef _PY_HEON_H
#define _PY_NEON_H 1
#include<Python.h>
#include<structmember.h>
#include<ne_socket.h>
#include<ne_utils.h>
#include<ne_session.h>

static int neon_status;

static PyMethodDef module_methods[] = {
	{NULL}  /* Sentinel */
};

//NeSession
typedef struct {
	PyObject_HEAD;
	ne_session *ne_ses;
} PyNeSession;


static int PyNeSession_init(PyNeSession *self, PyObject *args, PyObject *kwds);
static void PyNeSession_dealloc(PyNeSession *self);

static PyMemberDef PyNeSession_members[] = {
	{NULL}
};

static PyMethodDef PyNeSession_methods[] = {
	{NULL}
};

static PyTypeObject PyNeSessionType = {
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
#endif

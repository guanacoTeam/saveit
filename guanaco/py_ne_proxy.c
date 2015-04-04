#include"py_neon.h"

void PyNeSession_proxy(PyNeSession *self, PyObject *args, PyObject *kwds) {
	char *hostname = NULL;
	unsigned int port = 0;
	char *kwlist[] = {"hostname", "port"};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "sI", kwlist, &hostname, &port))
		return ;

	ne_session_proxy(self->ne_sess, hostname, port);	
	return ;
}

extern void PyNeSession_system_proxy(PyNeSession *self, PyObject *args, PyObject *kwds) {
	unsigned int flags = 0;
	char *kwlist[] = {"flags"};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "I", kwlist, &flags))
		return ;

	ne_session_system_proxy(self->ne_sess, flags);	
	return ;
}

extern void PyNeSession_socks_proxy(PyNeSession *self, PyObject *args, PyObject *kwds) {
	int version = 0;
	char *hostname = NULL, *username = NULL, *password = NULL;
	unsigned int port = 0;
	char *kwlist[] = {"version", "hostname", "port", "username", "password"};

	if (!PyArg_ParseTupleAndKeywords(args, kwds, "isIss", kwlist, &version, &hostname, &port, &username, &password))
		return ;

	ne_session_socks_proxy(self->ne_sess, version, hostname, port, username, password);
	return ;
}

extern void PyNeSession_set_addrlist(PyNeSession *self, PyObject *args, PyObject *kwds) {
	//TODO
	return ;
}

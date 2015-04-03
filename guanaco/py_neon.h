#ifndef PY_HEON_H
#define PY_NEON_H 1
#include<Python.h>
#include<structmember.h>
#include<ne_socket.h>
#include<ne_utils.h>
#include<ne_session.h>
#include<ne_request.h>

extern void initpyneon(void);

extern int neon_status;

extern PyMethodDef pyneon_methods[];

//NeSession
typedef struct {
	PyObject_HEAD;
	ne_session *ne_sess;
} PyNeSession;


extern int PyNeSession_init(PyNeSession *self, PyObject *args, PyObject *kwds);

extern void PyNeSession_dealloc(PyNeSession *self);

extern void PyNeSession_close_connection(PyNeSession *self);

extern void PyNeSession_destroy(PyNeSession *self);

extern void PyNeSession_set_flag(PyNeSession *self, PyObject *args, PyObject *kwds);

extern PyObject *PyNeSession_get_flag(PyNeSession *self, PyObject *args, PyObject *kwds);

//NeSession.proxy
extern void PyNeSession_proxy(PyNeSession *self, PyObject *args, PyObject *kwds);

extern void PyNeSession_system_proxy(PyNeSession *self, PyObject *args, PyObject *kwds);

extern void PyNeSession_socks_proxy(PyNeSession *self, PyObject *args, PyObject *kwds);

extern void PyNeSession_set_addrlist(PyNeSession *self, PyObject *args, PyObject *kwds);


extern PyMemberDef PyNeSession_members[];

extern PyMethodDef PyNeSession_methods[];

extern PyTypeObject PyNeSessionType;
#endif

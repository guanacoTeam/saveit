#include"py_neon.h"

int neon_status = 0;

PyMethodDef pyneon_methods[] = {
	{NULL}  /* Sentinel */
};

void initpyneon(void) {
	int ne_sess_flag = 0, socks = 0;
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

	module = Py_InitModule3("pyneon", pyneon_methods, "Binding of neon lib.");

	if (module == NULL)
		return;

    	PyModule_AddIntConstant(module, "persist", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "icy", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "ssl2", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "rfc4918", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "connauth", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "tlssni", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "expect100", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "last", ne_sess_flag++);
    	PyModule_AddIntConstant(module, "sv4", socks++);
    	PyModule_AddIntConstant(module, "sv4a", socks++);
    	PyModule_AddIntConstant(module, "sv5", socks++);

	Py_INCREF(&PyNeSessionType);
	PyModule_AddObject(module, "NeSession", (PyObject *)&PyNeSessionType);
}

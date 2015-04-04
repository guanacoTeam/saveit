#include"py_neon.h"

int neon_status = 0;

PyMethodDef pyneon_methods[] = {
	{NULL}  /* Sentinel */
};

void initpyneon(void) {
	int enumer = 0;
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

    	PyModule_AddIntConstant(module, "persist", enumer++);
    	PyModule_AddIntConstant(module, "icy", enumer++);
    	PyModule_AddIntConstant(module, "ssl2", enumer++);
    	PyModule_AddIntConstant(module, "rfc4918", enumer++);
    	PyModule_AddIntConstant(module, "connauth", enumer++);
    	PyModule_AddIntConstant(module, "tlssni", enumer++);
    	PyModule_AddIntConstant(module, "expect100", enumer++);
    	PyModule_AddIntConstant(module, "last", enumer++);

	enumer = 0;
    	PyModule_AddIntConstant(module, "sv4", enumer++);
    	PyModule_AddIntConstant(module, "sv4a", enumer++);
    	PyModule_AddIntConstant(module, "sv5", enumer++);

	enumer = 0;
    	PyModule_AddIntConstant(module, "ipv4", enumer++);
    	PyModule_AddIntConstant(module, "ipv6", enumer++);

	Py_INCREF(&PyNeSessionType);
	PyModule_AddObject(module, "NeSession", (PyObject *)&PyNeSessionType);
}

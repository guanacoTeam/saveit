from distutils.core import setup, Extension

neon = Extension(
	name = 'pyneon',
	sources = ['guanaco/py_ne_iaddr.c', 'guanaco/py_neon.c', 'guanaco/py_ne_proxy.c', 'guanaco/py_ne_session.c'],
	include_dirs = ['/usr/include/neon'],
	library_dirs = ['/usr/lib'],
	libraries = ['neon-gnutls'],
	define_macros = [('_LARGEFILE64_SOURCE', None), ('NE_LFS', None), ('PY_SSIZE_T_CLEAN', "size_t")],
	#extra_compile_args = ['-Wextra']
)

webdav = Extension(
	name = 'webdav',
	sources = ['guanaco/webdavbind.c', 'guanaco/getpass.c'],
	include_dirs = ['/usr/include/neon'],
	library_dirs = ['/usr/lib'],
	libraries = ['neon-gnutls'],
	define_macros = [('_LARGEFILE64_SOURCE', None), ('NE_LFS', None), ('PY_SSIZE_T_CLEAN', "size_t")],
	#extra_compile_args = ['-Wextra']
)

setup(name='pyneon', version='0.1', ext_modules=[neon]) #setuping

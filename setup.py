from distutils.core import setup, Extension

webdav = Extension(
	name = 'webdav',
	sources = ['guanaco/webdavbind.c', 'guanaco/getpass.c'],
	include_dirs = ['/usr/include/neon'],
	library_dirs = ['/usr/lib'],
	libraries = ['neon-gnutls'],
	define_macros = [('_LARGEFILE64_SOURCE', None), ('NE_LFS', None), ('PY_SSIZE_T_CLEAN', "size_t")],
	#extra_compile_args = ['-Wextra']
)

setup(name='siModules', version='0.0.1', ext_modules=[webdav]) #setuping

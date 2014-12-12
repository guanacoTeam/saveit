from distutils.core import setup, Extension

webdav = Extension(
	name = 'webdav',
	sources = ['guanaco/webdavbind.c'],
	include_dirs = ['/usr/include/neon']
)

setup(name='siModules', version='0.0.1', ext_modules=[webdav]) #setuping

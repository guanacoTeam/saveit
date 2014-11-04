from distutils.core import setup, Extension
setup(name='webdavbind', version='0.0.1',  \
      ext_modules=[Extension('webdavbind', ['webdavbind.c'], include_dirs = ['/usr/include/neon'])])

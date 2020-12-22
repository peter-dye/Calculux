"""
 py2app/py2exe build script for MyApplication.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
     python setup.py py2app

 Usage (Windows):
     python setup.py py2exe
"""
import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup

mainscript = 'MyApplication.py'
DATA_FILES = ['stylesheet.qss']

if sys.platform == 'darwin':
 extra_options = dict(
     setup_requires=['py2app'],
     app=[mainscript],
     data_files=DATA_FILES,
     # Cross-platform applications generally expect sys.argv to
     # be used for opening files.
     options=dict(py2app=dict(argv_emulation=True)),
 )
elif sys.platform == 'win32':
 extra_options = dict(
     setup_requires=['py2exe'],
     app=[mainscript],
     data_files=DATA_FILES
 )
else:
 extra_options = dict(
     # Normally unix-like platforms will use "setup.py install"
     # and install the main script as such
     scripts=[mainscript],
 )

setup(
name="MyApplication",
**extra_options
)

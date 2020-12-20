from distutils.core import setup
import py2exe

APP = ['Calculux.py']
DATA_FILES = ['stylesheet.qss']
OPTIONS = {
    'iconfile':'resources/icon.icns',
}

setup(
    console=APP,
    data_files=DATA_FILES,
    options={'py2eze': OPTIONS},
    setup_requires=['py2exe']
)

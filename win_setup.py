from distutils.core import setup
import py2exe

APP = ['calculux.py']
DATA_FILES = [('', ['stylesheet.qss'])]
OPTIONS = {
    # 'iconfile':'resources/icon.icns',
}

setup(
    windows=APP,
    data_files=DATA_FILES,
    options={'py2eze': OPTIONS}
)

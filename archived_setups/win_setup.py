from distutils.core import setup
import py2exe

DATA_FILES = [('', ['stylesheet.qss'])]
OPTIONS = {
    # 'iconfile':'resources/icon.ico',
}

setup(
    windows={'script': 'calculux.py'},
    data_files=DATA_FILES,
    options={'py2exe': OPTIONS}
)

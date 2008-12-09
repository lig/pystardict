#!/usr/bin/env python

import os
from distutils.core import setup

setup(
    name='PyStarDict',
    version='0.1-alpha',
    description=
'Library for manipulating StarDict dictionaries from within Python',
    author='Serge Matveenko',
    author_email='s@matveenko.ru',
    url='http://pystardict.nophp.ru/',
    requires=['gzip', 'struct',],
    py_modules=['pystardict',],
    package_dir={'': 'src',},
    data_files=[
        ('share/pystardict', [
            'examples/demo.py',
        ],),
        ('share/pystardict/stardict-quick_eng-rus-2.4.2', [
            'examples/demo.py',
            'examples/stardict-quick_eng-rus-2.4.2/quick_english-russian.dict',
            'examples/stardict-quick_eng-rus-2.4.2/quick_english-russian.idx',
            'examples/stardict-quick_eng-rus-2.4.2/quick_english-russian.idx.oft',
            'examples/stardict-quick_eng-rus-2.4.2/quick_english-russian.ifo',
        ],),
        ('share/pystardict/stardict-quick_rus-eng-2.4.2', [
            'examples/stardict-quick_rus-eng-2.4.2/quick_russian-english.dict.dz',
            'examples/stardict-quick_rus-eng-2.4.2/quick_russian-english.idx',
            'examples/stardict-quick_rus-eng-2.4.2/quick_russian-english.idx.oft',
            'examples/stardict-quick_rus-eng-2.4.2/quick_russian-english.ifo',
        ],),
    ],
)

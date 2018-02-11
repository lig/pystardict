#!/usr/bin/env python
"""
Copyright 2008 Serge Matveenko

This file is part of PyStarDict.

PyStarDict is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyStarDict is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyStarDict.  If not, see <http://www.gnu.org/licenses/>.

"""
from setuptools import setup


setup(
    name='PyStarDict',
    use_scm_version=True,
    description='Library for manipulating StarDict dictionaries from within Python',
    author='Serge Matveenko',
    author_email='s@matveenko.ru',
    url='http://www.ohloh.net/p/pystardict',
    install_requires=['six'],
    setup_requires=['setuptools_scm'],
    py_modules=['pystardict'],
    data_files=[
        ('share/pystardict', [
            'examples/demo.py',
            'examples/profile_demo.py',
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

# -*- coding: utf-8 -*-
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

import os, sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from pystardict import Dictionary

class DictionaryTest(unittest.TestCase):
    
    def setUp(self):
        self.dict = Dictionary(os.path.join(os.path.dirname(__file__), '..',
            'examples', 'stardict-quick_eng-rus-2.4.2/quick_english-russian'))
    
    def test001Idx(self):
        self.assertEqual(self.dict.idx['test'], (581161, 16,))

    def test002Dict(self):
        self.assertEqual(self.dict.dict['test'], 'проверка')
    
    def test003Dictionary(self):
        self.assertEqual(self.dict['test'], 'проверка')
    
    def test004Contains(self):
        self.assertTrue('test' in self.dict)
        self.assertFalse('testtt' in self.dict)
    
    def test005Delitem(self):
        self.dict['test']
        del self.dict['test']
        self.assertFalse('test' in self.dict._dict_cache)
    
    def test006Len(self):
        self.assertEqual(len(self.dict), 31705)
    
    def test007Eq(self):
        y = Dictionary(os.path.join(os.path.dirname(__file__), '..',
            'examples', 'stardict-quick_eng-rus-2.4.2/quick_english-russian'))
        self.assertTrue(self.dict == y)
    
    def test008Ne(self):
        y = Dictionary(os.path.join(os.path.dirname(__file__), '..',
            'examples', 'stardict-quick_eng-rus-2.4.2/quick_english-russian'))
        self.assertFalse(self.dict != y)
    
    def test009Repr(self):
        self.assertEqual(repr(self.dict),
            '''<class 'pystardict.Dictionary'> quick_english-russian''')
    
    def test010Clear(self):
        self.dict['test']
        self.dict.clear()
        self.assertEqual(len(self.dict._dict_cache), 0)
    
    def test011Get(self):
        self.assertEqual(self.dict.get('test', 't'), 'проверка')
        self.assertEqual(self.dict.get('testtt', 't'), 't')

suite = unittest.defaultTestLoader.loadTestsFromTestCase(DictionaryTest)

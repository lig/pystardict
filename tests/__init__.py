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
        self.dict = Dictionary(
            'examples/stardict-quick_eng-rus-2.4.2/quick_english-russian')
    
    def test001Idx(self):
        self.assertEqual(self.dict.idx['test'], (581161, 16,))

    def test002Dict(self):
        self.assertEqual(self.dict.dict['test'], 'проверка')
    
    def test003Dictionary(self):
        self.assertEqual(self.dict['test'], 'проверка')

suite = unittest.defaultTestLoader.loadTestsFromTestCase(DictionaryTest)

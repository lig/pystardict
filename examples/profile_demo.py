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

@author: Serge Matveenko <s@matveenko.ru>
"""
import cProfile
import os
import sys

"""hack in local sources"""
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src')) 
from demo import demo

if __name__ == '__main__':
    cProfile.run('demo()')

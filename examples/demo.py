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
# -*- coding: utf-8 -*-
import datetime

from pystardict import Dictionary

if __name__ == '__main__':
    
    milestone1 = datetime.datetime.today()
    
    dict1 = Dictionary('stardict-quick_eng-rus-2.4.2/quick_english-russian')
    dict2 = Dictionary('stardict-quick_rus-eng-2.4.2/quick_russian-english')
    
    milestone2 = datetime.datetime.today()
    print '2 dicts load:', milestone2-milestone1
    
    print dict1.idx['test']
    print dict2.idx['проверка']
    
    milestone3 = datetime.datetime.today()
    print '2 cords getters:', milestone3-milestone2
    
    print dict1.dict['test']
    print dict2.dict['проверка']
    
    milestone4 = datetime.datetime.today()
    print '2 direct data getters (w\'out cache):', milestone4-milestone3
    
    print dict1['test']
    print dict2['проверка']

    milestone5 = datetime.datetime.today()
    print '2 high level data getters (not cached):', milestone5-milestone4
    
    print dict1['test']
    print dict2['проверка']
    
    milestone6 = datetime.datetime.today()
    print '2 high level data getters (cached):', milestone6-milestone5

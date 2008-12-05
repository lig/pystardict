# -*- coding: utf-8 -*-
from __init__ import Dictionary

if __name__ == '__main__':

    dict1 = Dictionary('/home/lig/workspace/PyStarDict/stardict-quick_eng-rus-2.4.2/quick_english-russian')
    dict2 = Dictionary('/home/lig/workspace/PyStarDict/stardict-quick_rus-eng-2.4.2/quick_russian-english')

    print dict1.idx['test']
    print dict2.idx['аббат']

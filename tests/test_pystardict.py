# -*- coding: utf-8 -*-
import os

import pytest

from pystardict import Dictionary


@pytest.fixture(params=['on_disk', 'in_memory'], scope="session")
def fixture_dict(request):
    return {
        'on_disk': Dictionary(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                'examples',
                'stardict-quick_eng-rus-2.4.2',
                'quick_english-russian')),
        'in_memory': Dictionary(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir,
                'examples',
                'stardict-quick_eng-rus-2.4.2',
                'quick_english-russian'),
            in_memory=True),
    }[request.param]


@pytest.fixture
def fixture_in_memory_dict():
    return


def test001Idx(fixture_dict):
    assert fixture_dict.idx['test'] == (581161, 16,)


def test002Dict(fixture_dict):
    assert fixture_dict.dict['test'] == u'проверка'


def test003Dictionary(fixture_dict):
    assert fixture_dict['test'] == u'проверка'


def test004Contains(fixture_dict):
    assert 'test' in fixture_dict
    assert 'testtt' not in fixture_dict


def test005Delitem(fixture_dict):
    fixture_dict['test']
    del fixture_dict['test']
    assert 'test' not in fixture_dict._dict_cache


def test006Len(fixture_dict):
    assert len(fixture_dict) == 31705


def test007Eq(fixture_dict):
    y = Dictionary(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'examples',
            'stardict-quick_eng-rus-2.4.2',
            'quick_english-russian'))
    assert fixture_dict == y


def test008Ne(fixture_dict):
    y = Dictionary(
        os.path.join(
            os.path.dirname(__file__),
            os.pardir,
            'examples',
            'stardict-quick_eng-rus-2.4.2',
            'quick_english-russian'))
    assert (fixture_dict != y) is False


def test009Repr(fixture_dict):
    assert repr(fixture_dict) ==\
        "<class 'pystardict.Dictionary'> quick_english-russian"


def test010Clear(fixture_dict):
    fixture_dict['test']
    fixture_dict.clear()
    assert len(fixture_dict._dict_cache) == 0


def test011Get(fixture_dict):
    assert fixture_dict.get('test', 't') == u'проверка'
    assert fixture_dict.get('testtt', 't') == 't'


def test013IterateDict(fixture_dict):
    for k, v in fixture_dict.items():
        assert fixture_dict[k] == v

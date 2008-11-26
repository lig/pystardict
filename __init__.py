class StarDictDict(dict):
    """
    Dictionary-like class for lazy manipulating stardict dictionaries
    
    All items of this dictionary are writable and dict is expandable itself,
    but changes are not stored anywhere and available in runtime only.
    
    We assume in this documentation that "x" or "y" is instances of the
    StarDictDict class and "x.{ifo,idx{,.gz},dict{,.dz),syn}" or
    "y.{ifo,idx{,.gz},dict{,.dz),syn}" is files of the corresponding stardict
    dictionaries.
    
    
    Following documentation is from the "dict" class an is subkect to rewrite
    in further impleneted methods:
    
    """
    
    def __init__(self, filename_prefix):
        """
        filename_prefix: path to dictionary files without files extensions
        
        initializes new StarDictDict instance from stardict dictionary files
        provided by filename_prefix
        
        TODO: implement me
        """
        
        #somedict.ifo
        self.ifo = ''
        
        #somedict.idx or somedict.idx.gz
        self.idx = ''
        
        #somedict.dict or somedict.dict.dz
        self.dict = ''
        
        #somedict.syn (optional)
        self.syn = ''
    
    def __cmp__(self, y):
        """
        returns cmp(md5(self.idx), md5(y.idx))
        
        TODO: implement me
        """
        pass
    
    def __contains__(self, k):
        """
        returns True if x.idx has a word k, else False
        
        TODO: implement me
        """
        pass
    
    def __delitem__(self, k):
        """
        blacklists dictionary entry for the word k
        
        TODO: implement me
        """
        pass
    
    def __eq__(self, y):
        """
        returns True if md5(x.idx) is equal to md5(y.idx), else False
        
        TODO: implement me
        """
        pass
    
    def __ge__(self, y):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __getitem__(self, k):
        """
        returns translation for word k
        
        TODO: implement me
        """
        pass
    
    def __gt__(self, y):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __iter__(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __le__(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __len__(self):
        """
        returns number of words provided by wordcount parameter of the x.ifo
        
        TODO: implement me
        """
        pass
    
    def __lt__(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __ne__(self):
        """
        returns True if md5(x.idx) is not equal to md5(y.idx), else False
        
        TODO: implement me
        """
        pass
    
    def __repr__(self):
        """
        returns classname and bookname parameter of the x.ifo
        
        TODO: implement me
        """
        pass
    
    def __setitem__(self, k, v):
        """
        sets translation of the word k to v
        
        TODO: implement me
        """
        pass
    
    def clear(self):
        """
        unlike dict class resets dictionary to the original state, i.e. clears
        all of the blacklisting info or reverts changed values 
        
        TODO: implement me
        """
        pass
    
    def get(self, k, d=''):
        """
        returns translation of the word k from self.dict or d if k not in x.idx
        
        d defaults to empty string
        
        TODO: implement me
        """
        pass
    
    def has_key(self, k):
        """
        returns True if self.idx has a word k, else False
        
        TODO: implement me
        """
        pass
    
    def items(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def iteritems(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def iterkeys(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def itervalues(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def keys(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def pop(self, k, d):
        """
        Returns translation for the word k from self.dict and blacklists
        specified word. If word is not in self.idx, d is returned if given,
        otherwise KeyError is raised
        
        TODO: implement me
        """
        pass
    
    def popitem(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def setdefault(self, k, d):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def update(self, E, **F):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def values(self):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def fromkeys(self, S, v=None):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()

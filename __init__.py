import configobj
import gzip
import sys
from struct import unpack

class _StarDictIfo():
    """
    The .ifo file has the following format:
    
    StarDict's dict ifo file
    version=2.4.2
    [options]
    
    Note that the current "version" string must be "2.4.2" or "3.0.0".  If it's not,
    then StarDict will refuse to read the file.
    If version is "3.0.0", StarDict will parse the "idxoffsetbits" option.
    
    [options]
    ---------
    In the example above, [options] expands to any of the following lines
    specifying information about the dictionary.  Each option is a keyword
    followed by an equal sign, then the value of that option, then a
    newline.  The options may be appear in any order.
    
    Note that the dictionary must have at least a bookname, a wordcount and a 
    idxfilesize, or the load will fail.  All other information is optional.  All 
    strings should be encoded in UTF-8.
    
    Available options:
    
    bookname=      // required
    wordcount=     // required
    synwordcount=  // required if ".syn" file exists.
    idxfilesize=   // required
    idxoffsetbits= // New in 3.0.0
    author=
    email=
    website=
    description=    // You can use <br> for new line.
    date=
    sametypesequence= // very important.
    
    TODO: handle first line correctly
    TODO: handle version
    """
    def __init__(self, dict_prefix, container):
        
        ifo_filename = '%s.ifo' % dict_prefix
        
        try:
            self._file = open(ifo_filename)
        except IOError:
            raise Exception('.ifo file does not exists')
        
        _configobj = configobj.ConfigObj(self._file)
        
        self.bookname = _configobj.get('bookname')
        if self.bookname is None: raise Exception('ifo has no bookname')
        
        self.wordcount = _configobj.get('wordcount')
        if self.wordcount is None: raise Exception('ifo has no wordcount')
        self.wordcount = int(self.wordcount)
        
        try:
            _syn = open('%s.syn' % dict_prefix)
            self.synwordcount = _configobj.get('synwordcount')
            if self.synwordcount is None:
                raise Exception('ifo has no synwordcount but .syn file exists')
            self.synwordcount = int(self.synwordcount)
        except IOError:
            pass
        
        self.idxfilesize = _configobj.get('idxfilesize')
        if self.idxfilesize is None: raise Exception('ifo has no idxfilesize')
        self.idxfilesize = int(self.idxfilesize)
        
        self.idxoffsetbits = _configobj.get('idxoffsetbits', 32)
        if self.idxoffsetbits is not None:
            self.idxoffsetbits = int(self.idxoffsetbits)
        
        self.author = _configobj.get('author')
        
        self.email = _configobj.get('email')
        
        self.website = _configobj.get('website')
        
        self.description = _configobj.get('description')
        
        self.date = _configobj.get('date')
        
        self.sametypesequence = _configobj.get('sametypesequence')

class _StarDictIdx():
    """
    The .idx file is just a word list.
    
    The word list is a sorted list of word entries.
    
    Each entry in the word list contains three fields, one after the other:
         word_str;  // a utf-8 string terminated by '\0'.
         word_data_offset;  // word data's offset in .dict file
         word_data_size;  // word data's total size in .dict file 
    
    TODO: implement .idx special methods
    """
    
    def __init__(self, dict_prefix, container):
        
        idx_filename = '%s.idx' % dict_prefix
        idx_filename_gz = '%s.gz' % idx_filename
        
        try:
            file = open(idx_filename, 'rb')
        except IOError:
            try:
                file = gzip.open(idx_filename_gz, 'rb')
            except IOError:
                raise Exception('.idx file does not exists')
        
        # check file size
        self._file = file.read()
        if file.tell() != container.ifo.idxfilesize:
            raise Exception('size of the .idx file is incorrect')
        
        self._ifile = iter(self._file)
        #TODO: make class for idx entry 
        self._idx = {}
        entry = []
        word_str = ''
        for byte in self._ifile:
            
            # looping for word_str
            if byte == '\x00':
                entry.append(word_str)
                word_str = ''
            else:
                #TODO: handle encoding
                word_str += unpack('s', byte)[0]
                continue
            
            # reading word_data_offset
            word_data_offset_bytes = ''.join(
                [self._ifile.next() for i in range(
                    int(container.ifo.idxoffsetbits / 8))])
            word_data_offset = unpack('!L', word_data_offset_bytes)[0]
            entry.append(word_data_offset)
            
            # reading word_data_size
            word_data_size_bytes = ''.join(
                [self._ifile.next() for i in range(4)])
            word_data_size = unpack('!L', word_data_size_bytes)[0]
            entry.append(word_data_size)
            
            # saving line
            self._idx[entry[0]] = tuple(entry[1:])
            entry = []
    
    def __getitem__(self, word):
        """
        returns tuple (word_data_offset, word_data_size,) for word in .dict
        """
        return self._idx[word]

class _StarDictDict():
    #TODO: implement .dict special methods
    
    def __init__(self, dict_prefix, container):
        
        dict_filename = '%s.dict' % dict_prefix
        dict_filename_dz = '%s.dz' % dict_filename
        
        try:
            self._file = open(dict_filename)
        except IOError:
            try:
                self._file = gzip.open(dict_filename_dz)
            except IOError:
                raise Exception('.dict file does not exists')

class _StarDictSyn():
    #TODO: implement .syn special methods
    
    def __init__(self, dict_prefix, container):
        
        syn_filename = '%s.syn' % dict_prefix
       
        try:
            self._file = open(syn_filename)
        except IOError:
            # syn file is optional, passing silently
            pass

class Dictionary(dict):
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
        
        TODO: option to init from path to folder not from prefix
        """
        
        # reading somedict.ifo
        self.ifo = _StarDictIfo(dict_prefix=filename_prefix, container=self)
        
        # reading somedict.idx or somedict.idx.gz
        self.idx = _StarDictIdx(dict_prefix=filename_prefix, container=self)
        
        # reading somedict.dict or somedict.dict.dz
        self.dict = _StarDictDict(dict_prefix=filename_prefix, container=self)
        
        # reading somedict.syn (optional)
        self.syn = _StarDictSyn(dict_prefix=filename_prefix, container=self)
    
    def __cmp__(self, y):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
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

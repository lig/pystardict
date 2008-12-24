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
import gzip
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
    """
    def __init__(self, dict_prefix, container):
        
        ifo_filename = '%s.ifo' % dict_prefix
        
        try:
            _file = open(ifo_filename)
        except IOError:
            raise Exception('.ifo file does not exists')
        
        # skipping ifo header
        _file.readline()
        
        _line = _file.readline().split('=')
        if _line[0] == 'version':
            self.version = _line[1]
        else:
            raise Exception('ifo has invalid format')
        
        _config = {}
        for _line in _file:
            _line_splited = _line.split('=')
            _config[_line_splited[0]] = _line_splited[1]
        
        self.bookname = _config.get('bookname', None)
        if self.bookname is None: raise Exception('ifo has no bookname')
        
        self.wordcount = _config.get('wordcount', None)
        if self.wordcount is None: raise Exception('ifo has no wordcount')
        self.wordcount = int(self.wordcount)
        
        if self.version == '3.0.0':
            try:
                _syn = open('%s.syn' % dict_prefix)
                self.synwordcount = _config.get('synwordcount', None)
                if self.synwordcount is None:
                    raise Exception('ifo has no synwordcount but .syn file exists')
                self.synwordcount = int(self.synwordcount)
            except IOError:
                pass
        
        self.idxfilesize = _config.get('idxfilesize', None)
        if self.idxfilesize is None: raise Exception('ifo has no idxfilesize')
        self.idxfilesize = int(self.idxfilesize)
        
        self.idxoffsetbits = _config.get('idxoffsetbits', 32)
        self.idxoffsetbits = int(self.idxoffsetbits)
        
        self.author = _config.get('author', '')
        
        self.email = _config.get('email', '')
        
        self.website = _config.get('website', '')
        
        self.description = _config.get('description', '')
        
        self.date = _config.get('date', '')
        
        self.sametypesequence = _config.get('sametypesequence', '')

class _StarDictIdx():
    """
    The .idx file is just a word list.
    
    The word list is a sorted list of word entries.
    
    Each entry in the word list contains three fields, one after the other:
         word_str;  // a utf-8 string terminated by '\0'.
         word_data_offset;  // word data's offset in .dict file
         word_data_size;  // word data's total size in .dict file 
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
        self._idx = {}
        word_str = ''
        c = 0
        idx_offset_bytes_size = int(container.ifo.idxoffsetbits / 8)
        idx_offset_format = {4: 'L', 8: 'Q',}[idx_offset_bytes_size]
        idx_cords_bytes_size = idx_offset_bytes_size + 4
        for byte in self._ifile:
            
            # looping for word_str
            if byte == '\x00':
                
                # reading word_data_offset and word_data_size bytes
                word_data_cords_bytes = ''.join([self._ifile.next() for i in
                    range(idx_cords_bytes_size)])
                
                # unpacking record values
                record_tuple = unpack('!%sc%sL' % (c, idx_offset_format),
                    word_str + word_data_cords_bytes)
                word, cords = record_tuple[:c], record_tuple[c:]
                
                # saving line
                self._idx[word] = cords
                
                word_str = ''
                c = 0
            else:
                word_str += byte
                c += 1
                continue
                        
    
    def __getitem__(self, word):
        """
        returns tuple (word_data_offset, word_data_size,) for word in .dict
        
        @note: here may be placed flexible search realization
        """
        return self._idx[tuple(word)]

class _StarDictDict():
    """
    The .dict file is a pure data sequence, as the offset and size of each
    word is recorded in the corresponding .idx file.
    
    If the "sametypesequence" option is not used in the .ifo file, then
    the .dict file has fields in the following order:
    ==============
    word_1_data_1_type; // a single char identifying the data type
    word_1_data_1_data; // the data
    word_1_data_2_type;
    word_1_data_2_data;
    ...... // the number of data entries for each word is determined by
           // word_data_size in .idx file
    word_2_data_1_type;
    word_2_data_1_data;
    ......
    ==============
    It's important to note that each field in each word indicates its
    own length, as described below.  The number of possible fields per
    word is also not fixed, and is determined by simply reading data until
    you've read word_data_size bytes for that word.
    
    
    Suppose the "sametypesequence" option is used in the .idx file, and
    the option is set like this:
    sametypesequence=tm
    Then the .dict file will look like this:
    ==============
    word_1_data_1_data
    word_1_data_2_data
    word_2_data_1_data
    word_2_data_2_data
    ......
    ==============
    The first data entry for each word will have a terminating '\0', but
    the second entry will not have a terminating '\0'.  The omissions of
    the type chars and of the last field's size information are the
    optimizations required by the "sametypesequence" option described
    above.
    
    If "idxoffsetbits=64", the file size of the .dict file will be bigger 
    than 4G. Because we often need to mmap this large file, and there is 
    a 4G maximum virtual memory space limit in a process on the 32 bits 
    computer, which will make we can get error, so "idxoffsetbits=64" 
    dictionary can't be loaded in 32 bits machine in fact, StarDict will 
    simply print a warning in this case when loading. 64-bits computers 
    should haven't this limit.
    
    Type identifiers
    ----------------
    Here are the single-character type identifiers that may be used with
    the "sametypesequence" option in the .idx file, or may appear in the
    dict file itself if the "sametypesequence" option is not used.
    
    Lower-case characters signify that a field's size is determined by a
    terminating '\0', while upper-case characters indicate that the data
    begins with a network byte-ordered guint32 that gives the length of 
    the following data's size(NOT the whole size which is 4 bytes bigger).
    
    'm'
    Word's pure text meaning.
    The data should be a utf-8 string ending with '\0'.
    
    'l'
    Word's pure text meaning.
    The data is NOT a utf-8 string, but is instead a string in locale
    encoding, ending with '\0'.  Sometimes using this type will save disk
    space, but its use is discouraged.
    
    'g'
    A utf-8 string which is marked up with the Pango text markup language.
    For more information about this markup language, See the "Pango
    Reference Manual."
    You might have it installed locally at:
    file:///usr/share/gtk-doc/html/pango/PangoMarkupFormat.html
    
    't'
    English phonetic string.
    The data should be a utf-8 string ending with '\0'.
    
    Here are some utf-8 phonetic characters:
    θʃŋʧðʒæıʌʊɒɛəɑɜɔˌˈːˑṃṇḷ
    æɑɒʌәєŋvθðʃʒɚːɡˏˊˋ
    
    'x'
    A utf-8 string which is marked up with the xdxf language.
    See http://xdxf.sourceforge.net
    StarDict have these extention:
    <rref> can have "type" attribute, it can be "image", "sound", "video" 
    and "attach".
    <kref> can have "k" attribute.
    
    'y'
    Chinese YinBiao or Japanese KANA.
    The data should be a utf-8 string ending with '\0'.
    
    'k'
    KingSoft PowerWord's data. The data is a utf-8 string ending with '\0'.
    It is in XML format.
    
    'w'
    MediaWiki markup language.
    See http://meta.wikimedia.org/wiki/Help:Editing#The_wiki_markup
    
    'h'
    Html codes.
    
    'r'
    Resource file list.
    The content can be:
    img:pic/example.jpg     // Image file
    snd:apple.wav           // Sound file
    vdo:film.avi            // Video file
    att:file.bin            // Attachment file
    More than one line is supported as a list of available files.
    StarDict will find the files in the Resource Storage.
    The image will be shown, the sound file will have a play button.
    You can "save as" the attachment file and so on.
    
    'W'
    wav file.
    The data begins with a network byte-ordered guint32 to identify the wav
    file's size, immediately followed by the file's content.
    
    'P'
    Picture file.
    The data begins with a network byte-ordered guint32 to identify the picture
    file's size, immediately followed by the file's content.
    
    'X'
    this type identifier is reserved for experimental extensions.
    """
    
    def __init__(self, dict_prefix, container):
        """
        opens regular or dziped .dict file 
        """
        self._container = container
        
        dict_filename = '%s.dict' % dict_prefix
        dict_filename_dz = '%s.dz' % dict_filename
        
        try:
            self._file = open(dict_filename, 'rb')
        except IOError:
            try:
                self._file = gzip.open(dict_filename_dz, 'rb')
            except IOError:
                raise Exception('.dict file does not exists')
    
    def __getitem__(self, word):
        """
        returns data from .dict for word
        """
        
        # getting word data coordinats
        cords = self._container.idx[word]
        
        # seeking in file for data
        self._file.seek(cords[0])
        
        # reading data
        bytes = self._file.read(cords[1])
        
        #@todo: handle multifield data
        #@todo: handle encoding. it seems to be working as is but i'm not sure 
        return bytes

class _StarDictSyn():
    #@todo: implement .syn special methods
    
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
        
        @todo: option to init from path to folder not from prefix
        """
        
        # reading somedict.ifo
        self.ifo = _StarDictIfo(dict_prefix=filename_prefix, container=self)
        
        # reading somedict.idx or somedict.idx.gz
        self.idx = _StarDictIdx(dict_prefix=filename_prefix, container=self)
        
        # reading somedict.dict or somedict.dict.dz
        self.dict = _StarDictDict(dict_prefix=filename_prefix, container=self)
        
        # reading somedict.syn (optional)
        self.syn = _StarDictSyn(dict_prefix=filename_prefix, container=self)
        
        # initializing cache
        self._dict_cache = {}
    
    def __cmp__(self, y):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __contains__(self, k):
        """
        returns True if x.idx has a word k, else False
        
        @todo: implement me
        """
        pass
    
    def __delitem__(self, k):
        """
        frees cache from word k translation
        
        @todo: implement me
        """
        pass
    
    def __eq__(self, y):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __ge__(self, y):
        """
        raises NotImplemented exception
        """
        raise NotImplementedError()
    
    def __getitem__(self, k):
        """
        returns translation for word k from cache or not and then caches
        """
        if k in self._dict_cache:
            return self._dict_cache[k]
        else:
            value = self.dict[k]
            self._dict_cache[k] = value
            return value
    
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
        
        @todo: implement me
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
        
        @todo: implement me
        """
        pass
    
    def __repr__(self):
        """
        returns classname and bookname parameter of the x.ifo
        
        @todo: implement me
        """
        pass
    
    def __setitem__(self, k, v):
        """
        sets translation of the word k to v
        
        @todo: implement me
        """
        pass
    
    def clear(self):
        """
        unlike dict class resets dictionary to the original state, i.e. clears
        all of the blacklisting info or reverts changed values 
        
        @todo: implement me
        """
        pass
    
    def get(self, k, d=''):
        """
        returns translation of the word k from self.dict or d if k not in x.idx
        
        d defaults to empty string
        
        @todo: implement me
        """
        pass
    
    def has_key(self, k):
        """
        returns True if self.idx has a word k, else False
        
        @todo: implement me
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
        
        @todo: implement me
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

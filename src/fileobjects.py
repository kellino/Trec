#!/usr/bin/python2.7


class VecObject():
    # the VecObject is a generic data type suitable for storing the information
    # from either the document vector file or the query file
    # terms and term_frequencies are both lists of integers, ID is either the
    # query number or the clueweb id
    def __init__(self, ID=None, terms=None, term_frequencies=None):
        self.ID = ID
        self.terms = terms
        self.term_frequencies = term_frequencies


class Doc():
    # class specifically for use with the portfolio implementation
    def __init__(self, ID=None, terms=None, term_frequencies=None, bm25=None, altered=None):
        self.ID = ID
        self.terms = terms
        self.term_frequencies = term_frequencies
        self.bm25 = bm25
        self.altered = altered

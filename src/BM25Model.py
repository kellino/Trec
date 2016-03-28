#!/usr/bin/python2.7
from math import log
from filehandler_vers2 import FileHandler
from fileobjects import VecObject
from sys import exit
from collections import OrderedDict

doc_collection = dict()
query_collection = OrderedDict()
idfs = dict()
term_totals = dict()


class Doc(VecObject):
    # inherits from generic VecObject, and adds a doc length attribute - useful
    # when calculating the bm25 score
    def __init__(self, doc_length=None):
        VecObject.__init__(self)
        self.doc_length = doc_length


class Query():
    def __init__(self, queryNo=None, terms=None,
                 term_frequency=None):
        self.queryNo = queryNo
        self.terms = terms
        self.term_frequency = term_frequency


class BM25():

    def get_doc_lengths(self):
        for k, doc in doc_collection.iteritems():
            doc.doc_length = sum(doc.term_frequencies)

    def get_average_doc_length(self):
        # sum the doc lengths of everything in the dictionary, and divide
        # by length of dictionary
        return (sum([v.doc_length for k, v in doc_collection.iteritems()]) /
                len(doc_collection))

    def get_term_totals(self):
        # gets the total number of occurrences of each term in the collection
        # slightly wasteful of memory, as it is really only necessary to
        # get the terms totals of query items
        for k, doc in doc_collection.iteritems():
            for i in range(len(doc.terms)):
                # if term already in dictionary, add the frequency of term to
                # total
                if doc.terms[i] in term_totals:
                    term_totals[doc.terms[i]] += doc.term_frequencies[i]
                # if term not in dictionary, initialize with the term frequency
                else:
                    term_totals[doc.terms[i]] = doc.term_frequencies[i]

    def calculate_idf_of_terms(self, N):
        # calculate the inverse document frequency of each term in the query
        for k, query in query_collection.iteritems():
            for q in query.terms:
                nqi = term_totals.get(q)
                partial = (N - nqi + 0.5) / (nqi + 0.5)
                if partial >= 0.0:
                    idf = log(partial, 2)
                    if idf > 0.0:
                        idfs[q] = idf
                    else:
                        idfs[q] = 0.0

    def calculate_bm25(self, query, avdl, k, b):
        # query vector
        q_vec = [q for q in query.terms]
        # idfs of query vector
        idf_of_q = [idfs.get(q) for q in q_vec]
        print q_vec, idf_of_q
        # for k, doc in doc_collection.iteritems():
            # doc_vec = []        # holds the frequencies of the search terms
            # for q in q_vec:
                # if q in doc.terms:
                    # doc_vec.append(doc.term_frequencies[doc.terms.index(q)])
            # try:
                # bm25 = sum(map(
                    # (lambda x, y: x * (y * (k+1) / y + k *
                                       # (1 - b + b * (doc.doc_length / avdl)))),
                    # idf_of_q, doc_vec))
                # print query.queryNo, doc.docID, bm25
            # except:
                # pass

if __name__ == '__main__':
    try:
        f = FileHandler()
        b = BM25()
        query_file = open(f.find_file("query_term_vectors", "*.dat"))
        doc_file = open(f.find_file("document_term_vectors", "*.dat"))
        f.fill_dictionary(doc_file, doc_collection)
        f.fill_dictionary(query_file, query_collection)
    except:
        print("unexpected error reading from files")
        exit()
    finally:
        # close open files
        f.close_file(query_file)
        f.close_file(doc_file)
    b.get_doc_lengths()
    avdl = b.get_average_doc_length()
    b.get_term_totals()
    N = len(doc_collection)
    b.calculate_idf_of_terms(N)
    for k, v in idfs.iteritems():
        print k, v
    for k, v in query_collection.iteritems():
        b.calculate_bm25(v, avdl, 1.5, 0.75)

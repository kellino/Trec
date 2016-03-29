#!/usr/bin/python2.7
from math import log
from filehandler_vers2 import FileHandler
from sys import exit
from collections import OrderedDict
from operator import itemgetter

doc_collection = dict()
query_collection = OrderedDict()
idfs = dict()
term_totals = dict()


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
                # if a term appears in the document, increment the count
                if doc.terms[i] in term_totals:
                    term_totals[doc.terms[i]] += 1
                # if term not in dictionary, initialize with the term frequency
                else:
                    term_totals[doc.terms[i]] = 1

    def calculate_idf_of_terms(self, N):
        # calculate the inverse document frequency of each term in the query
        # IDFt = log10(N/nt)
        for k, query in query_collection.iteritems():
            for q in query.terms:
                nt = term_totals.get(q)
                idfs[q] = log(N / nt)

    def calculate_bm25(self, query, avdl, k, b):
        order = []
        for i, doc in doc_collection.iteritems():
            # f(qi, D)
            t_freq = []
            for q in query.terms:
                if q in doc.terms:
                    t_freq.append(doc.term_frequencies[doc.terms.index(q)])
                else:
                    t_freq.append(0)
            # IDF(qi)
            idf_list = []
            for j in range(len(query.terms)):
                idf_list.append(idfs.get(query.terms[j]))
            s = sum(map((lambda idf, fq: idf * (k + 1) / (fq + (k * (
                1 - b + (b * (doc.doc_length / avdl)))))), idf_list, t_freq))
            order.append([query.ID, doc.ID, s])
        order.sort(key=itemgetter(2), reverse=True)
        for o in order:
            print o[0], o[1], o[2]


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
    for k, v in query_collection.iteritems():
        b.calculate_bm25(v, avdl, 1.5, 0.75)

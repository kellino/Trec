#!/usr/bin/python2.7
from filehandler import FileHandler
import pandas as pd


class Portfolio():

    def __init__(self):
        self.ordered = dict()
        self.docs = dict()
        self.queries = dict()
        self.top_results = dict()

    def calc_pearson(self, queryNo, doc1, doc2):
        d1 = pd.Series(doc1.term_frequencies)
        d2 = pd.Series(doc2.term_frequencies)
        num = pd.Series.cov(d1, d2)
        denom = (pd.Series.std(d1) * pd.Series.std(d2))
        return num / denom

    def calc_mva(self, query, doc, ind):
        b = 4
        if len(self.ordered) == 0:
            doc.altered = (float(doc.bm25)) - (b * ind) - 2*b
            self.ordered[doc.ID] = doc
        else:
            doc.altered = float(doc.bm25) - (b * ind) \
                - 2*b * (sum(map((lambda x: self.calc_pearson
                                 (query, doc, x)), self.ordered.values())))
            self.ordered[doc.ID] = doc

if __name__ == '__main__':
    f = FileHandler()
    p = Portfolio()
    query_file = open(f.find_file('query_term_vectors', '*.dat'))
    doc_file = open(f.find_file('document_term_vectors', '*.dat'))
    results_file = open(r'/home/david/Documents/data_retrieval'
                        r'/coursework/BM25b0.75_0.res')
    f.fill_dictionary(doc_file, p.docs)
    f.fill_dictionary(query_file, p.queries)
    res = f.top_results_from_file_with_bm25(results_file, p.docs, 100)
    f.close_file(query_file)
    f.close_file(doc_file)
    f.close_file(results_file)
    for k, v in res.iteritems():
        i = 0
        for vi in v:
            p.calc_mva(k, vi, i)
            i += 1
        for m, n in p.ordered.iteritems():
            print k, m, n.altered
        p.ordered.clear()

#!/usr/bin/python2.7
from filehandler import FileHandler
from math import log
import numpy as np
from ast import literal_eval

DEBUG = True
queries = dict()
docs = dict()
top_results = dict()
idfs = dict()


class MMR():

    def calc_mmr(self, queryNo, lam):
        ordered = dict()
        # check that the query exists in top_results, if not, exit the function
        if top_results.get(queryNo) is None:
            pass
        else:
            # all the top k vector objects for queryNo
            results = [docs[top_results.get(queryNo)[i]] for i in range(
                len(top_results.get(queryNo)))]
            # the query vector under consideration
            query = (queries.get(str(queryNo)))
            # calculate the mmr for each doc in relation to the query
            for i in range(100):
                if len(ordered) > 0:
                    sim = self._get_similarity(query, results[i])
                    sim_max = max(map(
                        (lambda (k, v): self._get_similarity
                            (results[i], v)), ordered.iteritems()))
                    mmr = (lam * sim) - ((1 - lam) * sim_max)
                    ordered[mmr] = results[i]
                else:
                    sim_max = self._get_similarity(query, results[i])
                    ordered[sim_max] = results[i]
        if DEBUG:
            for k, v in ordered.iteritems():
                print queryNo, v.ID, k

    def get_similarity(self, query, doc):
        # make a numpy array of terms and term frequencies
        d_matrix = np.array([doc.terms, doc.term_frequencies])
        # term frequencies of those terms present in both query and doc
        intersection = []
        for q in query.terms:
            if q in d_matrix[0]:
                i = np.nonzero(d_matrix[0] == q)
                # the triple indexing here seems strange, but numpy returns a
                # matrix rather than an int if we index it twice, so the third
                # '0' index extracts the result from its context
                # intersection.append(d_matrix[1][i][0])
                tf = 1 + log(d_matrix[1][i][0])
                intersection.append(tf)
            else:
                intersection.append(0)
        print intersection

if __name__ == '__main__':
    f = FileHandler()
    M = MMR()
    query_file = open(f.find_file('query_term_vectors', '*.dat'))
    doc_file = open(f.find_file('document_term_vectors', '*.dat'))
    results_file = open(r'/home/david/Documents/data_retrieval'
                        r'/coursework/BM25b0.75_0.res')
    # TODO cache the calculations from the bm25 so we don't have to
    # keep running the bloody thing. Tidy this code away
    with open('./idfs_cached', 'r') as idf_file:
        s = idf_file.read()
        idfs = literal_eval(s)
    f.fill_dictionary(doc_file, docs)
    f.fill_dictionary(query_file, queries)
    top_results = f.top_results_from_file(results_file, 100)
    f.close_file(query_file)
    f.close_file(doc_file)
    f.close_file(results_file)
    for k, query in queries.iteritems():
        for d, doc in docs.iteritems():
            M.get_similarity(query, doc)

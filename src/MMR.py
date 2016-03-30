#!/usr/bin/python2.7
from filehandler import FileHandler
from math import log10, sqrt
import numpy as np
from collections import OrderedDict
from ast import literal_eval

DEBUG = True
queries = OrderedDict()
docs = OrderedDict()
top_results = OrderedDict()
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
        # log frequency weighting of doc vector
        lfw_of_doc = []
        # log freqency weighting of query vector, as all query terms appear
        # only once in the vector this is a slightly redundant calculation
        # for this exercise, but it adds flexibility
        lfw_of_query = [1 + log10(q) for q in query.terms[0]]
        for q in query.terms[0]:
            if q in doc.terms[0]:
                i = np.nonzero(doc.terms[0] == q)[0][0]
                tf = 1 + log10(doc.terms[1][i])
                lfw_of_doc.append(tf)
            else:
                # term is not in doc vector, therefore 0
                lfw_of_doc.append(0)
        normalizer_doc = sqrt(sum(map((lambda x: x*x), lfw_of_doc)))
        if normalizer_doc == 0:
            # there is no cosine similarity, so return 0 now
            return 0
        else:
            normalizer_query = sqrt(sum(map((lambda x: x*x), lfw_of_query)))
            n_doc = [t / normalizer_doc for t in lfw_of_doc]
            n_query = [t / normalizer_query for t in lfw_of_query]
            return sum([x * y for x, y in zip(n_doc, n_query)])


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
    f.fill_dict_np(doc_file, docs)
    f.fill_dict_np(query_file, queries)
    top_results = f.top_results_from_file(results_file, 100)
    f.close_file(query_file)
    f.close_file(doc_file)
    f.close_file(results_file)
    for k, query in queries.iteritems():
        for d, doc in docs.iteritems():
            cos = M.get_similarity(query, doc)
            print k, doc.ID, cos

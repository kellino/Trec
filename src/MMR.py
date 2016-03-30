#!/usr/bin/python2.7
from filehandler import FileHandler
from math import log10, sqrt
import numpy as np
from collections import OrderedDict
import operator
from ast import literal_eval

queries = OrderedDict()
docs = dict()
idfs = dict()
top = OrderedDict()


class MMR():

    def calc_mmr(self, query, lamba_value):
        scored = dict()
        to_check = top.get(int(query.ID))
        if to_check:
            for doc in to_check:
                if len(scored) == 0:
                    scored[doc] = lamba_value * self.get_similarity(query, doc)
                else:
                    in_dict = [k for k, v in scored.iteritems()]
                    scored[doc] = lamba_value * self.get_similarity(query, doc) - (1 - lamba_value) * max(map(lambda x: self.get_similarity(doc, x), in_dict))
            sorted_scores = reversed(sorted(scored.items(), key=operator.itemgetter(1)))
            for score in sorted_scores:
                print query.ID, score[0].ID, score[1]

    def get_similarity(self, query, doc):
        # log frequency weighting of doc vector
        lfw_of_doc = []
        lfw_of_query = [1 + log10(q) for q in query.terms[1]]
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
    # initialize everything
    f = FileHandler()
    M = MMR()
    query_file = open(f.find_file('query_term_vectors', '*.dat'))
    doc_file = open(f.find_file('document_term_vectors', '*.dat'))
    results_file = open(r'/home/david/Documents/data_retrieval'
                        r'/coursework/BM25b0.75_0.res')
    # TODO check this file exists
    with open('./idfs_cached', 'r') as idf_file:
        s = idf_file.read()
        idfs = literal_eval(s)
    f.fill_dict_np(doc_file, docs)
    f.fill_dict_np(query_file, queries)
    # tidy up
    f.close_file(query_file)
    f.close_file(doc_file)

    # main starts here
    # get the top results for each query (as a string) and fill and ordered
    # dictionary with the results as vector objects
    top_results = f.top_results_from_file(results_file, 100)
    # tidy up
    f.close_file(results_file)
    for k, result in top_results.iteritems():
        group = []
        for r in result:
            group.append(docs.get(r))
        top[k] = group
    # for k, v in top.iteritems():
        # print k, len(v)
    for i in range(201, 251):
        M.calc_mmr(queries.get(str(i)), 0.5)

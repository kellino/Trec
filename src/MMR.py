#!/usr/bin/python2.7
from filehandler import FileHandler
from math import sqrt
# import numpy as np

queries = dict()
docs = dict()
top_results = dict()


def top_results_from_file(results_file, k):
    """ extracts the top k results for each query from a formatted file """
    # read file into an array
    rf = []
    for l in results_file:
        rf.append(l)
    # extract the top 100 results for each query and add them to a dictionary
    # of top results, with query number as key
    for i in range(201, 251):  # TODO query nums should not be hard coded
        group = [line.strip() for line in rf if line.startswith(str(i))][:k]
        # some queries don't exist, so check to make sure group is not empty
        # before adding them to the top_results dictionary
        if len(group) > 0:
            # list of clueweb doc ids
            names = []
            for g in group:
                p = g.split()
                names.append(p[2])
            top_results[i] = names


def mmr(queryNo, lam):
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
                sim = get_similarity(query, results[i])
                sim_max = max(map(
                    (lambda (k, v): get_similarity
                     (results[i], v)), ordered.iteritems()))
                mmr = (lam * sim) - ((1 - lam) * sim_max)
                ordered[mmr] = results[i]
            else:
                sim_max = get_similarity(query, results[i])
                ordered[sim_max] = results[i]
    for k, v in ordered.iteritems():
        print queryNo, v.ID, k


def get_similarity(query, doc2):
    vector = set(query.terms).intersection(doc2.terms)
    root_indices = [query.terms.index(v) for v in vector]
    r_indices = [doc2.terms.index(v) for v in vector]
    root_frequencies = [query.term_frequencies[j] for j in root_indices]
    r_frequencies = [doc2.term_frequencies[k] for k in r_indices]
    numerator = sum(map((lambda x, y: x*y),
                        root_frequencies, r_frequencies))
    denominator = (sqrt(sum([x*x for x in query.term_frequencies]))
                   * sqrt(sum(y*y for y in doc2.term_frequencies)))
    return numerator / denominator


if __name__ == '__main__':
    f = FileHandler()
    query_file = open(f.find_file('query_term_vectors', '*.dat'))
    doc_file = open(f.find_file('document_term_vectors', '*.dat'))
    results_file = open(r'/home/david/Documents/data_retrieval'
                        r'/coursework/BM25b0.75_0.res')
    f.fill_dictionary(doc_file, docs)
    f.fill_dictionary(query_file, queries)
    top_results_from_file(results_file, 100)
    f.close_file(query_file)
    f.close_file(doc_file)
    f.close_file(results_file)
    for i in range(201, 251):
        mmr(i, 0.25)

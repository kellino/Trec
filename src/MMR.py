#!/usr/bin/python2.7
from filehandler import FileHandler
from math import sqrt

DEBUG = True
queries = dict()
docs = dict()
top_results = dict()


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

    def _get_similarity(self, query, doc2):
        vector = set(query.terms).intersection(doc2.terms)
        # this is the bottleneck right here. How can this be rewritten?
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
    M = MMR()
    query_file = open(f.find_file('query_term_vectors', '*.dat'))
    doc_file = open(f.find_file('document_term_vectors', '*.dat'))
    results_file = open(r'/home/david/Documents/data_retrieval'
                        r'/coursework/BM25b0.75_0.res')
    f.fill_dictionary(doc_file, docs)
    f.fill_dictionary(query_file, queries)
    top_results = f.top_results_from_file(results_file, 100)
    f.close_file(query_file)
    f.close_file(doc_file)
    f.close_file(results_file)
    # M.calc_mmr(201, 0.5)
    for i in range(201, 251):
        M.calc_mmr(i, 0.25)

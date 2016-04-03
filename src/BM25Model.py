#!/usr/bin/env python2.7
import numpy as np
from collections import OrderedDict


class BM25():
    def __init__(self):
        self.total_words = 0
        self.docs = dict()
        self.term_appearances = dict()
        self.query_vecs = OrderedDict()
        self.avdl = 0

    def get_doc_vecs(self):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/document_term_vectors.dat') as ifile:
            for line in ifile:
                terms = []
                term_frequencies = []
                tokens = line.strip().split()
                for token in tokens[1:]:
                    if ':' in token:
                        nums = token.strip().split(':')
                        terms.append(int(nums[0]))
                        term_frequencies.append(int(nums[1]))
                        if int(nums[0]) in self.term_appearances:
                            self.term_appearances[int(nums[0])] += 1
                        else:
                            self.term_appearances[int(nums[0])] = 1
                # add the documents vectors to the docs dictionary
                self.docs[tokens[0]] = np.array([terms, term_frequencies])
                self.total_words += np.sum(term_frequencies)

    def get_query_vecs(self):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/query_term_vectors.dat') as ifile:
            for line in ifile:
                terms = []
                term_frequencies = []
                tokens = line.strip().split()
                for token in tokens[1:]:
                    if ':' in token:
                        nums = token.strip().split(':')
                        terms.append(int(nums[0]))
                        term_frequencies.append(int(nums[1]))
                self.query_vecs[int(tokens[0])] = np.array(
                    [terms, term_frequencies])

    def calc_bm25(self, query_vec, doc_vec, b, k):
        L = np.sum(doc_vec[1]) / self.avdl
        K = k * ((1 - b) + (b * L))
        vec_intersection = np.in1d(doc_vec[0], query_vec[0])
        if vec_intersection.any():
            term_frequencies = [self.term_appearances.get(y)
                                for y in doc_vec[0][vec_intersection]]
            bm25 = np.sum(map((lambda x, y: (x / x + K) *
                              (np.log2((len(self.docs) - y + 0.5) /
                                       (y + 0.5)))),
                              doc_vec[1][vec_intersection],
                              term_frequencies))
        else:
            bm25 = 0.0
            term_frequencies = []
        return L, K, term_frequencies, bm25

    def run(self, b, k):
        to_write = []
        for query, query_vec in self.query_vecs.iteritems():
            results = []
            for doc, doc_vec in self.docs.iteritems():
                L, K, term_frequencies, bm25 = self.calc_bm25(
                    query_vec, doc_vec, b, k)
                results.append((doc, bm25))
            rs = sorted(results, key=lambda bm25: bm25[1])
            rs.reverse()
            for i in range(100):
                line = "{} Q0 {} {} {} BM25b{}".format(
                    query, rs[i][0], i+1, rs[i][1], b)
                to_write.append(line)
        return to_write

if __name__ == '__main__':
    b = BM25()
    b.get_doc_vecs()
    b.get_query_vecs()
    b.avdl = b.total_words / float(len(b.docs))
    results = b.run(0.75, 1.5)
    with open('./BM25b0.75results', 'w') as ifile:
        ifile.writelines("%s\n" % item for item in results)

#!/usr/bin/env python2.7
import numpy as np
from collections import OrderedDict

query_nums = []
docIDs = []
bm25 = []

with open(r'/home/david/Documents/data_retrieval'
          r'/coursework/BM25b0.75_0.res') as ifile:
    for line in ifile:
        tokens = line.strip().split()
        query_nums.append(int(tokens[0]))
        docIDs.append(tokens[2])
        bm25.append(float(tokens[4]))

query_nums = np.array(query_nums)
docIDs = np.array(docIDs)
bm25 = np.array(bm25)

total_words = 0
docs = dict()
term_appearances = dict()
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
                if int(nums[0]) in term_appearances:
                    term_appearances[int(nums[0])] += 1
                else:
                    term_appearances[int(nums[0])] = 1
        # add the documents vectors to the docs dictionary
        docs[tokens[0]] = np.array([terms, term_frequencies])
        total_words += np.sum(term_frequencies)

query_vecs = OrderedDict()
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
        query_vecs[int(tokens[0])] = np.array([terms, term_frequencies])


def calc_bm25(query_vec, doc_vec, b, k):
    L = np.sum(doc_vec[1]) / avdl
    K = k * ((1 - b) + (b * L))
    vec_intersection = np.in1d(doc_vec[0], query_vec[0])
    if vec_intersection.any():
        term_frequencies = [term_appearances.get(y)
                            for y in doc_vec[0][vec_intersection]]
        bm25 = np.sum(map((lambda x, y: (x / x + K) *
                           (np.log2((len(docs) - y + 0.5) / (y + 0.5)))),
                          doc_vec[1][vec_intersection], term_frequencies))
    else:
        bm25 = 0.0
        term_frequencies = []
    return L, K, term_frequencies, bm25


avdl = total_words / float(len(docs))
for query, query_vec in query_vecs.iteritems():
    results = []
    for doc, doc_vec in docs.iteritems():
        L, K, term_frequencies, bm25 = calc_bm25(query_vec, doc_vec, 0.75, 1.5)
        results.append((doc, bm25))
    rs = sorted(results, key=lambda bm25: bm25[1])
    rs.reverse()
    for i in range(100):
        print query, "Q0", rs[i][0], i+1, rs[i][1], "BM25b0.75"

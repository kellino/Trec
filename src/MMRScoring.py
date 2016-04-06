#!/usr/bin/env python2.7
import numpy as np
from scipy import spatial
from sklearn.preprocessing import normalize
from itertools import islice
from operator import itemgetter


class MMR():
    def __init__(self):
        self.pages = dict()
        self.scores = []
        self.docIDs = []
        self.queries = []

    def get_bm25_scores(self):
        with open('./BM25b0.75.res') as ifile:
            for line in ifile:
                tokens = line.strip().split()
                # self.scores.append((tokens[2], float(tokens[4])))
                self.queries.append(int(tokens[0]))
                self.docIDs.append(tokens[2])
                self.scores.append(float(tokens[4]))
            self.queries = np.array(self.queries)
            self.docIDs = np.array(self.docIDs)
            self.scores = np.array(self.scores)

    def get_pages(self):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/document_term_vectors.dat') as ifile:
            while True:
                next_n_lines = list(islice(ifile, 5000))
                if not next_n_lines:
                    break
                else:
                    for line in next_n_lines:
                        terms = dict()
                        tokens = line.strip().split()
                        for token in tokens[1:]:
                            nums = token.strip().split(':')
                            terms[int(nums[0])] = int(nums[1])
                        self.pages[tokens[0]] = terms

    def normalize_vectors(self, doc1, doc2):
        # a list of term frequencies of the intersection of doc1 and doc2
        temp = []
        for k, v in doc1.iteritems():
            if k in doc2:
                temp.append(doc1.get(k))
            else:
                temp.append(0)
        return temp

    def get_cosine_similarity(self, doc1, doc2):
        temp1 = [x for k, x in doc1.iteritems()]
        temp2 = self.normalize_vectors(doc1, doc2)
        return 1 - spatial.distance.cosine(temp1, temp2)

    def run(self, l, query):
        results_set = []
        if query in m.queries:
            is_query = (m.queries == query)
            rels = m.docIDs[is_query]
            scores = m.scores[is_query]
            n_scores = normalize(scores.reshape(1, -1))[0]
            # as there is no comparison to make, add the first doc from rels
            # to the new results set
            for i in range(len(rels)):
                if i == 0:
                    new_score = l * n_scores[i] - (1 - l)
                    # results set contains a tuple of the form
                    # (query numbers, docID, adjusted score)
                    results_set.append((query, rels[i], i, scores[i], new_score))
                else:
                    # fetch tf dict of next document
                    to_score = m.pages.get(rels[i])
                    # get the term frequency vector from the to_score dict
                    new_score = (l * n_scores[i] - ((1 - l) * max
                                 (map((lambda (a, b, c, d, e): m.get_cosine_similarity
                                       (to_score, m.pages.get(b))),
                                      results_set))))
                    results_set.append((query, rels[i], i, scores[i], new_score))
        return results_set

if __name__ == '__main__':
    m = MMR()
    m.get_bm25_scores()
    m.get_pages()
    l_values = [0.25, 0.5]
    for l in l_values:
        lines = []
        for query in range(201, 251):
            res = m.run(l, query)
            rs = sorted(res, key=itemgetter(4))
            rs.reverse()
            for r in rs:
                lines.append("{} Q0 {} {} {} MMRlambda0.25".format(
                    r[0], r[1], r[2], r[3]))
        with open('./MMRScoring{}.res'.format(l), 'a') as ifile:
            ifile.writelines("%s\n" % s for s in lines)

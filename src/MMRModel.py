#!/usr/bin/env python2.7
import numpy as np
from scipy import spatial
from sklearn.preprocessing import normalize
from itertools import islice


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
        temp = []
        for k, v in doc1.iteritems():
            if k in doc2:
                temp.append(doc1.get(k))
            else:
                temp.append(0)
        return temp

    def get_cosine_similarity(self, doc1, doc2):
        return spatial.distance.cosine(doc1, doc2)

if __name__ == '__main__':
    m = MMR()
    m.get_bm25_scores()
    m.get_pages()
    l = 0.25
    for query in range(201, 251):
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
                    results_set.append((query, rels[i], new_score))
                else:
                    new_score = (l * n_scores[i] - ((1 - l) * max(map((lambda(a, b, x): m.get_cosine_similarity(n_scores[i], x)), results_set))))
                    results_set.append((query, rels[i], new_score))
            print results_set
    # with open('./mmr_results', 'a') as f:
        # f.writelines("%s\n" % p for p in cosines)

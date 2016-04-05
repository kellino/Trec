#!/usr/bin/env python2.7
import numpy as np
from scipy import spatial
from itertools import islice


class MMR():
    def __init__(self):
        self.pages = dict()
        self.scores = []

    def get_bm25_scores(self):
        with open('./bm25sample') as ifile:
            for line in ifile:
                tokens = line.strip().split()
                self.scores.append((tokens[2], float(tokens[4])))

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

    def calc_mmr(self, l, doc, bm25, returns):
        mmr = (l * bm25 - (1 - l) *
               max(map(lambda d: self.get_cosine_similarity(doc, d)), returns))
        return mmr

if __name__ == '__main__':
    m = MMR()
    m.get_bm25_scores()
    m.get_pages()
    for i in range(len(m.scores) - 1):
        cosines = []
        r = m.pages.get(m.scores[i][0])
        for j in range(i+1, len(m.scores)):
            tf = m.normalize_vectors(r, m.pages.get(m.scores[j][0]))
            root = np.array([x for k, x in r.iteritems()])
            cos = m.get_cosine_similarity(root, tf)
            cosines.append(cos)
        print max(cosines)

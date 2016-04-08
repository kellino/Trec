#!/usr/bin/env python2.7
from __future__ import division
import numpy as np
from scipy import stats
from itertools import islice
from operator import itemgetter

# even slower than MMR!!!


class Portfolio():
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
        temp = [v for k, v in doc1.iteritems()]
        temp2 = []
        for k, v in doc1.iteritems():
            if k in doc2:
                temp2.append(doc1.get(k))
            else:
                temp2.append(0)
        return temp, temp2

    def calc_pearsons(self, doc1, doc2):
        temp, temp2 = self.normalize_vectors(doc1, doc2)
        return stats.pearsonr(temp, temp2)[1]

    def run(self, b, query):
        results = []
        if query in self.queries:
            is_query = (self.queries == query)
            rels = self.docIDs[is_query][:100]
            scores = self.scores[is_query][:100]
            for i in range(len(rels)):
                wi = 1.0 / 2**(i+1)
                if i == 0:
                    mva = scores[i] - (b * wi)
                    results.append((query, rels[i], i+1, mva))
                else:
                    to_compare = [self.pages.get(e) for (a, e, c, d) in results]
                    order = [j for j in range(1, len(results)+1)]
                    mva = scores[i] - (b * wi) - (2 * b * np.sum(map((lambda x, y: (1.0/x**2) * self.calc_pearsons(self.pages.get(rels[i]), y)), order, to_compare)))
                    results.append((query, rels[i], i+1, mva))
        return results


if __name__ == '__main__':
    p = Portfolio()
    p.get_bm25_scores()
    p.get_pages()
    bs = [4, -4]
    for b in bs:
        lines = []
        for query in range(201, 251):
            res = p.run(b, query)
            rs = sorted(res, key=itemgetter(3))
            rs.reverse()
            for r in rs:
                line = "{} Q0 {} {} {} Portfolio{}".format(
                    query, r[1], r[2], r[3], b)
                lines.append(line)
        with open('./PortfolioScoringBP{}.res'.format(b), 'a') as ifile:
            ifile.writelines("%s\n" % line for line in lines)

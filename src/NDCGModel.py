#!/usr/bin/env python2.7
import numpy as np


class NDCG():
    def __init__(self):
        self.relevancies = dict()
        self.query_list = []
        self.docID_list = []
        self.relevance_list = []

    def open_adhoc(self):
        # using with means it is not necessary to worry about closing the file
        # properly, the python runtime is guarenteed to take care it it
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/qrels.adhoc.txt') as ifile:
            for line in ifile:
                tokens = line.strip().split()
                key = tokens[0] + tokens[2]
                if key not in self.relevancies:
                    self.relevancies[key] = int(tokens[3])

    def open_results(self):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/BM25b0.75_0.res') as ifile:
            for line in ifile:
                tokens = line.strip().split()
                self.query_list.append(int(tokens[0]))
                n.docID_list.append(tokens[2])
                self.relevance_list.append(
                    self.relevancies.get(tokens[0]+tokens[2]))

    def calc_dcg(self, rels, k):
        if k == 1:
            return rels[0]
        else:
            count = [x for x in range(2, k+1)]
            return rels[0] + np.sum(map(
                (lambda(r, i): r / np.log2(i)), zip(rels[1:], count)))


if __name__ == '__main__':
    n = NDCG()
    n.open_adhoc()
    n.open_results()
    n.query_list = np.array(n.query_list)
    n.docID_list = np.array(n.docID_list)
    n.relevance_list = np.array(n.relevance_list)

    k_values = [1, 5, 10, 20, 30, 40, 50]
    for k in k_values:
        accumulator = []
        for query in range(201, 251):
            if query in n.query_list:
                is_query = (n.query_list == query)
                rels = n.relevance_list[is_query]
                rels[rels < 0] = 0
                dcg = n.calc_dcg(rels, k)
                sorted_query = np.sort(rels)[::-1]
                idcg = n.calc_dcg(sorted_query, k)
                if idcg > 0:
                    ndcg = dcg / idcg
                else:
                    ndcg = 0.0
                accumulator.append(ndcg)
        print np.mean(accumulator)

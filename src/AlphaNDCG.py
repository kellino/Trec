#!/usr/bin/env python2.7
from __future__ import division
import numpy as np


class AlphaNDCG():
    def __init__(self):
        # parts belonging to the bm25 results
        self.docIDs = []
        self.query_no = []
        # parts belonging to the ndeval judgements
        self.ndeval_query = []
        self.ndeval_docID = []
        self.subtopic = []
        self.judgement = []

    def get_scores(self, filepath):
        """ parses a trec format results file and stores the details in
            multiple numpy arrays
            Format: query, Q0, docID, rank, score, model """
        with open(filepath) as ifile:
            for line in ifile:
                tokens = line.strip().split()
                self.docIDs.append(tokens[2])
                self.query_no.append(int(tokens[0]))
        self.docIDs = np.array(self.docIDs)
        self.query_no = np.array(self.query_no)

    def get_qrels(self):
        """ parses then ndeval qrels file """
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/qrels.ndeval.txt') as ifile:
            for line in ifile:
                tokens = line.strip().split()
                # query number
                self.ndeval_query.append(int(tokens[0]))
                # doc ID
                self.ndeval_docID.append(tokens[2])
                # subtopic
                self.subtopic.append(int(tokens[1]))
                # judgement
                self.judgement.append(int(tokens[3]))
        self.ndeval_query = np.array(self.ndeval_query)
        self.ndeval_docID = np.array(self.ndeval_docID)
        self.subtopic = np.array(self.subtopic)
        self.judgement = np.array(self.judgement)

    def calc_alpha_dcg(self, js, alpha, k):
        seen = dict()   # count of seen nuggets
        gain = []   # cumulative gain here
        # iterate through tuples
        for i in range(len(js)):
            # special case for first element
            if i == 0:
                gain.append(np.sum(js[i][2]) * (1 - alpha)**0 / np.log2(2))
                for s, x in enumerate(js[i][2]):
                    seen[s] = x
            else:
                if np.sum(js[i][2]) == 0:
                    gain.append(gain[-1])
                else:
                    e = 0
                    for s, x in enumerate(js[i][2]):
                        if x == 1:
                            if seen.get(s) is not None:
                                e += seen.get(s)
                                seen[s] += 1
                    new_gain = gain[-1] + ((np.sum(js[i][2]) * (1 - alpha)**e)) / np.log2(2 + i)
                    gain.append(new_gain)
        return np.sum(gain[:k])

    def run(self, query, alpha, ks):
        # isolate the top 100 docs for query
        top_100 = (self.query_no == query)
        docs = self.docIDs[top_100]
        # isolate the part of ndeval which belongs to the query number
        belongs_to_query = (self.ndeval_query == query)
        collection = self.ndeval_docID[belongs_to_query]
        judgement_list = self.judgement[belongs_to_query]
        # generates a list of docs with judgements for collection in
        # the following form docID (as ranked by bm25) [1 1 1 1 1 0]
        # = judgements for each subtopic, in order
        js = []
        for d in docs:
            ind = np.where(collection == d)
            for i in ind:
                juds = judgement_list[i]
                juds = np.array(juds)
                juds[juds > 1] = 1
                nans = np.isnan(juds)
                juds[nans] = 0
            js.append((query, d, juds))
        at_k = []
        for k in ks:
            dcg = self.calc_alpha_dcg(js, alpha, k)
            ideal = sorted(js, key=lambda (a, b, c): sum(c))
            ideal.reverse()
            idcg = self.calc_alpha_dcg(ideal, alpha, k)
            if idcg > 0:
                at_k.append(dcg / idcg)
            else:
                at_k.append(0.0)
        return at_k


if __name__ == '__main__':
    a = AlphaNDCG()
    a.get_scores('./PortfolioScoringBP4.res')
    a.get_qrels()
    ks = [1, 5, 10, 20, 30, 40, 50]
    totals = []
    for i in range(201, 251):
        if i in a.ndeval_query:
            at_k = a.run(i, 0.1, ks)
            totals.append(at_k)
        means = np.mean(totals, axis=0)
    with open('mmr_ndcg.txt', 'a') as f:
        f.write('MMR\n')
        f.write('lambda = 0.25\n')
        f.write('alpha | K |  alpha-NDCG@K\n')
        for j in range(len(ks)):
            f.write('0.1\t{}\t{:.3f}\n'.format(ks[j], means[j]))

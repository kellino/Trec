#!/usr/bin/env python2.7
import numpy as np
# from itertools import islice


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

    def get_bm25_scores(self):
        with open('./BM25b0.75.res') as ifile:
            for line in ifile:
                tokens = line.strip().split()
                self.docIDs.append(tokens[2])
                self.query_no.append(int(tokens[0]))
        self.docIDs = np.array(self.docIDs)
        self.query_no = np.array(self.query_no)

    def get_qrels(self):
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

    def run(self, query):
        # isolate the part of ndeval which belongs to the query number
        belongs_to_query = (self.ndeval_query == query)
        collection = self.ndeval_docID[belongs_to_query]
        judgement_list = self.judgement[belongs_to_query]
        # generates a list of docs with judgements for collection in
        # the following form docID (as ranked by bm25) [1 1 1 1 1 0]
        # = judgements for each subtopic, in order
        js = []
        for c in collection:
            is_c = (collection == c)
            judgements = judgement_list[is_c]
            judgements[judgements > 1] = 1
            # tuple of query num, doc id and list of binary judgements where
            # the index represents the subtopic
            js.append((query, c, judgements))
        acc = []
        for i in range(len(js)):
            if i == 0:
                acc = np.array(js[i][2])
            else:
                acc = np.add(acc, np.array(js[i][2]))
            print acc


if __name__ == '__main__':
    a = AlphaNDCG()
    a.get_bm25_scores()
    a.get_qrels()
    for i in range(201, 202):
        a.run(i)

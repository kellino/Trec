#!/usr/bin/env python2.7

import numpy as np
from itertools import islice


class AlphaNDCG():
    def __init__(self):
        self.queries = []
        self.sub_topics = []
        self.docIDs = []
        self.judgments = []

    def get_ndevals(self):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/qrels.ndeval.txt') as ifile:
            while True:
                next_n_lines = list(islice(ifile, 5000))
                if not next_n_lines:
                    break
                else:
                    for line in next_n_lines:
                        tokens = line.strip().split()
                        self.queries.append(int(tokens[0]))
                        self.sub_topics.append(int(tokens[1]))
                        self.docIDs.append(tokens[2])
                        self.judgments.append(int(tokens[3]))
            self.queries = np.array(self.queries)
            self.sub_topics = np.array(self.sub_topics)
            self.docIDs = np.array(self.docIDs)
            self.judgments = np.array(self.judgments)


if __name__ == '__main__':
    A = AlphaNDCG()
    A.get_ndevals()
    for query in range(201, 251):
        is_query = (A.queries == query)
        docs = A.docIDs[is_query]
        sub_topics = A.sub_topics[is_query]
        for i in range(np.min(sub_topics), np.max(sub_topics)+1):
            relevant = (sub_topics == i)
            print "query {} subtopic {} docs {}".format(query, i, docs[relevant])

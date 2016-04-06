#!/usr/bin/env python2.7
import numpy as np
from itertools import islice


class BM25():
    def __init__(self):
        self.total_words = 0
        self.docs = dict()
        self.N = 0
        self.queries = dict()
        self.term_appearances = dict()
        self.avdl = 0

    def get_doc_vecs(self):
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
                        self.docs[tokens[0]] = terms

    def get_query_vecs(self):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/query_term_vectors.dat') as ifile:
            for line in ifile:
                terms = dict()
                tokens = line.strip().split()
                for token in tokens[1:]:
                    nums = token.strip().split(':')
                    terms[int(nums[0])] = int(nums[1])
                self.queries[tokens[0]] = terms

    def get_word_total(self):
        for k, v in self.docs.iteritems():
            self.total_words += np.sum([x for w, x in v.iteritems()])

    def calc_average_doc_length(self):
        self.avdl = self.total_words / len(self.docs)

    def get_collection_size(self):
        self.N = len(self.docs)

    def get_term_appearances(self):
        for k, vec in self.docs.iteritems():
            for w, f in vec.iteritems():
                if w in self.term_appearances:
                    self.term_appearances[w] += 1
                else:
                    self.term_appearances[w] = 1

    def calc_bm25(self, query, doc, b, k):
        score = 0
        doc_length = sum([v for x, v in doc.iteritems()])
        for q, v in query.iteritems():
            if q in doc:
                idf = np.log10(self.N - self.term_appearances.get(q)
                               + 0.5 / self.term_appearances.get(q) + 0.5)
                numerator = idf * doc.get(q) * (k + 1)
                demonimator = doc.get(q) + k * (1 - b +
                                                (b * doc_length / self.avdl))
                score += numerator / demonimator
        return score

    def run(self):
        doc_collection = []
        for query in sorted(self.queries.iterkeys()):
            results = []
            for doc, d_vec in bm.docs.iteritems():
                score = bm.calc_bm25(self.queries[query], d_vec, 0.75, 1.5)
                results.append((doc, score))
            rs = sorted(results, key=lambda bm25: bm25[1])
            rs.reverse()
            for i in range(100):
                line = "{} Q0 {} {} {} BM25b{}".format(
                    query, rs[i][0], i+1, rs[i][1], 0.75)
                doc_collection.append(line)
        return doc_collection

if __name__ == '__main__':
    bm = BM25()
    bm.get_doc_vecs()
    bm.get_query_vecs()
    bm.get_word_total()
    bm.calc_average_doc_length()
    bm.get_collection_size()
    bm.get_term_appearances()
    scores = bm.run()
    with open('./BM25b0.75.res', 'w') as ifile:
        ifile.writelines("%s\n" % item for item in scores)

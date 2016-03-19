#!/usr/bin/env python2.7
import math as m
import copy

DEBUG = True
results = []
ndcg_list = []
relevancy = dict()


class Result():
    def __init__(self, queryNo, docID, bm25, relevance=None):
        self.queryNo = queryNo
        self.docID = docID
        self.bm25 = bm25
        self.relevance = relevance


class Qrel():
    def __init__(self, queryNo=None, relevance=None):
        self.queryNo = queryNo
        self.relevance = relevance


class NDCG():
    def calc_ndcg(self, rels, sorted_rels, k):
        if len(rels) > 0:
            temp = [(i, j) for i, j in enumerate(rels)]
            dcg = float(rels[0]) + sum(map(
                (lambda (i, j): j / m.log(i+1, 2)), temp[1:k]))
            ideal = [(i, j) for i, j in enumerate(sorted_rels)]
            idcg = float(sorted_rels[0]) + sum(map(
                (lambda (i, j): j / m.log(i+1, 2)), ideal[1:k]))
            if idcg == 0:
                ndcg = 0.0
            else:
                ndcg = dcg/idcg
            ndcg_list.append(ndcg)
        if DEBUG:
            self.print_debug(rels, sorted_rels, dcg, idcg, k, ndcg)

    def print_debug(self, rels, sorted_rels, dcg, idcg, k, ndcg):
        for i in rels:
            print i,
        print("dcg = {}".format(dcg))
        for i in sorted_rels:
            print i,
        print("idcg = {}".format(idcg))
        print("normalized dcg at {} = {}\n".format(k, ndcg))

    def gen_results_array(self, results_file):
        for line in results_file:
            cols = line.split()
            temp = Result(cols[0], cols[2], float(cols[4]))
            results.append(temp)

    def gen_relevancy_dict(self, relevancy_file):
        for line in relevancy_file:
            cols = line.split()
            key = cols[0] + cols[2]
            if int(cols[3]) < 0:
                relevancy[key] = Qrel(cols[0], 0)
            else:
                relevancy[key] = Qrel(cols[0], int(cols[3]))

    def assign_relevancy_to_result(self):
        for result in results:
            key = result.queryNo + result.docID
            item = relevancy.get(key)
            if item:
                result.relevance = int(item.relevance)
            else:
                result.relevance = 0

    def extract_relevancies(self, group_num):
        result_group = [x for x in results if x.queryNo == str(group_num)]
        if len(result_group) > 0:
            temp = []
            for result in result_group:
                if result is not None:
                    temp.append(int(result.relevance))
                else:
                    temp.append(0)
            if DEBUG:
                print("{}:".format(group_num))
            return temp

    def make_ideal_list(self, rels):
        temp = []
        if rels is not None:
            temp = copy.copy(rels)
            temp.sort()
            temp.reverse()
        return temp

    def gen_ndcg_average(self):
        ats = [0, 0, 0, 0, 0]
        for i in range(len(ndcg_list)):
            if i == 0:
                ats[0] += ndcg_list[i]
            if i % 5 == 0:
                ats[1] += ndcg_list[i]
            elif i % 5 == 1:
                ats[2] += ndcg_list[i]
            elif i % 5 == 2:
                ats[3] += ndcg_list[i]
            else:
                ats[4] += ndcg_list[i]
        n_length = len(ndcg_list) / 4
        ats = map((lambda x: x / n_length), ats)
        print("at 1 {}, at 5 {}, at 10 {}, at 20 {}, at 40 {}".format(
            ats[0], ats[1], ats[2], ats[3], ats[4]))


if __name__ == '__main__':
    results_file = open(
        '/home/david/Documents/data_retrieval/coursework/BM25b0.75_0.res')
    relevancy_file = open(
        '/home/david/Documents/data_retrieval/coursework/qrels.adhoc.txt')
    calc = NDCG()
    calc.gen_results_array(results_file)
    calc.gen_relevancy_dict(relevancy_file)
    calc.assign_relevancy_to_result()
    for group_num in range(201, 251):
        rels = calc.extract_relevancies(group_num)
        ideal = calc.make_ideal_list(rels)
        if rels is not None:
            map(lambda x: calc.calc_ndcg(rels, ideal, x),
                [1, 5, 10, 20, 30, 40, 50])
    calc.gen_ndcg_average()
    results_file.close()
    results_file.close()

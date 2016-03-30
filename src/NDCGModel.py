#!/usr/bin/env python2.7
import math as m
import numpy as np
import copy
from filehandler import FileHandler
from fileobjects import Result, Qrel


results = []
ndcg_list = np.empty((48, 7))
relevancy = dict()


class NDCG():

    def calc_ndcg(self, rels, sorted_rels, k):
        # calculates the ndcg for a given query up to position k
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
            return ndcg

    def gen_results_array(self, results_file):
        # fills a list with Result objects
        for line in results_file:
            cols = line.split()
            # cols[0] = query number
            # cols[2] = clueweb document number
            # cols[4] = bm25 float
            results.append(Result(cols[0], cols[2], float(cols[4])))

    def gen_relevancy_dict(self, relevancy_file):
        # lifts data from relevancy file, saving it to a dictionary, using a
        # compound key derived from the clueweb id and the query number
        for line in relevancy_file:
            cols = line.split()
            key = cols[0] + cols[2]
            # if relevancy is -2 or None, set to 0
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
            return temp

    def make_ideal_list(self, rels):
        # obtains the full list of relevancies for a given query, orders them
        # and then reverses the list, so that the highest elements are at the
        # beginning
        temp = []
        if rels is not None:
            # make a deep copy, otherwise the original list is sorted in place
            temp = copy.copy(rels)
            temp.sort()
            temp.reverse()
        return temp


if __name__ == '__main__':
    # open files, get data
    f = FileHandler()
    results_file = open(f.find_file("BM25b0.75_0", "*.res").strip())
    relevancy_file = open(f.find_file("qrels.adhoc", "*.txt").strip())
    calc = NDCG()
    calc.gen_results_array(results_file)
    calc.gen_relevancy_dict(relevancy_file)
    calc.assign_relevancy_to_result()
    # clean up
    f.close_file(results_file)
    f.close_file(relevancy_file)

    # list of k values
    ks = [1, 5, 10, 20, 30, 40, 50]
    # main function really starts here
    for group_num in range(201, 251):
        i = 0
        rels = calc.extract_relevancies(group_num)
        ideal = calc.make_ideal_list(rels)
        if rels is not None:
            ndcg_list[i] = (
                [x for x in map(lambda x: calc.calc_ndcg(rels, ideal, x), ks)])
            i += 1
    np.set_printoptions(precision=3, linewidth=120)
    print(ndcg_list)
    print(np.sum(ndcg_list, axis=0))
    # this last line not working as expected, even though all the data appears
    # to be correct...
    print(np.mean(ndcg_list, axis=0, dtype=np.float64))

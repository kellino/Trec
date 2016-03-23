#!/usr/bin/python2.7
from filehandler import FileHandler
import numpy as np
from math import sqrt


query_list = []
doc_list = []
cosines = np.zeros([100, 100])


class Query():
    def __init__(self, queryNo=None, query_vector=None):
        self.queryNo = queryNo
        self.query_vector = query_vector


class Doc():
    def __init__(self, docID=None, terms=None, term_frequencies=None):
        self.docID = docID
        self.terms = terms
        self.term_frequencies = term_frequencies


def fill_query_list(query_file):
    for line in query_file:
        new = Query()
        parts = line.split()
        new.queryNo = parts[0]
        terms = []
        term_frequencies = []
        for part in parts[1:]:
            if ':' in part:
                nums = part.split(':')
                terms.append(int(nums[0]))
                term_frequencies.append(int(nums[1]))
        new.query_vector = terms
        new.term_frequencies = term_frequencies
        query_list.append(new)


def fill_doc_list(doc_file):
    for line in doc_file:
        new = Doc()
        parts = line.split()
        new.docID = parts[0]
        terms = []
        term_frequencies = []
        for part in parts[1:]:
            if ':' in part:
                nums = part.split(':')
                terms.append(int(nums[0]))
                term_frequencies.append(int(nums[1]))
        new.terms = terms
        new.term_frequencies = term_frequencies
        doc_list.append(new)


def calculate_cosine():
    i = 0
    root = doc_list[i]
    cos = []
    for doc in doc_list[i:100]:
        n_vec = set(root.terms).intersection(doc.terms)
        doc1 = []
        doc2 = []
        for i in n_vec:
            if i < len(root.term_frequencies):
                doc1.append(root.term_frequencies[i])
            else:
                doc1.append(0)
        for i in n_vec:
            if i < len(doc.term_frequencies):
                doc2.append(doc.term_frequencies[i])
            else:
                doc2.append(0)
        numerator = sum(map((lambda x, y: x*y), doc1, doc2))
        denominator = (sqrt(sum([x*x for x in root.term_frequencies]))
                       * sqrt(sum([y*y for y in doc.term_frequencies])))
        cos.append(numerator / denominator)
    cosines[0] = cos
    print cosines


if __name__ == '__main__':
    f = FileHandler()
    query_file = open(f.find_file('query_term_vectors', '*.dat'))
    doc_file = open(f.find_file('document_term_vectors', '*.dat'))
    # fill_query_list(query_file)
    fill_doc_list(doc_file)
    calculate_cosine()
    f.close_file(query_file)
    f.close_file(doc_file)

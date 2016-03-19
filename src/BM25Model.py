#!/usr/bin/env python2.7
import math
import subprocess

DEBUG = False

doc_collection = []
query_collection = []


class Docs():
    def __init__(self, docID=None, vector=None):
        self.docID = docID
        self.vector = vector


class Queries():
    def __init__(self, queryNo=None, vector=None):
        self.queryNo = queryNo
        self.vector = vector


def parse_doc_vectors(filename):
    """ reads the document vectors into a python list """
    for line in filename:
        new = Docs()
        parts = line.split()
        new.docID = parts[0]
        vectors = []
        for part in parts[1:]:
            if ':' in part:
                nums = part.split(':')
                vectors.append((int(nums[0]), int(nums[1])))
        new.vector = vectors
        doc_collection.append(new)


def parse_query_vectors(filename):
    for line in filename:
        new = Queries()
        parts = line.split()
        new.queryNo = parts[0]
        vectors = []
        for part in parts[1:]:
            if ':' in part:
                nums = part.split(':')
                vectors.append((int(nums[0]), int(nums[1])))
        new.vector = vectors
        query_collection.append(new)


def get_average_doc_length(N):
    """ gets the average length of a document where N is the
        size of the collection """
    total_words_in_collection = 0
    for doc in doc_collection:
        total_words_in_collection += sum([x for (i, x) in doc.vector])
    return total_words_in_collection / N


def calc_nqi(term):
    """ gets the number of documents containing 'term' """
    nqi = 0
    for doc in doc_collection:
        nqi += sum([x for (i, x) in doc.vector if term == i])
    return nqi


def calc_idf(nqi, N):
    """ gets the inverse document frequenct of term nqi
        sets this to 0 if a negative number is returned """
    div = (N - nqi + 0.5) / nqi + 0.5
    idf = math.log(div, 2)
    if idf >= 0:
        return idf
    else:
        return 0


def calc_bm25(query, doc, avdl, N):
    """ calculates the bm25 for a query vector of a document in collection """
    b = 0.75
    # k = 1.5
    K = (1 - b + b * (len(doc.vector) / avdl))
    idfs = []
    print K
    query_terms = [i for (i, q) in query.vector]    # dict, not frequency
    print "query num = {} query_terms vector = {}".format(
        query.queryNo, query_terms)
    doc_vec = [i for (i, x) in doc.vector]
    for q in query_terms:
        if q in doc_vec:
            idf = calc_idf(q, N)
            idfs.append(idf)
    print("idfs is/are {}".format(idfs))


def find_file(search, extension):
    # not very portable solution to finding the files on the system
    # but it will do
    filepath = subprocess.check_output(
        'find ~/ -type f -name "{}" | grep -i {}'.format(
            extension, search), shell=True)
    return filepath


if __name__ == '__main__':
    try:
        query_vectors = open(find_file("query_term_vectors", "*.dat").strip())
        term_vectors = open(
            find_file("document_term_vectors", "*.dat").strip())
        parse_doc_vectors(term_vectors)
        parse_query_vectors(query_vectors)
        N = len(doc_collection)
        avdl = get_average_doc_length(N)
        for query in query_collection:
            calc_bm25(query, doc_collection[0], avdl, N)
    except:
        pass
    finally:
        if query_vectors is not None:
            query_vectors.close()
        if term_vectors is not None:
            term_vectors.close()

#!/usr/bin/python2.7
import math
from filehandler import FileHandler

doc_collection = []
query_collection = []
idfs = dict()
term_frequencies = dict()


class Doc():
    def __init__(self, docID=None, terms=None,
                 term_frequency=None, doc_length=None):
        self.docID = docID
        self.terms = terms
        self.term_frequency = term_frequency
        self.doc_length = doc_length


class Query():
    def __init__(self, queryNo=None, terms=None,
                 term_frequency=None):
        self.queryNo = queryNo
        self.terms = terms
        self.term_frequency = term_frequency


def parse_file(filename, obj_type, array):
    for line in filename:
        parts = line.split()
        if obj_type == "query":
            new = Query()
            new.queryNo = parts[0]
        else:
            new = Doc()
            new.docID = parts[0]
        terms = []
        term_frequency = []
        for part in parts[1:]:
            if ':' in part:
                nums = part.split(':')
                terms.append(int(nums[0]))
                term_frequency.append(int(nums[1]))
        new.terms = terms
        new.term_frequency = term_frequency
        array.append(new)


def get_doc_length():
    for doc in doc_collection:
        doc.doc_length = sum(doc.term_frequency)


def get_average_doc_length():
    total = 0
    for doc in doc_collection:
        total += doc.doc_length
    return total / len(doc_collection)


def get_term_totals():
    # very wasteful this...
    for doc in doc_collection:
        for i in range(len(doc.terms)):
            if doc.terms[i] in term_frequencies:
                term_frequencies[doc.terms[i]] += doc.term_frequency[i]
            else:
                term_frequencies[doc.terms[i]] = 0


def calculate_idf_of_term(query, N):
    for q in query.terms:
        nqi = term_frequencies.get(q)
        if ((N - nqi + 0.5 / nqi + 0.5)) >= 0:
            idfs[q] = math.log((N - nqi + 0.5 / nqi + 0.5), 2)
        else:
            idfs[q] = 0.0


def calculate_bm25(query, avdl):
    k = 1.5
    b = 0.75
    q_vec = [q for q in query.terms]
    idf_of_q = [idfs.get(q) for q in q_vec]
    for doc in doc_collection:
        doc_vec = []        # holds the frequencies of the search terms
        for q in q_vec:
            if q in doc.terms:
                doc_vec.append(doc.term_frequency[doc.terms.index(q)])
        try:
            bm25 = sum(map((lambda x, y: x * (y * (k+1) / y + k * (1 - b + b * (doc.doc_length / avdl)))), idf_of_q, doc_vec))
            print query.queryNo, doc.docID, bm25
        except:
            pass


if __name__ == '__main__':
    try:
        f = FileHandler()
        query_file = open(f.find_file("query_term_vectors", "*.dat"))
        doc_file = open(f.find_file("document_term_vectors", "*.dat"))
        # read the query file into the query_collection list
        parse_file(query_file, "query", query_collection)
        # read the doc file into the doc_collection list
        parse_file(doc_file, "doc", doc_collection)
    except:
        pass
    finally:
        # close open files
        f.close_file(query_file)
        f.close_file(doc_file)
    get_doc_length()
    avdl = get_average_doc_length()
    get_term_totals()
    N = len(doc_collection)
    for query in query_collection:
        calculate_idf_of_term(query, N)
    for query in query_collection:
        calculate_bm25(query, avdl)

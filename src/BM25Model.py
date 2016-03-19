#!/usr/bin/env python2.7
import math
import re

query_vectors = open(
    '/home/david/Documents/data_retrieval/coursework/query_term_vectors.dat')
term_vectors = open(
    '/home/david/Documents/data_retrieval/coursework/document_term_vectors.dat')

doc_collection = []
query_collection = []


def parse_vectors(filename, collection_list):
    for line in filename:
        vectors = []
        parts = line.split()
        for part in parts:
            if ':' in part:
                nums = part.split(':')
                vectors.append((int(nums[0]), int(nums[1])))
        print vectors
        collection_list.append(vectors)


def get_queries():
    for line in query_vectors:
        query_collection.append(line)


def get_average_doc_length(N):
    total_words_in_collection = 0
    for line in doc_collection:
        words = line.split()
        for word in words:
            total_words_in_collection += int(word[1])
            # if re.search(":", word):
                # i = word.index(":") + 1
                # total_words_in_collection += int(word[i:])
    return total_words_in_collection / N


def calc_nqi(term):
    nqi = 0
    for line in doc_collection:
        if term in line:
            nqi += 1
    return nqi


def calc_idf(N, nqi):
    div = (N - nqi + 0.5) / nqi + 0.5
    idf = math.log(div, 2)
    if idf >= 0:
        return idf
    else:
        return 0


def calc_bm25(query, doc, avdl):
    b = 0.75
    # k = 1.5
    doc_length = 0
    words = doc.split(' ')
    for word in words[1:]:
        if re.search(":", word):
            i = word.index(":") + 1
            doc_length += i
    print("query vector {}, doc length {}, bottom line value is {}".format(
        query, doc_length, (1-b) + (b * (doc_length / avdl))))


if __name__ == '__main__':
    parse_vectors(term_vectors, doc_collection)
    parse_vectors(query_vectors, query_collection)
    N = len(doc_collection)
    # nqi = calc_nqi('7:')
    # idf = calc_idf(N, nqi)
    print("collection size = {}".format(N))
    avdl = get_average_doc_length(N)
    # print("average doc length = {}".format(avdl))
    # print(len(query_collection))
    # for query in query_collection:
        # for doc in doc_collection:
            # calc_bm25(query, doc, avdl)
    query_vectors.close()
    term_vectors.close()

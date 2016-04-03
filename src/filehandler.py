#!/usr/bin/env python2.7
import numpy as np


class FileHandler():
    def get_doc_vectors(docs, term_appearances):
        with open(r'/home/david/Documents/data_retrieval'
                  r'/coursework/document_term_vectors.dat') as ifile:
            for line in ifile:
                terms = []
                term_frequencies = []
                tokens = line.strip().split()
                for token in tokens[1:]:
                    if ':' in token:
                        nums = token.strip().split(':')
                        terms.append(int(nums[0]))
                        term_frequencies.append(int(nums[1]))
                        if int(nums[0]) in term_appearances:
                            term_appearances[int(nums[0])] += 1
                        else:
                            term_appearances[int(nums[0])] = 1
                # add the documents vectors to the docs dictionary
                docs[tokens[0]] = np.array([terms, term_frequencies])

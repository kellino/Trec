#!/usr/bin/python2.7
import subprocess
from sys import exit
import numpy as np
from fileobjects import VecObject, Doc, VecObj2
from collections import OrderedDict


class FileHandler():

    def find_file(self, search, extension=None):
        # not very portable solution to finding the files on the system,
        # should work on linux/mac and probably cygwin as well
        try:
            filepath = subprocess.check_output(
                'find ~/ -type f -name "{}" | grep -i {}'.format(
                    extension, search), shell=True)
            return filepath.strip()
        except subprocess.CalledProcessError:
            print(r"unable to find file on system."
                  r"Please check file information")
            exit()

    def close_file(self, filename):
        """ safe file closure, throws an IOError exception if
            unable to close"""
        if filename is not None:
            try:
                filename.close()
            except IOError:
                print "unable to close file"
                exit()

    def fill_dict_np(self, filename, dictionary):
        for line in filename:
            parts = line.split()
            new = VecObj2()
            new.ID = parts[0].strip()
            term_list = []
            term_frequencies = []
            for part in parts[1:]:
                if ':' in part:
                    nums = part.split(':')
                    term_list.append(int(nums[0]))
                    term_frequencies.append(int(nums[1]))
            new.terms = np.array([term_list, term_frequencies])
            dictionary[parts[0]] = new

    def fill_dictionary(self, filename, dictionary):
        """ takes an open (formatted) file and a dictionary and sets the first
            element of the line as the key, and assigning the rest of the data
            to a VecObject """
        for line in filename:
            parts = line.split()
            new = VecObject()
            new.ID = parts[0]
            terms = []
            term_frequencies = []
            for part in parts[1:]:
                if ':' in part:
                    nums = part.split(':')
                    terms.append(int(nums[0]))
                    term_frequencies.append(int(nums[1]))
            new.terms = terms
            new.term_frequencies = term_frequencies
            # there is a redundancy here, in that the id is stored twice, once
            # as the key and in the object itself
            dictionary[parts[0]] = new

    def top_results_from_file(self, results_file, k):
        """ extracts the top k results for each query from a
            formatted file into a dictionary"""
        rs = OrderedDict()
        all_results = []
        for l in results_file:
            all_results.append(l)
        for i in range(201, 251):
            group = [line.split() for line in all_results if
                     line.startswith(str(i))][:k]
            if len(group) > 0:
                doc = []
                for subgroup in group:
                    doc.append(subgroup[2])
                rs[i] = doc
        return rs

    def top_results_from_file_with_bm25(self, results_file, docs, k):
        """ extracts the top k results for each query from a
            formatted file into a dictionary"""
        # destination dictionary
        d = dict()
        # read file into an array
        rf = []
        for l in results_file:
            rf.append(l)
        # extract the top 100 results for each query and add
        # them to a dictionary of top results, with query number as key
        for i in range(201, 251):  # TODO query nums should not be hard coded
            lst = []
            group = [line.strip() for line in rf if
                     line.startswith(str(i))][:k]
            # some queries don't exist, so check to make sure group is
            # not empty before adding them to the top_results dictionary
            if len(group) > 0:
                # make objects of the top 100 clueweb returns, saving id, bm23
                # and term/frequency vectors
                for g in group:
                    doc = Doc()
                    p = g.split()
                    doc.ID = p[2]
                    doc.bm25 = p[4]
                    doc.terms = docs.get(doc.ID).terms
                    doc.term_frequencies = docs.get(doc.ID).term_frequencies
                    lst.append(doc)
                d[i] = lst
        return d

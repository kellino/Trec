#!/usr/bin/python2.7
import subprocess
from sys import exit
from fileobjects import VecObject


class FileHandler():

    def find_file(self, search, extension):
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

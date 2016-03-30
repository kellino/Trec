#!/usr/bin/python
import sys

# run program with two command line args, the filepath of the results file, and
# the collection filepath
results = sys.argv[1]
collection = sys.argv[2]

f = open(results, 'r')
original_lines = []
line_nums = []
coll = dict()


def get_linenums_from_trec_results():
    for line in f:
        original_lines.append(line)
        words = line.split(" ")
        line_nums.append(int(words[2]))
    f.close()


def read_collection_spec():
    fc = open(collection, 'r')

    i = 1
    for line in fc:
        words = line.split('/')
        new_num = words[7].split('.')
        coll[i] = new_num[0]
        i += 1
    fc.close()


def print_collection():
    for k, v in coll.iteritems():
        print k, v


# slightly lazy, but easier to use a redirection in the shell than open a new
# file and close it in python
def merge_files():
    i = 0
    for i in range(len(line_nums)):
        new_line = original_lines[i].split()
        print(new_line[0] + " " + new_line[1] + " " +
              coll.get(line_nums[i]) + " " + new_line[3] + " " +
              new_line[4] + " " + new_line[5])


if __name__ == '__main__':
    get_linenums_from_trec_results()
    read_collection_spec()
    merge_files()

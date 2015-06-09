#! /usr/bin/env python

from os import listdir
from os.path import isfile, join
import fileinput
import re
import utils.defaults
import sys

def get_dictionary(docs, dictFilters=None):
    allwords = {}
    for doc in docs:
        for word in doc:
            try:
                allwords[word] += 1
            except KeyError:
                allwords[word] = 1
    if dictFilters:
        for filter in dictFilters:
            allwords = filter(allwords)
    dict_list = list()
    index_map = {}
    i = 0
    for word in allwords:
        dict_list.append(word[0])
        index_map[word[0]] = i
        i += 1

    return dict_list, index_map

def write_dictionary(dict_list, path="dictionary.txt"):
    with open(path, "w") as f:
        for word in dict_list:
            f.write(word + "\n")
    

def produce_lda(docs, index_map):
    to_return = ''
    for doc in docs:
        to_print = []
        for word,count in doc.iteritems():
            try:
                to_print.append(str(index_map[word]) + ':' + str(count))
            except KeyError:
                pass
        if len(to_print) > 0:
                print str(len(to_print)) +' ' +  ' '.join(to_print)
        to_return += str(len(to_print)) + ' ' + ' '.join(to_print) + '\n'
    return to_return

def plaintext_to_wordcounts(words):
    counts = {}
    for word in words:
        try:
            counts[word] += 1
        except KeyError:
            counts[word] = 1
    return counts

def file_to_doc(filename, processingFunc=None):
    to_return = []
    for line in fileinput.input(filename):
        words = re.findall("\w+", line)
        if processingFunc:
            for func in processingFunc:
                words = func(words)
        to_return += [word for word in words if word] # removes words that become empty strings
    return to_return

def file_list_to_lda(filelist, processingFunc=None, dictFilters=None):
    # get dictionary
    allwords = {}
    for thisfile in filelist:
        doc = file_to_doc(thisfile, processingFunc)
        for word in set(doc):
            try:
                allwords[word] += 1
            except KeyError:
                allwords[word] = 1
        sys.stderr.write('PROCESSED FOR DICTIONARY: ' + thisfile + '\n')
    if dictFilters:
        for filter in dictFilters:
            allwords = filter(allwords)
    i = 0
    dict_list = []
    index_map = {}
    for word in allwords:
        dict_list.append(word[0])
        index_map[word[0]] = i
        i += 1
    write_dictionary(dict_list)

    # produce lda output
    for thisfile in filelist:
        doc = file_to_doc(thisfile, processingFunc)
        wordcounts = plaintext_to_wordcounts(doc)
        to_print = []
        for word, count in wordcounts.iteritems():
            try:
                to_print.append(str(index_map[word]) + ':' + str(count))
            except KeyError:
                pass
        if len(to_print) > 0:
            print str(len(to_print)) +' ' +  ' '.join(to_print)
            sys.stderr.write('PROCESSED FOR LDA: ' + thisfile + '\n')
#        to_return += str(len(to_print)) + ' ' + ' '.join(to_print) + '\n'
'''
def file_list_to_lda(filelist, processingFunc=None, dictFilters=None):
    # takes a list of files
    # produces a list of those files represented as lda input-formatted strings
    # 
    # can pass some processing functions to apply to each line optionally, if you want
    # to do some additional pre-processing. by default, we pass a stemmer and stopword removal
    sys.stderr.write(str(len(filelist)) + '\n')
    docs = []
    for this_file in filelist:
        sys.stderr.write(this_file + '\n')
        lines = []
        for line in fileinput.input(this_file):
            words = re.findall("\w+", line)
            if processingFunc:
                for func in processingFunc:
                    words = func(words) # yeah, it's a bit limited
            lines += [word for word in words if word]
        doc = plaintext_to_wordcounts(lines)
        docs.append(doc)
    sys.stderr.write(str(len(docs)) + '\n')
    # 'docs' is a list of lists of words that have been pre-processed
    dict_list, index_map = get_dictionary(docs, dictFilters)
    write_dictionary(dict_list)
    lda_input = produce_lda(docs, index_map)
    return lda_input
'''
# standalone client:
# - pass a directory that contains all of the flat files to process
if __name__ == '__main__':
    import sys
    onlyfiles = [ (sys.argv[1]+"/" + f) for f in listdir(sys.argv[1]) if isfile(join(sys.argv[1], f)) ]
    from random import shuffle
    shuffle(onlyfiles)
    onlyfiles = onlyfiles[1000:1500]
    default_functions = utils.defaults.Preprocessors
    defaultDictFilters = utils.defaults.DictFilters
    file_list_to_lda(onlyfiles, processingFunc=default_functions, dictFilters=defaultDictFilters)

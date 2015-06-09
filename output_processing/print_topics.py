#! /usr/bin/env python

import subprocess, sys, os

def print_topics(dict_file, lda_dir, results_dir, configs=None):
    if configs:
        command = "%s/topics.py %s/final.beta %s %s" % (lda_dir, results_dir, dict_file, configs['words per topic'])
    else:
        command = "%s/topics.py %s/final.beta %s 10" % (lda_dir, results_dir, dict_file)
    p = subprocess.Popen(command, shell=True)
    p.wait()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "usage: " + sys.argv[0] + " <dict_file> <lda_dir> <results_dir>"
        sys.exit()
    cwd = os.getcwd()
    for i in range(1, len(sys.argv)):
        if not os.path.isabs(sys.argv[i]):
            sys.argv[i] = cwd + '/' + sys.argv[i]
    dict_file = sys.argv[1]
    lda_dir = sys.argv[2]
    results_dir = sys.argv[3]
    configs = None
    if len(sys.argv) >= 5:
        configs = {'num topics': '10',
                   'words per topic': '10',
                   'alpha':'.01'}
        with open(sys.argv[4], 'r') as f:
            for line in f:
                parts = [part.strip() for part in line.split('=')]
                if len(parts) == 2:
                    configs[parts[0]] = parts[1]
    print_topics(dict_file, lda_dir, results_dir, configs)

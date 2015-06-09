#! /usr/bin/env python

import os, sys, subprocess

# this just calls the blei library
def run_lda(input_file, dictionary_file, lda_path, results_dir, configs=None):
    if configs:
        command = ("%s/lda est %s %s %s/settings.txt %s random %s" % (lda_path, configs['alpha'], configs['num topics'], lda_path, input_file, results_dir))
    else:
        command = ("%s/lda est .01 10 %s/settings.txt %s random %s" % (lda_path, lda_path, input_file, results_dir))
    print command
    p = subprocess.Popen(command, shell=True)
    p.wait()

# just for testing
if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "usage: " + sys.argv[0] + " <input-file> <dict-file> <lda-path> <results-dir>"
        sys.exit()
    cwd = os.getcwd()
    for i in range(1, len(sys.argv)):
        if not os.path.isabs(sys.argv[i]):
            sys.argv[i] = cwd + '/' + sys.argv[i]
    input_file = sys.argv[1]
    dict = sys.argv[2]
    lda_path = sys.argv[3]
    results_dir = sys.argv[4]
    configs = None
    if len(sys.argv) >= 6:
        configs = {'num topics': '10',
                   'words per topic': '10',
                   'alpha':'.01'}
        with open(sys.argv[5], 'r') as f:
            for line in f:
                parts = [part.strip() for part in line.split('=')]
                if len(parts) == 2:
                    configs[parts[0]] = parts[1]
    run_lda(input_file, dict, lda_path, results_dir, configs)

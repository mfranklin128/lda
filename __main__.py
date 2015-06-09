#! /usr/bin/env python

import data_preprocessing
import run_lda
import output_processing

import sys, os, subprocess

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: ' + sys.argv[0] + ' <input-dir>'
        sys.exit()

    data_dir = sys.argv[1] # folder containing input flat files
    config_filename = ''
    process_data_str = ''
    if len(sys.argv) >= 3:
        config_filename = sys.argv[2]
    if len(sys.argv) >= 4:
        process_data_str = sys.argv[3]
    if not os.path.isabs(sys.argv[0]):
        sys.argv[0] = os.getcwd() + '/' + sys.argv[0]
    if process_data_str == 'true' or process_data_str == 't':
        command = "python " + sys.argv[0] + "/data_preprocessing/flat_files_to_lda.py "
        command += data_dir
        print sys.argv[0] + '/input.lda'
        with open(sys.argv[0] + '/input.lda', 'w') as f:
            p = subprocess.Popen(command, shell=True, stdout=f)
            p.wait()
                
    command = "python " + sys.argv[0] + "/run_lda/run_lda.py "
    command += "%s %s %s %s" % (sys.argv[0]+"/input.lda", os.getcwd() + '/dictionary.txt',
                                sys.argv[0]+"/lda-c-dist", sys.argv[0]+"/lda-c-dist")
    command += ' ' + config_filename
    p = subprocess.Popen(command, shell=True)
    p.wait()

    command = "python " + sys.argv[0] + "/output_processing/print_topics.py "
    command += "%s %s %s" % (os.getcwd() + '/dictionary.txt', sys.argv[0]+"/lda-c-dist",
                             sys.argv[0]+"/lda-c-dist")
    command += ' ' + config_filename
    p = subprocess.Popen(command, shell=True)
    p.wait()

    print 'DONE'

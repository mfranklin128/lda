#! /usr/bin/env python

import numpy
import numpy

# iterate over gamma files
def normalize(weights):
    sum = 0.0
    for weight in weights:
        sum += float(weight)
    to_return = []
    for weight in weights:
        to_return.append(float(weight)/sum)
    return to_return

# takes an iterable of topic weights, where each item is a document
# if the weight surpasses some threshold, we consider the topic to be "present"
#
# returns a list where the ith element is the portion of documents in the set
# in which the ith topic was "present"
def get_proportions_threshold(topic_weights, threshold=0.9):
    if not topic_weights or len(topic_weights) == 0:
        print 'Why did you give me an empty list??'
        return []
    results = list()
    for i in range(len(topic_weights[0])):
        results.append(0)
    for document in topic_weights:
        weights = normalize(document)
        for i in range(len(weights)):
            if weights[i] > threshold:
                results[i] += 1
    return results
# takes the same topic weights as get_proportions_threshold, plus a number of quantiles
#
# computes, for each topic, how many documents fall in each quantile
# returns a list of lists, where:
# results[i][j] = the number of documents in the jth quantile for topic i
def get_proportions_distribution(topic_weights, num_quantiles=10):
    if not topic_weights or len(topic_weights) == 0:
        print 'Why did you give me an empty list??'
        return []
    results = list()
    for i in range(len(topic_weights[0])):
        result = list()
        for j in range(num_quantiles):
            result.append(0)
        results.append(result)
    quantile_width = 1.0/num_quantiles
    import sys
    for i in range(len(topic_weights)):
        weights = normalize(topic_weights[i])
        for topic in range(len(topic_weights[0])):
            result = results[topic]
#            print results
#            print topic
#            print result
#            sys.stdin.readline()
            weight = weights[topic]
            quantile = int(weight/quantile_width)
            results[topic][quantile] += 1
    return results

def get_mean_weight(topic_weights):
    if not topic_weights or len(topic_weights) == 0:
        print 'Why did you give me an empty list??'
        return []
    results = [0]*len(topic_weights[0])
    for i in range(len(topic_weights[0])):
        results[i] = numpy.mean([normalize(weight)[i] for weight in topic_weights])
    return results

def get_stddev_weight(topic_weights):
    if not topic_weights or len(topic_weights) == 0:
        print 'Why did you give me an empty list??'
        return []
    results = [0]*len(topic_weights[0])
    for i in range(len(topic_weights[0])):
        results[i] = numpy.std([normalize(weight)[i] for weight in topic_weights])
    return results

def gamma_file_to_matrices(filename):
    input = []
    num_topics = -1
    with open(filename, "r") as f:
        for line in f:
            weights = [float(elem) for elem in line.split()]
            if not num_topics == -1 and not len(weights) == num_topics:
                print 'Malformed input: not consistent number of topics'
                return None
            input.append(weights)
    return input

# runs all of the above procedures for a given gamma file
# prints the results
def print_document_weight_info(input):
    proportions_threshold = get_proportions_threshold(input)
    proportions_distribution = get_proportions_distribution(input)
    mean = get_mean_weight(input)
    stddev = get_stddev_weight(input)

    for i in range(len(mean)):
        print ('Mean of documents in topic %d: ' % i) + str(mean[i])

    for i in range(len(stddev)):
        print ('Stddev of documents in topic %d: ' % i) + str(stddev[i])

    for i in range(len(proportions_threshold)):
        print ('Proportion of documents containing topic %d: ' % i) + str(proportions_threshold[i])

    print proportions_distribution
    for i in range(len(proportions_distribution)):
        print 'Topic %d: ' % i
        for quantile in range(len(proportions_distribution[i])):
            if quantile == 0:
                print ('\tProportion less than ' + str(1.0/float(len(proportions_distribution[i]))) 
                       + ': ' + str(proportions_distribution[i][quantile]))
            else:
                print ('\tProportion between ' + str(float(quantile)/float(len(proportions_distribution[i]))) +
                       ' and ' + str(float(quantile+1)/float(len(proportions_distribution[i]))) + ': ' + str(proportions_distribution[i][quantile]))
    

    return (mean, stddev, proportions_threshold, proportions_distribution)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'Usage: ' + sys.argv[0] + ' [gamma-file]'
    
    print_document_weight_info(gamma_file_to_matrices(sys.argv[1]))

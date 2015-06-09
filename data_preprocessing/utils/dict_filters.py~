# these all take a dict of word -> count and return a dict of filtered_words -> count
# where key-value pairs have been removed on the basis of the filter
import operator

def unique(allwords, dicts, threshold=1):
    to_return = set()
    if threshold < 1.0:
        threshold = len(dicts)*threshold
    for word in allwords:
        count = 0
        for dict in dicts:
            if word in dict:
                count += 1
            if count == threshold+1:
                to_return.add(word)
                break
        if count == threshold+1:
            to_return.add(word)
    return to_return
    
def ubiquitous(allwords, dicts, threshold=0.99):
    to_return = set()
    if threshold == None:
        return allwords
    threshold = len(dicts)*threshold
    for word in allwords:
        count = 0
        for dict in dicts:
            if word in dict:
                count += 1
        if count < threshold:
            to_return.add(word)
    return to_return

def percentile(dict, cutoff=0.9):
    num_items = len(dict)
    threshold = int(float(num_items)*cutoff)
    hard_threshold(dict, threshold)

def hard_threshold(dict, threshold=10000):
    return sorted(dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:threshold]


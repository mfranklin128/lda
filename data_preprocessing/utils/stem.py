import porterstemmer

stemmer = porterstemmer.Stemmer()

def stem_list(words):
    for i in xrange(len(words)):
        words[i] = stem(words[i])
    return words

def stem(word):
    return stemmer(word)

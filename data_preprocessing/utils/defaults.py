import stem
import stopwords
import string

def lower_wrapper(words):
    return [word.lower() for word in words]

def single_char_wrapper(words):
    return [word for word in words if len(word) > 1]

def all_digits(words):
    def word_all_digits(word):
        for char in word:
            if not char in string.digits:
                return False
        return True
    toreturn = [word for word in words if not word_all_digits(word)]
    return toreturn

Preprocessors = [stem.stem_list, stopwords.remove_default, single_char_wrapper, lower_wrapper, all_digits]

import dict_filters

DictFilters = [dict_filters.hard_threshold]
PreDictFilters = [dict_filters.unique, dict_filters.ubiquitous]
PostDictFilters = [dict_filters.percentile, dict_filters.hard_threshold]

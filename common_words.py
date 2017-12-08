import re
from collections import Counter
import tqdm
import numpy as np

def nonuniq_words(text):
    return [e.lower().replace('ё', 'е') for e in re.findall("\w+", text, re.UNICODE)]


def uniq_words(text):
    return set(nonuniq_words(text))


def calculate_idfs(data):
    counter_data = Counter()
    uniq_data = set(data)
    for e in tqdm.tqdm_notebook(uniq_data, desc="calc idf"):
        set_words = uniq_words(e)
        counter_data.update(set_words)

    num_docs = len(uniq_data)
    print(num_docs)
    idfs = {}
    for word in counter_data:
        idfs[word] = np.log(num_docs / counter_data[word])
    return idfs


def calculate_counter(data):
    counter_data = Counter()
    uniq_data = set(data)
    for e in tqdm.tqdm_notebook(uniq_data, desc="calc freq"):
        set_words = nonuniq_words(e)
        counter_data.update(set_words)

    return counter_data


def calculate_idfs_chars(data, nchars=3):
    counter_data = Counter()
    uniq_data = set(data)
    for e in tqdm.tqdm_notebook(uniq_data, desc="calc idf"):
        s = ' '.join(nonuniq_words(e))
        set_chars = set([s[i:i + nchars] for i in range(len(s) - nchars) if ' ' not in s[i:i + nchars]])
        counter_data.update(set_chars)

    num_docs = len(uniq_data)
    print(num_docs)
    idfs = {}
    for word in counter_data:
        idfs[word] = np.log(num_docs / counter_data[word])
    return idfs
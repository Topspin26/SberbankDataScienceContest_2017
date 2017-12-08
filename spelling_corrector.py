import os
import tqdm
from common_words import uniq_words

class SpellingCorrector:
    def __init__(self, counts):
        self.alphabet='абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz'
        self.counts = counts

    def known(self, words):
        "Return the subset of words that are actually in the dictionary."
        return {w for w in words if w in self.counts}

    def edits0(self, word):
        "Return all strings that are zero edits away from word (i.e., just word itself)."
        return {word}

    def edits2(self, word):
        "Return all strings that are two edits away from this word."
        return {e2 for e1 in self.edits1(word) for e2 in self.edits1(e1)}

    def edits1(self, word):
        "Return all strings that are one edit away from this word."
        pairs = self.splits(word)
        deletes = [a + b[1:] for (a, b) in pairs if b]
        transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
        replaces = [a + c + b[1:] for (a, b) in pairs for c in self.alphabet if b]
        inserts = [a + c + b for (a, b) in pairs for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def splits(self, word):
        "Return a list of all possible (first, rest) pairs that comprise word."
        return [(word[:i], word[i:])
                for i in range(len(word) + 1)]

    def correct(self, word):
        "Find the best spelling correction for this word."
        # Prefer edit distance 0, then 1, then 2; otherwise default to word itself.
        e0 = self.known(self.edits0(word))
        e1 = []
        e2 = []
        if len(e0) == 0:
            e1 = self.known(self.edits1(word))
            e2 = self.known(self.edits2(word))
        candidates = []
        if word in self.counts:
            candidates += [[word, self.counts.get(word), 3]]
        else:
            candidates += [[word, 0, 0]]
        candidates += [[e, self.counts.get(e), 2] for e in e1]
        candidates += [[e, self.counts.get(e), 1] for e in e2]
        candidates = sorted(candidates, key=lambda x: -(x[2] + x[1] / 1e8))
        return candidates[0][0], candidates


def calcW2Spell(spel_cor, questions):
    if not os.path.exists('data/spell'):
        os.mkdir('data/spell')

    if not os.path.exists('data/spell/w2spell.txt'):
        w2spel = dict()
        for q in tqdm.tqdm_notebook(questions, total=len(questions)):
            for w in uniq_words(q):
                if w not in w2spel:
                    wcor, cands = spel_cor.correct(w)
                    w2spel[w] = [wcor, cands]
                    if wcor != w:
                        print(w, wcor, cands[:min(len(cands), 5)])

        with open('data/spell/w2spell.txt', 'w', encoding='utf-8') as fout:
            for w in sorted(w2spel):
                wcor, cands = w2spel[w]
                if wcor != w:
                    fout.write(w + '\t' + wcor + '\t' + '\t'.join([';'.join([str(ee) for ee in e]) for e in cands]) + '\n')

    w2spel = dict()
    with open('data/spell/w2spell.txt', encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            w = tokens[0]
            wcor = tokens[1]
            cands = []
            for e in tokens[2:]:
                arr = e.split(';')
                cands.append([arr[0], int(arr[1]), int(arr[2])])
            w2spel[w] = [wcor, cands]
    return w2spel
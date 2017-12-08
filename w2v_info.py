import numpy as np
import scipy as sp
from common_mystem import getMystemText
from common_words import uniq_words

class W2VInfo:
    def __init__(self, filename, counter_words, idfs_paragraphs, idfs_questions):

        self.all_words = set(counter_words.keys()) | set(idfs_paragraphs.keys()) | set(idfs_questions.keys())
        print(len(self.all_words))

        self.w2v = dict()
        with open(filename, encoding='utf-8', errors='replace') as fin:
            i = 0
            s = next(fin)
            n_lines = int(s.split(' ')[0])
            print(n_lines)
            for j,line in enumerate(fin):
                tokens = line.rstrip().split(' ')
                if tokens[0] not in self.all_words:
                    continue
                #print(tokens[0], end=' ')
                self.w2v[tokens[0]] = np.array([float(e) for e in tokens[1:]])
                i += 1
                if i % 1000 == 0:
                    print(i, end=' ')
                    #break
            print()


    def calcW2vScore(self, ss, all_questions2mystem, filter_pos={'S', 'A'}, agg_type='max', matrixReturn=False):
        tt = list(sorted(uniq_words(getMystemText(ss, all_questions2mystem, filter_pos=filter_pos))))
        tt = [e for e in tt if e in self.w2v]
        if len(tt) == 0:
            return 0
        a = np.zeros((len(tt), len(tt)))
        for i1,t1 in enumerate(tt):
            for i2,t2 in enumerate(tt):
                if i1 == i2:
                    a[i1, i2] = 0
                    continue
                if i1 <= i2:
                    a[i1, i2] = 1 - sp.spatial.distance.cosine(self.w2v[t1], self.w2v[t2])
                    a[i2, i1] = a[i1, i2]
        score = 0
        if agg_type == 'min':
            for i in range(len(tt)):
                a[i, i] = 1
            score = np.min(a)
        elif agg_type == 'minimax':
            score = np.min(np.max(a, axis=1))
        elif agg_type == 'max':
            score = np.max(a)
        else:
            raise
        if matrixReturn is False:
            return score
        return score, a, tt


    def calcMyScoreQP(self, ssq, ssp, all_questions2mystem, all_paragraphs2mystem, filter_pos={'S', 'A'}, agg_type='min', matrixReturn=False):
        ttq = list(sorted(uniq_words(getMystemText(ssq, all_questions2mystem, filter_pos=filter_pos))))
        ttp = list(sorted(uniq_words(getMystemText(ssp, all_paragraphs2mystem, filter_pos=filter_pos))))
        ttq = [e for e in ttq if e in self.w2v]
        ttp = [e for e in ttp if e in self.w2v]
        if len(ttq) == 0 or len(ttp) == 0:
            return 0
        twq = [self.w2v[e] for e in ttq]
        twp = [self.w2v[e] for e in ttp]
        a = np.zeros((len(ttq), len(ttp)))
        for i1, t1 in enumerate(ttq):
            for i2, t2 in enumerate(ttp):
                if t1 == t2:
                    a[i1, i2] = 1
                else:
                    a[i1, i2] = 1 - sp.spatial.distance.cosine(twq[i1], twp[i2])
        score = 0
        if agg_type == 'min':
            score = np.min(a)
        elif agg_type == 'minimax':
            score = np.min(np.max(a, axis=1))
        elif agg_type == 'max':
            score = np.max(a)
        else:
            raise

        if matrixReturn is False:
            return score
        return score, a, ttp, ttq

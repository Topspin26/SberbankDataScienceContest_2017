from common_mystem import getMystemText
from common_words import uniq_words
import numpy as np

def calcMyScore(ss, w2z, all_questions2mystem, filter_pos={'S', 'A', 'V'}, agg_type='min', matrixReturn=False):
    tt = list(sorted(uniq_words(getMystemText(ss, all_questions2mystem, filter_pos=filter_pos))))
    if len(tt) == 0:
        return 0
    a = np.zeros((len(tt), len(tt)))
    for i1, t1 in enumerate(tt):
        for i2, t2 in enumerate(tt):
            if i1 == i2:
                a[i1, i2] = 1
                continue
            if i1 <= i2:
                set1 = w2z.get(t1, set())
                set2 = w2z.get(t2, set())
                a[i1, i2] = ((len(set1 & set2) + 0.1)**2) / ((len(set1) + 0.2) * (len(set2) + 0.2))
                a[i1, i2] = a[i1, i2]**0.5
                a[i2, i1] = a[i1, i2]
    score = 0
    if agg_type == 'min':
        score = np.min(a)
    elif agg_type == 'minimax':
        for i in range(len(tt)):
            a[i, i] = 0
        score = np.min(np.max(a, axis=1))
    else:
        raise
    if matrixReturn is False:
        return score
    return score, a, tt


def calcMyScore2(ss, w2z, all_questions2mystem, filter_pos={'S'}, agg_type='min', w2z_sum_idfs=None, idfs_words=None, join_type='mul', matrixReturn=False):
    tt = list(sorted(uniq_words(getMystemText(ss, all_questions2mystem, filter_pos=filter_pos))))
    if len(tt) == 0:
        return 0
    a = np.zeros((len(tt), len(tt)))
    sets = list()
    for t1 in tt:
        sets.append(set(w2z.get(t1, dict()).keys()))

    for i1, t1 in enumerate(tt):
        for i2, t2 in enumerate(tt):
            if i1 == i2:
                a[i1, i2] = 1
                continue
            if i1 <= i2:
                set1 = sets[i1]
                set2 = sets[i2]
                if idfs_words is None:
                    n1 = len(set1)
                    n2 = len(set2)
                    n12 = len(set1 & set2)
                else:
                    n1 = w2z_sum_idfs.get(t1, 0.0)
                    n2 = w2z_sum_idfs.get(t2, 0.0)
                    n12 = 0.0
                    for ttt in set1 & set2:
                        n12 += idfs_words.get(ttt, 0.0)
                p1 = (n12 + 0.1) / (n1 + 0.2)
                p2 = (n12 + 0.1) / (n2 + 0.2)
                p12 = (n12 + 0.1) / (n1 + n2 - n12 + 0.2)
                if join_type == 'mul':
                    if agg_type == 'min':
                        a[i1, i2] = p1 * p2
                    elif agg_type == 'minimax':
                        a[i1, i2] = p12
                elif join_type == 'max':
                    a[i1, i2] = max(p1, p2)
                else:
                    raise

                a[i1, i2] = a[i1, i2]**0.5
                a[i2, i1] = a[i1, i2]

    score = 0
    if agg_type == 'min':
        score = np.min(a)
    elif agg_type == 'minimax':
        for i in range(len(tt)):
            a[i, i] = 0
        score = np.min(np.max(a, axis=1))
    else:
        raise
    if matrixReturn is False:
        return score
    return score, a, tt


def calcMyScoreQP(sq, sp, w2z, all_questions2mystem, all_paragraphs2mystem, filter_pos={'S', 'A', 'V'}, agg_type='min', join_type='mul', matrixReturn=False):
    ttq = list(sorted(uniq_words(getMystemText(sq, all_questions2mystem, filter_pos=filter_pos))))
    ttp = list(sorted(uniq_words(getMystemText(sp, all_paragraphs2mystem, filter_pos=filter_pos))))
    if len(ttq) == 0:
        return 0
    a = np.zeros((len(ttq), len(ttp)))
    for i1, t1 in enumerate(ttq):
        for i2, t2 in enumerate(ttp):
            set1 = w2z.get(t1, set())
            set2 = w2z.get(t2, set())
            n1 = len(set1)
            n2 = len(set2)
            n12 = len(set1 & set2)
            p1 = (n12 + 0.1) / (n1 + 0.2)
            p2 = (n12 + 0.1) / (n2 + 0.2)
            p12 = (n12 + 0.1) / (n1 + n2 - n12 + 0.2)
            if join_type == 'mul':
                if agg_type == 'min':
                    a[i1, i2] = p1 * p2
                elif agg_type == 'minimax':
                    a[i1, i2] = p12
            elif join_type == 'max':
                a[i1, i2] = max(p1, p2)
            else:
                raise
            a[i1, i2] = a[i1, i2]**0.5
    score = 0
    if agg_type == 'min':
        score = np.min(a)
    elif agg_type == 'minimax':
        score = np.min(np.max(a, axis=1))
    else:
        raise

    if matrixReturn is False:
        return score
    return score, a, ttp, ttq

import pandas as pd
from Levenshtein import distance
import re
import numpy as np
import sys

stop_words_nltk = ['и','в','во','не','что','он','на','я','с','со','как','а','то','все','она','так','его','но','да','ты','к','у','же','вы','за','бы','по','только','ее','мне','было','вот','от','меня','еще','нет','о','из','ему','теперь','когда','даже','ну','вдруг','ли','если','уже','или','ни','быть','был','него','до','вас','нибудь','опять','уж','вам','ведь','там','потом','себя','ничего','ей','может','они','тут','где','есть','надо','ней','для','мы','тебя','их','чем','была','сам','чтоб','без','будто','чего','раз','тоже','себе','под','будет','ж','тогда','кто','этот','того','потому','этого','какой','совсем','ним','здесь','этом','один','почти','мой','тем','чтобы','нее','сейчас','были','куда','зачем','всех','никогда','можно','при','наконец','два','об','другой','хоть','после','над','больше','тот','через','эти','нас','про','всего','них','какая','много','разве','три','эту','моя','впрочем','хорошо','свою','этой','перед','иногда','лучше','чуть','том','нельзя','такой','им','более','всегда','конечно','всю','между']
stop_words_sim2 = []#nltk.corpus.stopwords.words('russian')
stop_words_sim2 += ['как', 'какой', 'каков', 'где', 'когда', 'что', 'чем', 'кто', 'кем',
                    'сколько', 'зачем', 'почему', 'куда', 'откуда', 'чей', 'такой']
stop_words_sim2 += ['перечислять', 'называть', 'ли', 'происходить']

def loadLangs():
    langs = []
    try:
        dfLangs = pd.read_csv('data/langs.txt', sep='\t')
    except:
        dfLangs = pd.read_csv('langs.txt', sep='\t')
    ind = (dfLangs['Полное название'] != dfLangs['Сокращенное название']) & \
          (dfLangs['Сокращенное название'].apply(lambda x: x.find('см.') == -1))
    for e1, e2 in zip(dfLangs[ind]['Полное название'], dfLangs[ind]['Сокращенное название']):
        for e in e1.lower().replace('(', ' (').split(' '):
            if len(e) > 0:
                langs.append([e.replace('(', '').replace(')', ''), e2.lower() + '.'])
    langs.append(['латинский', 'лат.'])
    langs.append(['латынь', 'лат.'])
    langs.append(['латыня', 'лат.'])
    langs.append(['русский', 'рус.'])
    return langs

try:
    langs = loadLangs()
except:
    sys.stderr.write('similarity.py: No langs file\n')
    langs = []
#print(langs)

def cut(s, cnt):
    if len(s) < cnt + 1:
        return s
    return s[:-cnt]

def enrichBySinonims(text, tokens):
    s = set(tokens)
    s1 = {'%', 'процент', 'процентный'}
    if '%' in text or len(s1 & s) > 0:
        s |= s1

    for s2 in [{'г', 'гг', 'год'}, {'г', 'грамм'}, {'кг', 'килограмм'}, {'мг', 'миллиграмм'},
               {'м', 'метр'}, {'мм', 'миллиметр'}, {'см', 'сантиметр'}, {'км', 'километр'}]:
        if len(s2 & s) > 0:
            s |= s2
    for e1, e2 in langs:
        if e2 in text or e1 in s:
            s |= {e1, e2.replace('.', '')}
    for e in tokens:
        if (e[-1] == 'c' or e[-1] == 'с') and e[:-1].isdigit():
            s |= {'цельсий', 'цельсия'}
        if e.isdigit() and len(e) == 4:
            s |= {e[-2:], str(int(e[:2]) + 1)}

    for s1 in [{'XXI', '21', 'двадць', 'первый'},
               {'XX', '20', 'двадцатый', 'двадцать'},
               {'XIX', '19', 'девятнадцатый', 'девятнадцать'},
               {'XVIII', '18', 'восемнадцатый', 'восемнадцать'},
               {'XVII', '17', 'семнадцатый', 'семнадцать'},
               {'XVI', '16', 'шестнадцатый', 'шестнадцать'},
               {'XV', '15', 'пятнадцатый', 'пятнадцать'},
               {'XIV', '14', 'четырнадцатый', 'четырнадцать'},
               {'XIII', '13', 'тринадцатый', 'тринадцать'},
               {'XII', '12', 'двенадцатый', 'двенадцать'},
               {'XI', '11', 'одиннадцатый', 'одиннадцать'},
               {'X', '10', 'десятый', 'десять'},
               {'IX', '9', 'девятый', 'девять'},
               {'VIII', '8', 'восьмой', 'восемь'},
               {'VII', '7', 'седьмой', 'семь'},
               {'VI', '6', 'шестой', 'шесть'},
               {'V', '5', 'пятый', 'пять'},
               {'IV', '4', 'четвертый', 'четыре'},
               {'III', '3', 'третий', 'три'},
               {'I', '2', 'второй', 'два'},
               {'I', '1', 'первый', 'один'},
               {'30', 'тридцать', 'тридцатый'},
               {'40', 'сорок', 'сороковой'},
               {'50', 'пятьдесят', 'пятидесятый'},
               {'60', 'шестьдесят', 'шестидесятый'},
               {'70', 'семьдесят', 'семидесятый'},
               {'80', 'восемьдесят', 'восьмидесятый'},
               {'90', 'девяносто', 'девяностый'},
               {'00', 'нулевой'},
               ]:
        if len(s1 & s) > 0:
            s |= s1

    return s


def getIdfs(e, idfs_questions, idfs_paragraphs):
    if len(idfs_paragraphs) > 0:
        if len(idfs_questions) > 0:
            w = min(idfs_paragraphs.get(e, 5.0), idfs_questions.get(e, 5.0))
        else:
            w = idfs_paragraphs.get(e, 5.0)
    else:
        w = idfs_questions.get(e, 5.0)
    return w


def splitParagraphs(paragraph):
    arr = paragraph.split('.')
    res = []
    for e in arr:
        if len(e) > 10:
            res.append(e)
        else:
            if len(res) == 0:
                res.append(e)
            else:
                res[-1] += '.' + e
    res1 = [res[0]]
    #    print(res)
    for e in res[1:]:
        if len(res1[-1]) < 2 or res1[-1][-2] == ' ' or res1[-1][-2] == '.':
            res1[-1] += '.' + e
        else:
            res1.append(e)
    return res1


def splitParagraphsWindow(paragraph, ws=30):
    t_p = [e.lower().replace('ё', 'е') for e in re.findall("\w+", paragraph, re.UNICODE)]
    res = []
    i = 0
    while i < len(t_p):
        res.append(' '.join(t_p[i:min(i + ws, len(t_p))]))
        i += ws // 2
    return res

def calcSim1_list(qs, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=True):
    s_p, s_p_0, stop_words = prepare_paragraph(paragraph, stop_words_0, isCut)
    sim = []
    for i,q in enumerate(qs):
        qsim = calcSim1(q, s_p, s_p_0, stop_words, idfs_questions, idfs_paragraphs, isCut=isCut, isBreak=True)
        sim.append(qsim)
    return sim

def prepare_paragraph(paragraph, stop_words_0, isCut):
    t_p = [e.lower().replace('ё', 'е') for e in re.findall("\w+", paragraph, re.UNICODE)]
    t_p = list(enrichBySinonims(paragraph, t_p))

    t_p_0 = list(t_p)
    t_p = t_p_0.copy()
    stop_words = stop_words_0.copy()
    if isCut:
        t_p += [cut(e, 1) for e in t_p_0]
        t_p += [cut(e, 2) for e in t_p_0]
        t_p += [cut(e, 3) for e in t_p_0]

        stop_words += [cut(e, 1) for e in stop_words_0]
        stop_words += [cut(e, 2) for e in stop_words_0]

    s_p_0 = set(t_p_0 + stop_words_0)
    s_p = set(t_p + stop_words)
    return s_p, s_p_0, stop_words

def calcSim1_pre(question, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=True, isSplit=False,
             isSplitWindow=False, isBreak=False, w2spel={}):
    if isSplitWindow is True:
        return np.max(
            [calcSim1_pre(question, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=isCut, isSplit=False, isBreak=isBreak, w2spel=w2spel)
             for paragraph in splitParagraphsWindow(paragraph)])

    if isSplit is True:
        return np.max(
            [calcSim1_pre(question, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=isCut, isSplit=False, isBreak=isBreak, w2spel=w2spel)
             for paragraph in splitParagraphs(paragraph)])
    
    s_p, s_p_0, stop_words = prepare_paragraph(paragraph, stop_words_0, isCut)
    return calcSim1(question, s_p, s_p_0, stop_words, idfs_questions, idfs_paragraphs, isCut=isCut, w2spel=w2spel)
    
def calcSim1(question, s_p, s_p_0, stop_words, idfs_questions, idfs_paragraphs, isCut=True, isBreak=False, w2spel={}):
    glue = list()
    glue1 = list()

    t_q = [e.lower().replace('ё', 'е') for e in re.findall("\w+", question, re.UNICODE)]
    s_q = set(t_q)
    stop_words = set(stop_words)

    for w in t_q:
        if w in w2spel:
            wcor, _ = w2spel[w]
            if wcor != w:
                if wcor in s_p:
                    s_p.add(w)
                    s_p_0.add(w)
                    #print(w, wcor)

    if isBreak:
        if len(s_q & s_p - set(stop_words_nltk)) == 0:
            return 0
#    import sys
#    sys.stderr.write(' '.join(s_q & s_p) + '\n')
    
    sum1 = 0
    sum1_inter = 0
    for e in s_q:
        # print(e)
        if e in stop_words:
            continue
        w = getIdfs(e, idfs_questions, idfs_paragraphs)

        if e in s_p or isCut and (cut(e, 1) in s_p or cut(e, 2) in s_p or cut(e, 3) in s_p):
            # print(e)
            sum1 += w
            sum1_inter += w
        else:
            fl = 0
            if isCut == False:
                if len(e) > 2:
                    for z in s_p:
                        #if (e not in w2v or idfs_paragraphs.get(e, 8.0) >= 7.0):
                        if (idfs_paragraphs.get(e, 8.0) >= 7.0):
                            if distance(e, z) / min(len(e), len(z)) < 0.25:
                                fl = 1
                        else:
                            if len(e) >= 3 or idfs_paragraphs.get(e, 8.0) >= 5.0:
                                if distance(e, z) == abs(len(e) - len(z)) and distance(e, z) / min(len(e),
                                                                                                   len(z)) < 0.5:
                                    fl = 1
                        if fl == 1:
                            wz = getIdfs(z, idfs_questions, idfs_paragraphs)
                            sum1 += wz
                            sum1_inter += wz
                            glue.append([e, z])
                            # print(e, z)
                            break
            else:
                if len(e) > 2:
                    for z in s_p_0:
                        if distance(e, z) / min(len(e), len(z)) < 0.25:
                            fl = 1
                        if distance(e, z) == abs(len(e) - len(z)) and distance(e, z) / min(len(e), len(z)) < 0.5:
                            fl = 1
                        if fl == 1:
                            wz = getIdfs(z, idfs_questions, idfs_paragraphs)
                            sum1 += wz
                            sum1_inter += wz
                            glue1.append([e, z])
                            # print(e, z)
                            break

            if fl == 0:
                # print(e)
                w = min(w, 5.0)
                sum1 += w
                #    if sum1 > 0:
    return (sum1_inter + 0.1) * 1.0 / (sum1 + 0.2)
    #    return 0
    # return 2 * len(s1 & s2) / (len(s1) + len(s2))


def calcSim1_3chars(question, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=True, isSplit=False,
                    isSplitWindow=False, w2spel={}):
    if isSplitWindow is True:
        return np.max([calcSim1_3chars(question, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=isCut,
                                       isSplit=False, w2spel=w2spel)
                       for paragraph in splitParagraphsWindow(paragraph)])
    if isSplit is True:
        return np.max([calcSim1_3chars(question, paragraph, stop_words_0, idfs_questions, idfs_paragraphs, isCut=isCut,
                                       isSplit=False, w2spel=w2spel)
                       for paragraph in splitParagraphs(paragraph)])
    t_q = ' ' + ' '.join([e.lower().replace('ё', 'е') for e in re.findall("\w+", question, re.UNICODE)]) + ' '
    t_p = ' '.join([e.lower().replace('ё', 'е') for e in re.findall("\w+", paragraph, re.UNICODE)])
    t_p += ' '.join(stop_words_0)

    for w in set(t_q.split(' ')):
        if w in w2spel:
            wcor, _ = w2spel[w]
            if wcor != w:
                t_q = t_q.replace(' ' + w + ' ', ' ' + wcor + ' ')
    t_q = t_q.strip()

    s_p = set([t_p[i:i + 3] for i in range(len(t_p) - 3) if ' ' not in t_p[i:i + 3]])
    s_q = set([t_q[i:i + 3] for i in range(len(t_q) - 3) if ' ' not in t_q[i:i + 3]])

    sum1 = 0
    sum1_inter = 0
    for e in s_q:
        if len(idfs_paragraphs) > 0:
            if len(idfs_questions) > 0:
                w = min(idfs_paragraphs.get(e, 3.0), idfs_questions.get(e, 3.0))
            else:
                w = idfs_paragraphs.get(e, 3.0)
        else:
            w = idfs_questions.get(e, 3.0)

        if e in s_p or isCut and (cut(e, 1) in s_p or cut(e, 2) in s_p or cut(e, 3) in s_p):
            sum1 += w
            sum1_inter += w
        else:
            sum1 += min(w, 3.0)
            #    if sum1 > 0:
    return (sum1_inter + 0.1) * 1.0 / (sum1 + 0.2)
    #    return 0
    # return 2 * len(s1 & s2) / (len(s1) + len(s2))
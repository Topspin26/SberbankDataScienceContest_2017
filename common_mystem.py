import os
import json
import re
from string import printable
from pymystem3 import Mystem
mystem = Mystem()
import tqdm
import zlib
import common_zlib


def cleanString(s):
    return ''.join([x for x in s if (ord(x) < 256 and x in printable or x.isalpha() or x == '—')])


def getBad(data):
    badSymbols = set()
    badQuestions = set()
    for e in data:
        if len(cleanString(e)) != len(e):
            #print(e)
            badQuestions.add(e)
            for x in e:
                if not (ord(x) < 256 and x in printable or x.isalpha() or x == '—'):
                    badSymbols.add(x)
                    #print('------------------------------')
                #print(x, ord(x))
            #break
    return badSymbols, badQuestions


def runMystem(df_train, df_test, df_train_b, mode=''):
    all_paragraphs = set(list(df_train.paragraph) + list(df_train_b.paragraph) + list(df_test.paragraph))
    all_questions = set(list(df_train.question) + list(df_train_b.question) + list(df_test.question))
    print(len(all_paragraphs), len(all_questions))

    filename_p = 'data/mystem/all_paragraphs2mystem' + mode + '.txt'
    common_zlib.from_zlib(filename_p)

    if os.path.exists(filename_p):
        print('ok')
    else:
        print('run mystem for paragraphs')

        if not os.path.exists('data/mystem'):
            os.mkdir('data/mystem')

        with open(filename_p, 'w', encoding='utf-8') as fout:
            for e1 in tqdm.tqdm_notebook(sorted(all_paragraphs)):
                fout.write(e1 + '\t' + json.dumps(mystem.analyze(cleanString(e1)), ensure_ascii=False) + '\n')
        common_zlib.rm_zlib(filename_p)


    all_paragraphs2mystem = dict()
    with open(filename_p, encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            all_paragraphs2mystem[tokens[0]] = json.loads(tokens[1])

    common_zlib.to_zlib(filename_p)


    filename_q = 'data/mystem/all_questions2mystem' + mode + '.txt'
    common_zlib.from_zlib(filename_q)

    if os.path.exists(filename_q):
        print('ok')
    else:
        print('run mystem for questions')

        if not os.path.exists('data/mystem'):
            os.mkdir('data/mystem')
        with open(filename_q, 'w', encoding='utf-8') as fout:
            for e1 in tqdm.tqdm_notebook(sorted(all_questions)):
                fout.write(e1 + '\t' + json.dumps(mystem.analyze(cleanString(e1)), ensure_ascii=False) + '\n')
        common_zlib.rm_zlib(filename_q)


    all_questions2mystem = dict()
    with open(filename_q, encoding='utf-8') as fin:
        for line in fin:
            tokens = line.split('\t')
            all_questions2mystem[tokens[0]] = json.loads(tokens[1])

    common_zlib.to_zlib(filename_q)

    return all_paragraphs2mystem, all_questions2mystem

def calcText(d, save_upper=False, filter_pos=set()):
    res = []
    for e in d:
        p = getPOS(e)
        if len(filter_pos) == 0 or p in filter_pos:
            if ('analysis' in e) and (len(e['analysis']) > 0) and ('lex' in e['analysis'][0]):
                lex = e['analysis'][0]['lex']
                if save_upper is True:
                    if e['text'][0].istitle():
                        if e['text'].lower() == lex:
                            lex = e['text']
                        else:
                            lex = lex.title()
                res.append(lex)
            else:
                res.append(e['text'])
        else:
            if 'analysis' not in e:
                res.append(e['text'])

    return ''.join(res)


def calcPlainText(d, neg_filter_pos=set()):
    res = []
    for e in d:
        p = getPOS(e)
        if p not in neg_filter_pos:
            res.append(e['text'])
        else:
            if 'analysis' not in e:
                res.append(e['text'])

    return ' '.join(''.join(res).split())


def getMystemText(x, d, save_upper=False, filter_pos=set()):
    try:
        return calcText(d[x], save_upper=save_upper, filter_pos=filter_pos)
    except:
        print(x)
        raise


def getPOS(e):
    if ('analysis' in e) and (len(e['analysis']) > 0) and ('gr' in e['analysis'][0]):
        return e['analysis'][0]['gr'].split(',')[0].split('=')[0]
    else:
        if e['text'].isdigit():
            return 'NUMB'
        elif e['text'].isalpha():
            return 'ALPHA'
        elif e['text'] != ' ':
            return 'OTHER'
    return None

def calcPartOfSpeech(d, ngr=1):
    res = []
    for e in d:
        p = getPOS(e)
        if p is not None:
            res.append(p)
    if ngr > 1:
        res1 = []
        for i in range(2, ngr + 1):
            for j in range(len(res) - i):
                res1.append('_'.join(res[j:j + i]))
        res += res1
    return ' '.join(res)


def getPOS_for_last(e, text_pos = set()):
    if ('analysis' in e) and (len(e['analysis']) > 0) and ('gr' in e['analysis'][0]):
        pos = e['analysis'][0]['gr'].split(',')[0].split('=')[0]
        if pos == 'PR' and (e['text'][0].istitle() or e['text'][0] == 'с++'):
            pos = 'S'
        if pos in text_pos:
            return pos + '_' + e['analysis'][0]['lex']
        return pos
    else:
        for i in e['text']:
            if i.isdigit():
                return 'NUMB'
        if e['text'].isalpha():
            return 'ALPHA'
#        elif e['text'] != ' ':
#            return 'OTHER'
    return None


def calcA_S_CASE(d):
    res = []
    last = None
    for e in d:
        if ('analysis' in e) and (len(e['analysis']) > 0) and ('gr' in e['analysis'][0]):
            s = e['analysis'][0]['gr'].split(',')[0].split('=')[0]

            if s == 'A' or s == 'S':
                case = e['analysis'][0]['gr'].split('=')[1].split('|')[0].split(',')[0].lstrip('(')
                res.append(case)
                if last is not None:
                    res.append(last + '_' + s + case)
                last = s + case
            else:
                last = None
    return ' '.join(res)


dnames = {'PAD':{'им', 'род', 'дат', 'вин', 'твор', 'пр', 'парт', 'местн', 'зват'},
'VT':{'наст', 'непрош', 'прош'},
'CH':{'ед', 'мн'},
'L':{'1-л', '2-л', '3-л'},
'R':{'муж', 'жен', 'сред'},
'OTH':{'вводн', 'гео', 'затр', 'имя', 'искаж', 'мж', 'обсц', 'отч', 'прдк', 'разг', 'редк', 'сокр', 'устар', 'фам'}}

def getMystemInfo(e, names=['PAD', 'VT', 'CH', 'L', 'R', 'OTH']):
    ttt = e['analysis'][0]['gr'].replace('|', ',').replace('=', ',').replace('(', ',').replace(')', ',').split(',')
    res = dict()
    for name in names:
        res[name] = None
        ti = 100000
        for z in dnames[name]:
            if z in ttt:
                zi = ttt.index(z)
                if zi < ti:
                    res[name] = z
                    ti = zi
    return res

def calcA_V_S(d, col='CH', isE=False, filter_pos=set()):
    res = []
    last = None
    for e in d:
        if ('analysis' in e) and (len(e['analysis']) > 0) and ('gr' in e['analysis'][0]):
            s = e['analysis'][0]['gr'].split(',')[0].split('=')[0]

            if len(filter_pos) == 0 or s in filter_pos:
                sd = getMystemInfo(e, names=[col])
                if sd[col] is not None:
                    if isE:
                        res.append(s + sd[col])
                    if last is not None:
                        res.append(last + '_' + s + sd[col])
                    last = s + sd[col]
                else:
                    last = None
            else:
                last = None
    return ' '.join(res)


def calcPR_S_CASE(d):
    res = []
    lastPr = ''
    for e in d:
        if ('analysis' in e) and (len(e['analysis']) > 0) and ('gr' in e['analysis'][0]):
            s = e['analysis'][0]['gr'].split(',')[0].split('=')[0]
            if s == 'S':
                s = e['analysis'][0]['gr'].split('=')[1]
                res.append(lastPr + '_' + s.split('|')[0].split(',')[0].lstrip('('))
            elif s == 'PR':
                lastPr = e['text'].lower()
    return ' '.join(res)



def getMystemPartOfSpeech(x, d, ngr=1):
    try:
        return calcPartOfSpeech(d[x], ngr=ngr)
    except:
        print(x)
        raise

def getMystemPR_S_CASE(x, d):
    try:
        return calcPR_S_CASE(d[x])
    except:
        print(x)
        raise
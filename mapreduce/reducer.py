#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import io
import numpy as np
import re

sys.path.append('./../')

import imp
similarity = imp.load_source('similarity', 'similarity.py')
import process

def load_idfs(filename):
    idfs = dict()
    with open(filename, encoding='utf-8') as fin:
        for line in fin:
            tokens = line.strip().split('\t')
            idfs[tokens[0]] = float(tokens[1])
    return idfs

try:
    idfs_paragraphs = load_idfs('idfs_paragraphs.txt')
    idfs_questions = load_idfs('idfs_questions.txt')
except:
    idfs_paragraphs = load_idfs('data/idfs_paragraphs.txt')
    idfs_questions = load_idfs('data/idfs_questions.txt')


sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
p = None
pn = None
qs = list()
qsn = list()
for line in sys.stdin:
    line = line.strip()
    tokens = line.split('\t')
    if tokens[1] != '':
        qsn.append(tokens[1])
        qs.append(tokens[2])
    else:
        if p is not None and len(qs) > 0:
            sys.stderr.write(str(pn) + '\t' + p + '\n')
            out = process(p, pn, qs, qsn, idfs_questions, idfs_paragraphs)
            for e in out:
                sys.stdout.write(e)
        pn = tokens[0]
        p = tokens[2]
        qs = list()
        qsn = list()
if p is not None and len(qs) > 0:
    out = process(p, pn, qs, qsn, idfs_questions, idfs_paragraphs)
    for e in out:
        sys.stdout.write(e)

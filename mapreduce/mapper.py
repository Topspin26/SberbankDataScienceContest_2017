#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import io

sys.path.append('./../')

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
for line in sys.stdin:
    line = line.strip()
    tokens = line.split('\t')
    if tokens[0][0] == 'q':
        for i in range(10705):
        #for i in [4911]:
            sys.stdout.write('p' + str(i) + '\t' + tokens[0] + '\t' + tokens[2] + '\n')
    else:
        sys.stdout.write(tokens[0] + '\t' + '\t' + tokens[2] + '\n')
        

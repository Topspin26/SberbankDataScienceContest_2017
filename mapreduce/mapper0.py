#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import io

sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
for line in sys.stdin:
    sys.stdout.write(line)
        

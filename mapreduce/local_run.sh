#!/bin/bash

cat question_ms.txt paragraph_ms.txt | python3 mapper.py > output_mapper.txt
sort -t $'\t' -k1,2  output_mapper.txt > sort_output_mapper.txt
cat sort_output_mapper.txt | python3 reducer.py > output_reducer.txt
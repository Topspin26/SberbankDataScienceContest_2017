#!/bin/sh

INPUT_DIRNAME="/user/administrator/zhelubenkov/Sberbank/"

#hadoop jar $HADOOP_STREAMING_PATH \
#-D mapred.job.name='Sim' \
#-file mapper0.py \
#-mapper mapper0.py \
#-input ${INPUT_DIRNAME}/question_ms.txt \
#-output ${INPUT_DIRNAME}/question_ms


hadoop jar $HADOOP_STREAMING_PATH \
-D mapred.job.name='Sim' \
-D mapreduce.map.memory.mb=4096 \
-D mapreduce.map.java.opts=-Xmx3072m \
-D mapreduce.reduce.memory.mb=4096 \
-D mapreduce.reduce.java.opts=-Xmx3072m \
-D num.key.fields.for.partition=1 \
-D mapred.text.key.partitioner.options='-k1,1' \
-D stream.num.map.output.key.fields=2 \
-D stream.num.reduce.output.key.fields=2 \
-D mapred.output.key.comparator.class='org.apache.hadoop.mapred.lib.KeyFieldBasedComparator' \
-D mapred.text.key.comparator.options='-k1,1 -k2,2' \
-file mapper.py \
-file reducer.py \
-file similarity.py \
-file 'idfs_paragraphs.txt' \
-file 'idfs_questions.txt' \
-file 'langs.txt' \
-mapper mapper.py \
-reducer reducer.py \
-input ${INPUT_DIRNAME}/paragraph_ms.txt \
-input ${INPUT_DIRNAME}/question_ms \
-output ${INPUT_DIRNAME}/qp_sim_250 \
-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

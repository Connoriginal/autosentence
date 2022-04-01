#!/bin/sh
conda activate autosentence
cd ./data_preprocess
echo "Start data preprocess"
nohup python -u data_annotation.py -f kookmin_small.txt -p ./data/ 
echo "data annotate done"
cd ../data_analysis
nohup python -u data_analysis.py -f ../data_preprocess/data/kookmin_small_annotated.txt -p ./data/
echo "data analysis done"
cd ..
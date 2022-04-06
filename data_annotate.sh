#!/bin/sh
conda activate autosentence
cd ./data_preprocess
echo "Start data preprocess"
nohup python -u data_annotation.py -f kookmin.txt -p ./data/ 
echo "data annotate done"
cd ../data_analysis
nohup python -u data_analysis.py -f ../data_preprocess/data/kookmin_annotated.txt -p ./results/
echo "data analysis done"
cd ..
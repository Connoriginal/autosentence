#!/bin/sh
cd ./data_preprocess
echo "Start data preprocess"
nohup python -u data_annotation.py -f kookmin_small.txt -p ./results/ 
echo "data annotate done"
cd ../data_analysis
nohup python -u data_analysis.py -f ../data_preprocess/results/kookmin_small_annotated.txt -p ./results/
echo "data analysis done"
cd ..
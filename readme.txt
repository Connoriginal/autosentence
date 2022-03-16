******** 사용법 *********
python data_annotation.py -f (읽고자 하는 파일 경로 (필수)) -p (저장하고자 하는 파일 경로(필수 아님, default는 현재 디렉토리))
예시 : 1. python data_annotation.py -f ./kookmin.txt -p ./data/
      2. python data_annotation.py -f ./kookmin.txt

******** requirements ********

- https://github.com/bluedisk/hangul-toolkit
한글 자모 분리 python library
pip install hgtk (conda install 은 존재하지 않기 때문에 pip install을 사용해야 한다)
python 3.6 까지 테스트가 되어있기 때문에 python version 3.6x를 추천 한다.



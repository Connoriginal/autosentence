import hgtk
import argparse
import time
from pykospacing import Spacing # https://github.com/haven-jeon/PyKoSpacing
from hanspell import spell_checker # https://github.com/ssut/py-hanspell
 
# Read .txt file
def read_txt(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    f.close()
    return lines

# Write .txt file start at the end of the file
def write_txt(file_name, list):
    with open(file_name, 'w', encoding='utf-8') as f:
        for line in list:
            f.write(line + '\n')
    f.close()

# Make Sentence by word list
def make_sentence(word_list):
    sentence = ""
    for word in word_list:
        sentence += word + ' '
    return sentence

# Decompose words
def decompose(line):
    result = ""
    for word in line:
        if hgtk.checker.is_hangul(word):
            result += hgtk.text.decompose(word)[0]
        else:
            result += word
    return result

# Read sentence length & check word length
def sentence_length(line):
    result = 0
    flag = True
    for i in line.split(' '):
        temp = len(i)
        if(temp >= MAX_WORD) :
            flag = False
            break
        result += temp
    
    if flag :
        return flag, result
    else :
        return flag, 0

# set global variable
MIN_LEN = 7
MAX_WORD = 10

def main():
    parser = argparse.ArgumentParser(description='Data annotation')
    parser.add_argument('-f','--file', help='File path to annotate', required=True)
    parser.add_argument('-p','--path', default='./', help='Path to save the annotated file')
    args = parser.parse_args()

    # get filename frome file path with out .txt
    file_name = args.file.split('/')[-1].split('.')[0]

    # path for annotated file
    PATH = args.path

    # upload txt file
    corpus = read_txt(args.file)

    # list of not corpus word
    not_corpus = ['"','\'', '.', ',', '!', '?', ':', ';', '-', '\n', '\t', '\r']

    # make list for initial clean data (Erase not corpus word & non-hangul word)
    init_corpus = [] ## tuple of (sentence, sentence length(only word))
    
    # Spacing object
    spacing = Spacing()

    print("Start cleaning data...")
    t0 = time.time()
    t1 = time.time()

    # make list for initial clean data (Erase not corpus word & non-hangul word)
    for iter,line in enumerate(corpus) :

        # print progress
        if iter % 1000000 == 0:
            print("{} lines cleaned".format(iter))
            t2 = time.time()
            print("{} seconds".format(t2 - t1))
            t1 = t2
        
        temp = ""
        for word in line :
            if word not in not_corpus and hgtk.checker.is_hangul(word) or word == ' ':
                if word != ' ':
                    temp += word
                else:
                    if temp != '' and temp[-1] != ' ':
                        temp += word

        check_word, length = sentence_length(temp)

        # if sentence length is over MAX_WORD and under MIN_LEN, delete sentence
        if check_word and length >= MIN_LEN:    
            # init_corpus.append((spacing(temp), length))
            init_corpus.append(temp)
    
    # test for spacing
    write_txt(PATH + file_name + '_init.txt', init_corpus)
    print("Saved init corpus")

    # make list for results
    clean_corpus = []
    annotated_corpus = []

    # print cleaning data time(min) and start annotating
    t2 = time.time()
    print("Cleaning data time(min) :", (t2 - t0) / 60)
    print("Start annotating data...")
    t0 = time.time()
    t1 = time.time()
    
    # split the sentences by minimum word length 5 & annotate
    for iter, (line) in enumerate(init_corpus):
        # print progress
        if iter % 100000 == 0:
            print(iter, "sentences have been annotated")
            t2 = time.time()
            print("{} seconds".format(t2 - t1))
            t1 = t2
            
        # apply spacing

        # pykospacing version
        line = spacing(line)

        # hanspell version
        # res = spell_checker.check(line)
        # line = res.checked
        
        que = line.split(' ')
        que_size = len(que)

        
        flag = False
        st = 0
        en = 2
        while en < que_size :

            if sentence_length(make_sentence(que[st:en]))[1] >= MIN_LEN :

                if en == que_size -1 or sentence_length(make_sentence(que[en:]))[1] < MIN_LEN :
                    temp = make_sentence(que[st:])
                    que = []
                    que_size = 0
                    flag = True

                else :
                    temp = make_sentence(que[st:en])
                    st = en
                    en += 1
                
                clean_corpus.append(temp)
                annotated_corpus.append(decompose(temp))

            if flag : 
                break

            en += 1


    
    # print annotating data time(min)
    t2 = time.time()
    print("Annotating data time(min) :", (t2 - t0) / 60)
    print("Total lines :", iter)

    # Debugging
    # for i,word in enumerate(clean_corpus) :
    #     if sentence_length(word) < MIN_LEN:
    #         print(word,i)
    
    # write clean & annotated file
    write_txt(PATH + file_name + '_clean.txt', clean_corpus)
    write_txt(PATH + file_name + '_annotated.txt', annotated_corpus)


if __name__ == '__main__' :
    main()


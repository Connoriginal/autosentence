import hgtk
import argparse
import time

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
MIN_LEN = 5
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
            init_corpus.append((temp, length))
    
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
    for iter, (line, total_num) in enumerate(init_corpus):

        # print progress
        if iter % 1000000 == 0:
            print(iter, "sentences have been annotated")
            t2 = time.time()
            print("{} seconds".format(t2 - t1))
            t1 = t2

        que = line.split(' ')
        que_size = len(que)
        que_length = total_num

        while que != []:
            
            # 남은 어절의 개수가 2 보다 작거나, 남은 어절의 길이가 5보다 작을때 다 합침
            if len(que[2:]) < 2 or sentence_length(make_sentence(que[2:]))[1] < MIN_LEN :
                temp = make_sentence(que)
                clean_corpus.append(temp)
                annotated_corpus.append(decompose(temp))
                que = []
                break
            
            temp_len = 0
            temp_size = 0

            for idx in range(2,que_size):
                if sentence_length(make_sentence(que[:idx]))[1] >= MIN_LEN:
                    temp_len = sentence_length(make_sentence(que[:idx]))[1]
                    temp_size = idx
                    break

                
                if len(que[idx+1:]) < 2 or sentence_length(make_sentence(que[idx+1:]))[1] < MIN_LEN :
                    temp_len = que_length
                    temp_size = que_size
                    break
            
            temp = make_sentence(que[:temp_size])
            clean_corpus.append(temp)
            annotated_corpus.append(decompose(temp))
            que = que[temp_size:]
            que_length -= temp_len
            que_size -= temp_size

    
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


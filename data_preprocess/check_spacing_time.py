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

def main():
    parser = argparse.ArgumentParser(description='Data annotation')
    parser.add_argument('-f','--file', help='Files to check time', required=True)
    parser.add_argument('-p','--path', default='./', help='Path to save the spaced done file')
    args = parser.parse_args()

    # get filename frome file path with out .txt
    file_name = args.file.split('/')[-1].split('.')[0]

    # path for saving file
    PATH = args.path

    # read txt file
    corpus = read_txt(args.file)

    # list for pykospace & hanspell
    pyko = []
    hansp = []

    # Spacing object
    spacing = Spacing()

    print("Start checking time for pykospacing")
    t0 = time.time()

    for iter,line in enumerate(corpus) :
        line = spacing(line)
        pyko.append(line)
        if iter == 1000 :
            t1 = time.time()
            print("{:.2f} seconds".format(t1-t0))
            break

    print("Start checking time for hanspell")
    t0 = time.time()

    for iter,line in enumerate(corpus) :
        res = spell_checker.check(line)
        line = res.checked
        hansp.append(line)
        if iter == 1000 :
            t1 = time.time()
            print("{:.2f} seconds".format(t1-t0))
            break
    
    write_txt(PATH + file_name + '_pyko_1000.txt', pyko)
    write_txt(PATH + file_name + '_hansp_1000.txt', hansp)


if __name__ == '__main__' :
    main()


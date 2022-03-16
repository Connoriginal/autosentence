import argparse
import pandas as pd
import pickle
import time

# Read .txt file
def read_txt(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    f.close()
    return lines

# Write .txt file 
def write_txt(file_name, dict):
    with open(file_name, 'w', encoding='utf-8') as f:
        for key, value in dict.items():
            f.write(key + ' : ' + str(value) + '\n')
    f.close()

# Write .csv file
def write_csv(file_name, dict):
    df = pd.DataFrame(dict.items(), columns=['jaum', 'count'])
    df.to_csv(file_name, encoding='utf-8', index=False)

# Save dictionary to pickle file
def save_pickle(file_name, dict):
    with open(file_name, 'wb') as fw:
        pickle.dump(dict, fw)
    
def main():
    parser = argparse.ArgumentParser(description='Data annotation')
    parser.add_argument('-f','--file', help='File path to analyize', required=True)
    parser.add_argument('-p','--path', default='./', help='Path to save the analyized file')
    args = parser.parse_args()
    
    # get filename frome file path with out .txt
    file_name = args.file.split('/')[-1].split('.')[0]

    # path for annotated file
    PATH = args.path
    
    # list of jaum
    ja = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
    
    # list of not corpus word
    not_corpus = [' ','"','\'', '.', ',', '!', '?', ':', ';', '-', '\n', '\t', '\r']
    
    # make a list of 5 character of jaum
    jaum_list = []
    for i in range(len(ja)):
        for j in range(len(ja)):
            for k in range(len(ja)):
                for l in range(len(ja)):
                    for m in range(len(ja)):
                        jaum_list.append(ja[i] + ja[j] + ja[k] + ja[l] + ja[m])
    
    # make a dictionary of jaum_list : numder of jaum
    jaum_dict = {i : 0 for i in jaum_list}
    
    print("start counting...")
    t0 = time.time()

     # upload txt file
    corpus = read_txt(args.file)
    t1 = time.time()
    print("time for read the .txt file : {:.2f} (min)".format((t1-t0)/60))
    
    # read five character of each line and add count to dictionary
    iter = 1

    for line in corpus:

        if iter % 1000000 == 0 :
            t2 = time.time()
            print("{} line checked : {:.2f} seconds".format(iter, t2-t1))
            t1 = t2

        temp = ""
        for word in line:
            if word in not_corpus :
                continue
            if word not in ja :
                break
            
            temp += word

            if len(temp) == 5 :
                jaum_dict[temp] += 1
                break

        iter += 1
    
    t2 = time.time()
    print("Finished... cost {:.2f} minutes".format((t2-t0)/60))
    # Debugging
    # count = 0
    # for i in jaum_dict.items():
    #     count += i[1]
    # print("count :", count)
    # print("line_count :", line_count)
    
    # write txt, excel, pickle file
    write_txt(PATH + file_name + '_jaum_count.txt', jaum_dict)
    write_csv(PATH + file_name + '_jaum_count.csv', jaum_dict)
    save_pickle(PATH + file_name + '_jaum_count.pickle', jaum_dict)
    
if __name__ == '__main__' :
    main()
    
    
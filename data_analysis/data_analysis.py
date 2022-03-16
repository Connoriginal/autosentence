import argparse
import pandas as pd
import pickle

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
    
    # upload txt file
    corpus = read_txt(args.file)
    
    # read five character of each line and add count to dictionary
    # line_count = 0 ## for debugging
    for line in corpus:
        # remove ' ' from each line and read front five character
        line = line.replace(' ', '')
        jaum_dict[line[0:5]] += 1
        # line_count += 1 ## for debugging
    
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
    
    
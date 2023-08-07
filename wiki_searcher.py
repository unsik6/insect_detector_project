import os
import argparse
from tqdm import tqdm
from datasets import load_dataset
import pandas as pd


def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keywords', nargs='+', type=str, help='keywords searched.')
    parser.add_argument('--parsed', action='store_true', help='Get also the version erased meta data of HTML or Markdown.')
    pars = parser.parse_args()
    print(vars(pars))
    if pars.keywords == None:
        print('Error: There is no keyword.')
        exit(1)
    return pars


# Load wiki dataset
def load_wiki():
    global raw_dataset
    global parsed_dataset
    raw_dataset = load_dataset("heegyu/namuwiki")
    parsed_dataset = load_dataset("heegyu/namuwiki-extracted")
    print('Loading dataset is completed')


# Search keyword in wiki DB
def search_word(search_word, isParse):
    print('Start searching: ' + search_word)
    searched_datas = []
    collected_cnt = 0
    for row in tqdm(raw_dataset['train']):
        title = row['title']
        if title.find(search_word) > -1:
            searched_datas.append([row['title'], row['text']])
            collected_cnt += 1
    print('End searching: ' + search_word + ' ' + str(collected_cnt) + ' items is collected.')
    cols=['title', 'text']
    pd_store_data = pd.DataFrame(searched_datas, columns = cols)    
    path = os.getcwd()
    file_name = path + '\\' + search_word + '.xlsx'
    pd_store_data.to_excel(file_name, encoding='utf-8-sig')
    print('Storing .xlsx complete: ' + search_word)
    
    if isParse:
        print('Start searching (parsed version): ' + search_word)
        searched_datas = []
        cnt = 1
        collected_cnt = 0
        for row in tqdm(parsed_dataset['train']):
            title = row['title']
            if title.find(search_word) > -1:
                searched_datas.append([row['title'], row['text']])
                collected_cnt += 1
            cnt+=1
        print('End searching (parsed version): ' + search_word + ' ' + str(collected_cnt) + ' items is collected.')
        cols=['title', 'text']
        pd_store_data = pd.DataFrame(searched_datas, columns = cols)    
        path = os.getcwd()
        file_name = path + '\\' + search_word + 'parsed.xlsx'
        pd_store_data.to_excel(file_name, encoding='utf-8-sig')
        print('Storing (parsed version) .xlsx complete: ' + search_word)


def main(pars):
    load_wiki()
    keywords = pars.keywords
    for word in keywords:
        search_word(word, pars.parsed)


if __name__ == '__main__':
    pars = parsing()
    main(pars)
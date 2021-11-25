import pandas as pd
import json
import jieba
import os
from tqdm import tqdm

def stopwords_list(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',
                                               encoding='utf-8').readlines()]
    stopwords.append("\n")
    stopwords.append(" ")
    return stopwords

def load_json(filename):
    with open("data/" + filename, encoding="utf-8") as fp:
        s = json.load(fp)['text']
    return s


def get_word_list(s, stopwords):
    word_list = []
    sentence_seg = jieba.cut(s)
    for word in sentence_seg:
        if word not in stopwords:
            if word != "\t":
                word_list.append(word)
    return list(set(word_list))

if __name__ == '__main__':

    stopwords = stopwords_list("hit_stopwords.txt")
    file_list = os.listdir("data")
    text_list, all_word_list, index_list = [], [], []

    for i in tqdm(file_list[:]):
        word_list = get_word_list(load_json(i), stopwords)
        text_list.append(word_list)

    df = pd.DataFrame({"file":file_list[:], "word_list":text_list})
    df.to_csv("正排索引.csv", index=False)
    all_data_dict = {}
    file, word = [], []
    for row in tqdm(df.values):
        for j in row[1]:
             file.append(row[0])
             word.append(j)

    all_data_dict['file'] = file
    all_data_dict['word'] = word
    all_data = pd.DataFrame.from_dict(all_data_dict)
    del all_data_dict

    all_data_index = all_data.groupby(["word"])['file'].apply(list).reset_index()
    print(all_data_index)
    all_data_index.to_csv("倒排索引.csv", index=False)


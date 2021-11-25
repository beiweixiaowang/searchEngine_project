import pandas as pd
# from SE_project.get_index import  stopwords_list, get_word_list
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import pdist
import json
import jieba
from Exp8 import Exp8_1

def stopwords_list(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r',
                                               encoding='utf-8').readlines()]
    stopwords.append("\n")
    stopwords.append(" ")
    return stopwords

def get_word_list(s, stopwords):
    word_list = []
    sentence_seg = jieba.cut(s)
    for word in sentence_seg:
        if word not in stopwords:
            if word != "\t":
                word_list.append(word)
    return list(set(word_list))

def process_text(word_list):
    doc_list = []
    for text in word_list:
        doc_list.append(' '.join(text))
    return doc_list

def get_tfidf_matrix(doc_list, file_list):
    tfidf_vec = TfidfVectorizer(lowercase=False)
    tfidf_matrix = tfidf_vec.fit_transform(doc_list)
    words = tfidf_vec.vocabulary_
    tfidf = tfidf_matrix.toarray()
    df = pd.DataFrame(tfidf.T, columns=file_list,
                      index=words)
    return df

def get_cosine_dis(df):
    cosine_matrix = 1 -pdist(df.values.T, "cosine")[:len(df.columns) - 1]
    new_df = pd.DataFrame({"filename":df.columns[1:],
                           "cosine_similarity":cosine_matrix
                           }).sort_values(by="cosine_similarity", ascending=False).reset_index(drop=True)
    return new_df


def load_json(filename):
    with open("data/" + filename, encoding="utf-8") as fp:
        s = json.load(fp)
    return s

def search(df_index, df_word, search_word, stopwords):
    search_word_list = get_word_list(search_word, stopwords=stopwords)
    keyword = ' '.join(search_word_list)
    df = df_index[df_index['word'].isin(search_word_list)]
    file_list = df['file'].apply(lambda x: eval(x)).tolist()
    file_list = list(set(sum(file_list, [])))
    file_list = ['search_word'] + file_list
    word_list = df_word[df_word['file'].isin(file_list)]['word_list'].apply(lambda x :eval(x)).tolist()
    word_list = [search_word_list] + word_list
    doc_list = process_text(word_list)
    df_tfidf = get_tfidf_matrix(doc_list, file_list)
    df_cosine = get_cosine_dis(df_tfidf)
    data = []
    for i in df_cosine['filename']:
        temp_dict = load_json(i)
        c = Exp8_1.CreateAbstract(temp_dict['text'], 60)
        temp_dict['summary'] = c.getResult(keyword)
        data.append(temp_dict)
    return data



if __name__ == '__main__':
    df_index = pd.read_csv("倒排索引.csv")
    df_word = pd.read_csv("正排索引.csv")
    search_word = "习近平总书记"
    stopwords = stopwords_list("hit_stopwords.txt")
    df_cosine = search(df_index, df_word, search_word, stopwords)
    print(df_cosine)





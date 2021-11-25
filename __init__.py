from flask import Flask, render_template, request
from SE_project.search import search
from SE_project.get_index import stopwords_list
import json
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/search_show", methods=['post'])
def get_search():
    df_index = pd.read_csv("倒排索引.csv")
    df_word = pd.read_csv("正排索引.csv")
    stopwords = stopwords_list("hit_stopwords.txt")
    searchWord = request.form.get("searchWord")
    data_list = search(df_index=df_index, df_word=df_word, search_word=searchWord, stopwords=stopwords)
    return render_template("search_engine.html", list = data_list)


if __name__ == '__main__':
    app.run(debug=True)
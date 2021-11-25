import pandas as pd
import requests
from lxml import etree
from requests.exceptions import RequestException
from queue import Queue
from threading import Thread
import time
import re
import json



def get_html(url):
    try:
        response = requests.get(url=url, headers=headers, timeout=5)
        if response.status_code == 200:
            response.encoding = "utf-8"
            return response.text
    except RequestException:
        return None

def get_text_title(url):
    data = dict()
    data['url'] = url
    html = get_html(url)
    try:
        tree = etree.HTML(html)
        title = tree.xpath('/html/body/div[2]/h1/text()')
        text = tree.xpath('//*[@id="artibody"]/p/text()')
        if title != [] and text != []:
            data['title'] = title[0]
            data['text'] = '\n'.join([i.replace("\u3000\u3000", '') for i in text])
            return data
        else:
            return None
    except:
        return None

def run(in_q, out_q):
    while in_q.empty() is not True:
        url = in_q.get()
        data = get_text_title(url=url)
        if data != None:
            out_q.put(data)
        print(out_q.qsize(), url)
        in_q.task_done()


def write_file(file_list):
    for i in range(len(file_list)):
        js_data = json.dumps(file_list[i])
        with open('data/' + str(i) + '.json', "w", encoding="utf-8") as f:
            f.write(js_data)

if __name__ == '__main__':
    start = time.time()
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                             " AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/93.0.4577.82 Safari/537.36"}
    data = pd.read_csv("url.txt")
    url_list = list(data.values.reshape(-1))

    input_queue = Queue()
    output_queue = Queue()
    for i in url_list[:]:
        input_queue.put(i)
    print(input_queue.qsize())
    for index in range(10):
        thread = Thread(target=run, args=(input_queue, output_queue))
        thread.daemon = True
        thread.start()

    input_queue.join()
    end = time.time()
    print("总耗时：", end - start)
    print(output_queue.qsize())
    file_list = list(output_queue.queue)
    write_file(file_list)




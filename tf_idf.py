from os import listdir
from os.path import isfile
from collections import defaultdict

from math import log
from underthesea import word_tokenize
from numpy.core.defchararray import isalpha, isdigit, lower, splitlines
from sklearn.preprocessing import normalize
import numpy as np
import re


def gather_data():
    path = "..\\data\\"
    dirs = [path + dir_name + "\\"
            for dir_name in listdir(path)
            if not isfile(path + dir_name)]

    train_dir, test_dir = (
        dirs[0], dirs[1]) if 'train' in dirs[0] else (dirs[1], dirs[0])

    
    topic_list = [
        topic for topic in listdir(train_dir)
    ]
    topic_list.sort()

    with open(".\\vietnamese-stopwords.txt", encoding='UTF-8') as f:
        stop_words = [word
                        for word in f.read().splitlines()]

    def collect_data(p_dir, topic_list):
        data = []
        for topic_id, topic in enumerate(topic_list):
            label = topic_id
            path = p_dir + topic + "\\"
            files = [(filename, path + filename)
                    for filename in listdir(path)
                    if isfile(path + filename)]
            
            files.sort()

            for filename, filepath in files:
                with open(filepath, encoding='UTF-16') as f:
                    # print(filepath)
                    text = f.read()

                    words = []
                    for item in word_tokenize(text):
                        item = item.strip()
                        item = re.sub('[^A-Za-z]+', '', item)
                        word = item.lower()
                        if word not in stop_words and len(word) < 20 and len(word) > 0:
                            words.append(word)


                context = '<>'.join(words)
                data.append(str(label) + '<uuuu>' + filename + '<uuuu>' + context)

        return data

    train_data = collect_data(train_dir, topic_list)
    # test_data = collect_data(test_dir, topic_list)

    with open("..\\data\\train_data.txt", mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(train_data))
    
    # with open("..\\data\\test_data.txt", mode='w', encoding='UTF-8') as f:
    #     f.write('\n'.join(test_data))

gather_data()

def gen_vocabulary(data_path):
    with open(data_path, encoding='UTF-8') as f:
        data = f.read().splitlines()
    
    vocabulary = []
    
    for line in data:
        context = line.split('<uuuu>')[-1]
        words = context.split('<>')
        vocabulary = set(vocabulary).union(set(words))
    
    with open('..\\data\\vocabulary.txt', 'w', encoding='UTF-8') as f:
        f.write('\n'.join(vocabulary))

# gen_vocabulary('..\\data\\train_data.txt')

def compute_idf(data_path, vocab_path):
    with open(data_path, encoding='UTF-8') as f:
        data = f.read().splitlines()
    
    with open(vocab_path, encoding='UTF-8') as f:
        vocab = [line.split('<fff>: ')[0]
                for line in f.read().splitlines()]

    N = len(data)

    idf_dict = dict.fromkeys(vocab, 0)

    for line in data:
        context = line.split('<uuuu>')[-1]
        print(line.split('<uuuu>')[1])
        words = [word.strip()
                for word in context.split('<>')
                if word in vocab]

        term_count = defaultdict(int)
        for word in words:
            term_count[word] += 1
        
        for word, val in term_count.items():
            if val != 0:
                idf_dict[word] += 1
    
    for word, val in idf_dict.items():
        if val != 0:
            idf_dict[word] = log(1.0 * N / val)
        else:
            del(idf_dict[word])
    
    with open('..\\data\\vocabulary_idf_t.txt', 'w', encoding='UTF-8') as f:
        for key, value in idf_dict.items():
            f.write(str(key) + ': ' + str(value) + '\n')

    return idf_dict

# compute_idf('..\\data\\train_data.txt', '..\\data\\vocab3.txt')

def compute_tfidf(data_path, vocab_idf_path):
    with open(data_path, encoding='UTF-8') as f:
        data = [(line.split('<uuuu>')[0], line.split('<uuuu>')[1], line.split('<uuuu>')[2])
                for line in f.read().splitlines()]
    
    # vocab_idf = compute_idf('..\\data\\train_data.txt', '..\\data\\vocab3.txt')
    with open(vocab_idf_path, encoding='UTF-8') as f:
        vocab_idf = [(line.split(': ')[0], float(line.split(': ')[1]))
                    for line in f.read().splitlines()]
        # V = len(vocab_idf)

        word_ids = [(word, index)
                    for index, (word, idf) in enumerate(vocab_idf)]
        word_ids = dict(word_ids)

        vocab_idf = dict(vocab_idf)
    
    # D = len(data)

    data = enumerate(data)

    tf_idf = []
    
    for index, doc in data:
        label, file_name, context = doc

        print(file_name)
        words = [word.strip()
                for word in context.split('<>')
                if word in vocab_idf.keys()]
        
        max_tf = max([words.count(word) for word in words])
        tf_idf_doc = []
        sum_square = 0.0
        for word in words:
            tf = words.count(word)
            tf_idf_word = tf * 1.0 / max_tf * vocab_idf[word]
            tf_idf_doc.append((word_ids[word], tf_idf_word))
            sum_square += tf_idf_word ** 2

        doc_tf_idf_nomalized = [str(index1) + ': ' + str(tf_idf_word / sum_square)
                                for index1, tf_idf_word in tf_idf_doc]
        
        doc = '  '.join(doc_tf_idf_nomalized)
        tf_idf.append((label, index, doc))
    
    with open('..\\data\\tf_idf.txt', 'w') as f:
        for label, index, doc in tf_idf:
            f.write(label + '<fff>' + str(index) + '<fff>: ' + doc + '\n')

# compute_tfidf('..\\data\\train_data.txt', '..\\data\\vocabulary_idf.txt')



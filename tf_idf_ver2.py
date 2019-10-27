import os
import gensim
import scipy.sparse
import numpy as np

from pyvi import ViTokenizer, ViPosTagger
from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm


dir_path = os.path.dirname(os.path.realpath(os.getcwd()))
dir_path = os.path.join(dir_path, 'data')

def gather_data():
    dirs = [os.path.join(dir_path, dir_name)
            for dir_name in os.listdir(dir_path)
            if not os.path.isfile(os.path.join(dir_path, dir_name))]
    train_dir, test_dir = (dirs[0], dirs[1]) if 'train' in dirs[0] else (dirs[1], dirs[0])
    
    topic_list = [
        topic for topic in os.listdir(train_dir)
    ]
    topic_list.sort()

    with open(".\\vietnamese-stopwords.txt", encoding='UTF-8') as f:
        stop_words = [word.strip().replace(' ', '_')
                        for word in f.read().splitlines()]

    def collect_data(p_dir, topic_list):
        data_text = []
        data_term = []

        for topic_id, topic in enumerate(topic_list):
            label = topic_id
            path = os.path.join(p_dir, topic)
            files = [(filename, os.path.join(path, filename))
                    for filename in os.listdir(path)
                    if os.path.isfile(os.path.join(path, filename))]

            print(topic)
            for filename, filepath in tqdm(files):
                with open(filepath, encoding='UTF-16') as f:
                    text = f.read()
                    text = [word.strip().replace(' ', '_')
                            for word in word_tokenize(text)]
                    text = ' '.join(text)

                    text = gensim.utils.simple_preprocess(text)
                    text = ' '.join(text)
                    text = ViTokenizer.tokenize(text)
                    data_text.append(text)

                    words = []
                    for item in text.split():
                        item = item.strip()
                        word = item.lower()
                        if word not in stop_words and len(word) < 20 and len(word) > 0:
                            words.append(word)
                    context = '<>'.join(words)
                    data_term.append(str(label) + '<uuuu>' + filename + '<uuuu>' + context)

        return data_term, data_text

    train_data_term, train_data_text = collect_data(train_dir, topic_list)

    with open("..\\data\\train_data.txt", mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(train_data_term))
    
    with open("..\\data\\train_data_line.txt", mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(train_data_text))

# gather_data()

def compute_tf_idf(data_path):
    with open(data_path, mode='r', encoding='UTF-8') as f:
        data = [line.split('<uuuu>')[-1].replace('<>', ' ')
                for line in f.read().splitlines()]
        

    tf_idf_vec = TfidfVectorizer(analyzer='word', max_features=30000)
    tf_idf_vec.fit(data)
    train_tf_idf = tf_idf_vec.transform(data)
    print(train_tf_idf)
    vocab = tf_idf_vec.get_feature_names()
    scipy.sparse.save_npz("..\\data\\tf_idf.npz", train_tf_idf)
    # np.savetxt("..\\data\\tf_idf_text.txt", te, fmt='%.5f')
    
    with open("..\\data\\vocab.txt", mode='w', encoding='UTF-8') as f:
        f.write('\n'.join(vocab))

compute_tf_idf("..\\data\\train_data.txt")



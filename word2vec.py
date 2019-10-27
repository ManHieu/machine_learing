import gensim
import os


def word2vec(data, model_path):
    model = '../data/vi.bin'

    word2vec_model = gensim.models.Word2Vec.load(model)
    wv = word2vec_model.wv
    out = []
    for item in data:
        vec = wv[item]
        print(vec)
        out.append(vec)

word2vec(['đời_sống'], '../data/vi.bin')

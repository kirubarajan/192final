import math
import re
import numpy as np
from nltk.corpus import stopwords
from gensim.models import Word2Vec


# Removes stopwords from string and tokenizes string
def tokenize(string):
    text = re.sub("[^a-zA-Z]", " ", string)
    tokens = text.lower().split()
    english_stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if not in english_stop_words]
    return tokens


# Splits text into vectorize-able sentences
def get_sentences(string):
    sentences = [tokenize(sentence) for sentence in string.split(".")]
    return sentences


# Generates and trains word2vec model
def get_model(data):
    sentences = get_sentences(data)
    model = Word2Vec(sentences, min_count=1, window=20)
    return model


# Generates and trains word2vec model
def average_vector(vectors):
    return sum(vectors) / len(vectors)


# Returns a unit vector by dividing by a normal vector
def unit_vector(vector):
    return vector / np.linalg.norm(vector)


# Returns cosine distance by clipping dot product
def distance(vector1, vector2):
    unit_vec1 = unit_vector(vector1)
    unit_vec2 = unit_vector(vector2)
    return 1 - np.arccos(np.clip(np.dot(unit_vec1, unit_vec2), -1.0, 1.0))


# Calculates similary using cosine distance
def similarity(string1, string2):
    with open('corpus.txt', 'r') as f:
        data = f.read().replace('\n', '')
        model = get_model(data)

        string1_token_emb = [model[t] for t in tokenize(string1) if t in model]
        string2_token_emb = [model[t] for t in tokenize(string2) if t in model]

        if len(string1_token_emb) == 0 or len(string2_token_emb) == 0:
            return 0

        string1_embedding = average_vector(string1_token_emb)
        string2_embedding = average_vector(string2_token_emb)

        return 1 - abs(distance(string1_emb, string2_emb))

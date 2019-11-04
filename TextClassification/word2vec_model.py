from gensim.models import Word2Vec
from preprocessor import TextPreProcessor
from data_loader import load_pickle_data, load_config_preprocess, data_splits, target_encoder
from utils import texts2sequences, padding_sequences, concatenate_columns
import pandas as pd
import sys
import os

# Load data and config file
config = load_config_preprocess('config.json')

text_processor = TextPreProcessor (

	    normalize=['hashtag','user','email', 'phone', 'url','date','time'], 
		decode = True,
		remove = ['stop_list','punctuation','number'],
		config_preprocess = config

	)

data = pd.read_csv("/home/abdou/Bureau/Maif/TextClassification/tweets_w2v.csv", encoding='utf-8',sep='\t', names=['id','text'])
data['text'] = text_processor.preprocessing_docs(data['text'])
sentences = data['text'].str.split().values.tolist()


# train model
model = Word2Vec(sentences, size=200, window=5, min_count=5)
# summarize the loaded model

# access vector for one word
#print(model['maif'])

# save model
model.save('model2.bin')

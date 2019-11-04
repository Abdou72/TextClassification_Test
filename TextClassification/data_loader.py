# -*- coding: utf-8 -*-
import pandas as pd
import json
from sklearn import preprocessing
from keras.utils.np_utils import to_categorical
import numpy as np
from gensim.models import Word2Vec

def load_pickle_data(data_path):
	"""
	Load a csv file

	Parameters:
		File path where the pickled object will be loaded.

	Return
		DataFrame
	"""

	return pd.read_pickle(data_path)



def load_config_preprocess(file):

	"""
	Load the json file that contains the regular expressions and 

	Parameters:
		File path where the regex will be loaded.

	Return
		dic
	"""
	with open(file, 'r', encoding='utf-8') as myfile:
		data=myfile.read()
		return json.loads(data)


def data_splits(X, y, train_size=0.85):

	"""
		Split the X into training and testing.

		Parameters:
			- X:  Input data (sequence of arrays)
			- y:  Target data (sequence of arrays)
			- train_size: float, should be between 0.0 and 1.0 and represent the proportion 
			of the dataset to include in the train split.

		Returns:
			- sequence of arrays: train_size % of the data that should be held over for testing
			- sequence of arrays: (1-train_size) % percentage of the data that should be held over for testing
	"""
	split_idx = int(len(X)*train_size)
	x_train, x_test = X[:split_idx], X[split_idx:]
	y_train, y_test = y[:split_idx], y[split_idx:]

	return 	x_train, x_test, y_train, y_test



def embeddings_matrix(word2vec_file, EMBEDDING_DIM, word_index, nb_words):
	"""
		Contain at index i the embedding vector for the word of  
		index i in our word index.
	
	parametres:
		word2vec_file: trained embedding file path
		EMBEDDING_DIM: vector dimension
		nb_words: size of the vocabulary in the text data.
	
	returns: 
		embedding matrix

	"""
	# Load model word2vec

	w2v_model = Word2Vec.load('model.bin')

	#words not found in embedding index will be value between -1 and 1
	oov=[]
	oov.append((np.random.rand(EMBEDDING_DIM) * 2.0) - 1.0)
	oov = oov / np.linalg.norm(oov)
	embedding_matrix = np.zeros((nb_words, EMBEDDING_DIM))

	for word, i in word_index.items():
		if word in w2v_model.wv.vocab:
			embedding_matrix[i] = w2v_model.wv[word]
		else:
			embedding_matrix[i] = oov
	return embedding_matrix



def  target_encoder(targets):
	"""
		Transform : non-numerical labels --> to numerical labels --> one hot encoding
		
		parameters:
			y: vector to be converted into a matrix

		returns:
			A binary matrix representation of the input.
	"""
	# Step1: non-numerical labels --> to numerical labels
	# Encode labels with value between 0 and n_classes-1

	encoder = preprocessing.LabelEncoder()
	encoder.fit(targets)
	num_class = len(list(encoder.classes_))
	y_numerical = encoder.transform(targets)
	
	# Step2: umerical labels --> one hot encoding
	# Converts a class vector (integers) to binary class matrix.
	y_train = to_categorical(np.asarray(y_numerical), len(set(y_numerical)) )

	return y_train, num_class 





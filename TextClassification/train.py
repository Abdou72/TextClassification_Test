from preprocessor import TextPreProcessor
from data_loader import load_pickle_data, load_config_preprocess, data_splits, \
target_encoder, embeddings_matrix
from utils import texts2sequences, padding_sequences, concatenate_columns
from models import BLSTM_model
from keras.layers import LSTM
import sys
from keras.callbacks import Callback, ModelCheckpoint
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt

print("\n\tData Preprocessing ...")

# Load data and config file
config = load_config_preprocess('config.json')
#  Parameters
data_path = config['files']['data']
w2v_path  = config['files']['word2vec']
embedding_dim  = config['model_nn']['embedding_dim']
epochs =  config['model_nn']['epochs']
size =  config['model_nn']['size']
cells_rnn =  config['model_nn']['cells_rnn']


data = load_pickle_data(data_path)
data= concatenate_columns(data)

# Text processing to filter the noise from the raw text:
#     - All words are lowercase. E-mails, URLs and user handles are normalized,
#     - Remove common, uninformative words that don't add meaning to the sentence,
#     - etc.

text_processor = TextPreProcessor (

	    normalize=['hashtag','user','email', 'phone', 'url','date','time'], 
		decode = True,
		remove = ['stop_list','punctuation','number'],
		config_preprocess = config

	)
data['text'] = text_processor.preprocessing_docs(data['text'])

# Prepares the sequence to be used as input for the neural network model.
X, word_index, nb_words = texts2sequences(data['text'])
pad_sequences, maxlen = padding_sequences(X)



# Label one hot encoder
y, num_classes = target_encoder(data['thematique'])

# Split data into Train, Test 
x_train, x_valid, y_train, y_valid= data_splits(pad_sequences,y)



# word2vec Matrix
embeddings_matrix = embeddings_matrix(w2v_path,embedding_dim,word_index,nb_words)


# Building Neuronal Network Model
print("\n\tBuilding Neuronal Network Model...")
model = BLSTM_model(embeddings_matrix, num_classes=num_classes, vocab_size=nb_words,
                                input_length=maxlen, layers=2, unit=LSTM, embedding_dim=200,
                                cells=cells_rnn, bidirectional=True, lr=0.001, loss_l2=0.000,
                                dropout_final=0.3, dropout_words=0.3, dropout_rnn=0.3)



# Save best model
filepath="Acc-{epoch:02d}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]

print("\n\tTrainning ...")
history = model.fit(x_train, y_train,
                       validation_data=(x_valid,y_valid),
                       epochs=epochs, batch_size=size, callbacks=[checkpoint])




# Plot learning curve 
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

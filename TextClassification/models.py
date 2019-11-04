from keras.engine import Input
from keras.engine import Model
from keras.layers import Dropout, Dense, Bidirectional, LSTM, GRU, \
    Embedding, Activation, Flatten, TimeDistributed
from keras.models import Sequential
from keras.optimizers import Adam
from attention_with_context import AttentionWithContext



def rnn_layer(unit=LSTM, cells=64, bidirectional=False, return_sequences=True):
    """
    Creating a LSTM or GRU or BLSTM or BGRU layer

    # parameters
        return_sequences: Boolean. Whether to return the last output in the output sequence, 
        or the full sequence.
        cells: positive integer, dimensionality of the output space (containing information about the entire sequence).
        unit: a RNN cell instance (GRU ou LSTM)

    """
    rnn = unit(cells, return_sequences=return_sequences)
    if bidirectional:
        return Bidirectional(rnn)
    else:
        return rnn





def BLSTM_model(embeddings, embedding_dim, num_classes, vocab_size, input_length, 
                unit=LSTM, cells=64, nb_layers=2, **kwargs):
    
    # parameters
    bidirectional = kwargs.get("bidirectional", False)
    lr = kwargs.get("lr", 0.001)
    dropout_words = kwargs.get("dropout_wordsords", 0.)
    dropout_final = kwargs.get("dropout_final", 0.)
    dropout_rnn = kwargs.get("dropout_rnn", 0.)

    # model
    model = Sequential()
    model.add(embeddings_layer(input_length=input_length, embedding_matrix=embeddings,
                               vocab_size=vocab_size, embedding_dim=embedding_dim, trainable=False))

    for i in range(nb_layers):
        rs = (nb_layers > 1 and i < nb_layers - 1)
        model.add(rnn_layer(unit, cells, bidirectional, return_sequences=rs))
        if dropout_rnn > 0:
            model.add(Dropout(dropout_rnn))

    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer=Adam(lr=lr),
                  metrics=['acc'])

    model.summary()
    return model


def BGRU_model(embeddings, embedding_dim, num_classes, vocab_size, input_length, 
                unit=GRU, cells=64, **kwargs):
    """
        Similaire au modèle BLSTM_model avec
            - une autre implémentation
            - BGRU au lieu de BLSTM

    """
    lr = kwargs.get("lr", 0.001)
    # parameters
    bidirectional = kwargs.get("bidirectional", False)
    trainable = kwargs.get("trainable", False)  

    text_input = Input(shape=[input_length], dtype='int32')

    model = embeddings_layer(vocab_size =vocab_size, input_length=input_length, embedding_matrix=embeddings,
                                embedding_dim=embedding_dim,   trainable=False)(text_input)

    model = rnn_layer (unit, cells, bidirectional, return_sequences=False)(model)
    model = Dense(150,  activation='relu', name='dense1')(model)
    model = Dropout(0.3)(model)
    preds = Dense(num_classes,  activation='softmax', name='dense2')(model)

    model = Model(inputs=[text_input], \
        outputs=preds)

    model.summary()

    model.compile(loss='categorical_crossentropy',
            optimizer=Adam(lr=lr),
            metrics=['acc'])

    return model


def BLSTM_attention_model(embeddings, embedding_dim, num_classes, vocab_size, input_length, 
                unit=LSTM, cells=64, **kwargs):


        """
                Similaire au modèle BLSTM_model avec une couche de mécanisme 
                d'attention avant la derière couche dense

        """
    lr = kwargs.get("lr", 0.001)
    # parameters
    bidirectional = kwargs.get("bidirectional", False)
    trainable = kwargs.get("trainable", False)  

    text_input = Input(shape=[input_length], dtype='int32')

    model = embeddings_layer(vocab_size =vocab_size, input_length=input_length, embedding_matrix=embeddings,
                                embedding_dim=embedding_dim,   trainable=False)(text_input)

    model = rnn_layer (unit, cells, bidirectional, return_sequences=True)(model)
    model = Dense(150,  activation='relu', name='dense1')(model)
    model_att = Dropout(0.5)(AttentionWithContext()(model))
    preds = Dense(num_classes,  activation='softmax', name='dense2')(model_att)

    model = Model(inputs=[text_input], \
        outputs=preds)

    model.summary()

    model.compile(loss='categorical_crossentropy',
            optimizer=Adam(lr=lr),
            metrics=['acc'])

    return model



def embeddings_layer( embedding_dim, input_length, vocab_size, embedding_matrix, trainable=False):

	"""
		- Embedding layer that can be used for neural networks on text data
		- Pre-trained word embeddings into an Embedding layer by looking up 
		  the integer index of the word in the embedding matrix to get the word vector
		- input_length: 
		parametres:
			- nb_words: This is the size of the vocabulary in the text data.
			- embedding_dim: size of the vector space in which words will be embedded
			  note that we set trainable = False so as to keep the embeddings fixed
			- embeddings matrix
			- input_length: length of input sequences
			- trainable fine-tune / freeze some parameters (trainable = False so as to keep the embeddings fixed) 
			- Input shape: 2D tensor with shape: (batch_size, sequence_length)
	returns
			- Output shape: 3D tensor with shape: (batch_size, sequence_length, output_dim) 
	"""
	emb_layer = Embedding(vocab_size,  # The size of the vocabulary expected from data
	                            embedding_dim,
	                            weights=[embedding_matrix],
	                            input_length=input_length,
	                            trainable=trainable, name='embedding_layer')

	return emb_layer
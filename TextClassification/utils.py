from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import re

def concatenate_columns(df):
	"""
		Concatenate two string types columns ('title' and 'content')
		    - all nan values are replaced space
		    - two columns are separated with space

		Parameters:
			pandas.DataFrame object

		returns:
			pandas.DataFrame object
	"""
	df['titre'] = df['titre'].str.replace('\n',' ', regex=True)
	df['contenu'] = df['contenu'].str.replace('\n',' ', regex=True)
	text = df['titre'].fillna('')+" "+df['contenu'].fillna('')
	df['text'] = text
	return df[['text','thematique']]


def iso2utf8(text):
        """
        convert ISO charcters to ASII to utf8

        Parameters
             text: str

        Returns
            text: str

        Example 
            >>> Input: TWEET FROM: ARussac #DIGITECH2016 Le digital va coÃ»ter 200 Mâ‚¬ Ã  la Maif sur la pÃ©riode 2015-2018 (SI, Internet, mobile,...) + 125 Mâ‚¬ pour le fonds Maif Avenir
            <<< Output: TWEET FROM: ARussac #DIGITECH2016 Le digital va coûter 200  millions euros  à  la Maif sur la période 2015-2018 (SI, Internet, mobile,...) + 125  millions euros  pour le fonds Maif Avenir
        """
        text = re.sub(r"Ã©","é",text)
        text = re.sub(r'Ã€','À',text)
        text = re.sub(r'Ã§','ç',text)
        text = re.sub(r'Ã¨','è',text)
        text = re.sub(r'â€™',"'",text)
        text = re.sub(r'Ã®','î',text)
        text = re.sub(r'Ã¯','ï',text)
        text = re.sub(r'â€œ|â€¦|â€“|â€”|â€|Â»',"",text) # 'â€œ'=“ ; 'â€¦'='...' ; â€“='_'
        text = re.sub(r'Ãª', 'ê',text)
        text = re.sub(r'ô', 'Ã´',text)
        text = re.sub(r'Ã§','ç', text)
        text = re.sub(r'ù','Ã¹',text)
        text = re.sub(r'Ã»','û',text)
        text = re.sub('Ã´','ô',text)
        text = re.sub(r'â‚¬',' euros ',text)
        text = re.sub(r"Ã","à",text)

        return text


def texts2sequences(texts):
    """
        Transform each text in texts in a sequence of integers.

        Arguments:
            texts: pd.DataFrame
               list of texts to turn to sequences.

        Returns:
            list of sequences (one per text input)

    """

    tokenizer = Tokenizer(filters=' ')
    tokenizer.fit_on_texts(texts)
    word_index = tokenizer.word_index
    nb_words = len(word_index)+1
    return (tokenizer.texts_to_sequences(texts), word_index, nb_words)  


def padding_sequences(sequences):

    """
        - Pads sequences to the same length (maximum length of all sequences (maxlen)) 
        - The padding value is 0.0
        
        Parameters:
          - sequences: List of lists, where each element is a sequence.
    
        Returns:
            Numpy array with shape (len(sequences), maxlen)
            int: maximum length of all sequences
    """
    maxlen = 0
    for elt in sequences:
        if len(elt) > maxlen:
            maxlen = len(elt)

    x = pad_sequences(sequences, maxlen=maxlen)

    return x, maxlen
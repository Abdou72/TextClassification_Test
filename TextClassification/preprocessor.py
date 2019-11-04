# Import modules
import re
from data_loader import load_config_preprocess
from utils import iso2utf8



class TextPreProcessor:

    def __init__(self, **kwargs):
        """
        Kwargs:
            omit (list): choose what tokens that you want to omit from the text.
                possible values: ['email', 'percent', 'money', 'phone', 'user',
                'url', 'date', 'hashtag']
            normalize (list): choose what tokens that you want to normalize from the text.
                possible values: ['stop_list','punctuation','number']
            decode (bool): choose to convert ISO charcters  to utf8

        """
        self.decode = kwargs.get("decode", True)
        self.normalize = kwargs.get("normalize", {})
        self.config_preprocess = kwargs.get("config_preprocess", {})
        self.remove =  kwargs.get("remove", ['stop_list','punctuation','number'])
        self.punctuation = '|'.join(self.config_preprocess['punctuation'])


    def standardization (self,text):
        """
            Removing all symbols and punctuations
            Remove apostrophes from text (" d' ", " s' ", etc. )
            Remove HTML tags (<b>, <br>, etc.)
            Token standardization adapted for Maif documents (exp:  '335 Mds' ->  '<price> millions')
            Removing stop words
            ...

            Parameters:
                text: str

            returns:
                text: str 
        """
        text = re.sub(r"<[^>]*>"," ",text) # "<br> maif</br>" --> maif
        text = re.sub(r"\$|\€|EUR|euros|dollars?|\\$"," <currency> ",text) 
        text = re.sub(r"\b(\d+(?:[\.,']\d+))?\s?([m|M]ds)", " millions ",text)
        text = re.sub(r"[@|#](Maif|MAIF|maif)"," maif ", text) # "@maif" --> "maif"
        text = re.sub(r"\w+[\'|\’]([\w]+)","\\1 ",text) # "d'assureur "--> "assurreur"
        text = re.sub(r"(\w+)[\.+]+(\s|\n|$)"," \\1 ",text)# "maif."  --> "maif" ; "maif..." --> "maif"; "(maif)" --> "maif"
        text = re.sub(r"%"," percentage ",text)
        if ('stop_list' in self.remove):
            text =  ' '.join([i for i in text.split() if (i.lower() not in self.config_preprocess['stopwords'])  and (len(i)>1)]) # and (i not in self.config_preprocess['punctuation']) |'.join

        return text


    def preprocessing_doc(self,text):
        """
        Text processing for one document
            Calling the function that convert ISO charcters  to utf8
            Calling the function that performs a adapted transformation  to maif   documents 
            Putting all letters to lowercase
            Removing the punctuations, numbers and multiple spaces

        Parameters:
            text: str

        returns:
            text: str 

        """
        text = iso2utf8(text)
        text = self.standardization(text)
        for item in self.normalize :
            if item == "hashtag":
                text = re.sub(self.config_preprocess['regex'][item]," <hashtag> \\1" ,text)
            text = re.sub(self.config_preprocess['regex'][item],' <'+item+'> ',text)
        if ('punctuation' in self.remove):
            text = re.sub(self.punctuation, " ", text)
        if ('number' in self.remove):
            text = re.sub(r" \d+"," ",text)
        text = re.sub(' +', ' ', text)
        return text.lower()



    def preprocessing_docs(self,df):
        """
            Text processing for many documents (use function preprocessing_doc)

            Parameters:
                pandas.DataFrame object

            returns:
                pandas.DataFrame object
        """
        df = df.apply(lambda x: self.preprocessing_doc(x))
        return df
        



""" Example1
text_processor = TextPreProcessor(
    normalize = ['email', 'phone', 'user',
                'url', 'date', 'hashtag'],
    remove = ['stop_list','punctuation','number']
)
====
doc ="Assurance-vie : Augmentation cotisation Assurance Auto non conforme Bonjour, J'ai une question concernant ma cotisation d'assurance automobile. Pour rien vous cacher je suis a la MAIF, et celle-ci a annoncé dans la presse augmenter ses tarifs auto pour 2017 de 1.5 è  2.5% selon les contrats. Pour ma part dans mon avis d'échéance 2017 si je compare le tarif de la cotisation HT... Produits et services"
print(text_processor.preprocessing_doc(doc))
====
text_process= text_processor.preprocessing_docs(data)
for i in range(len(text_process)):
    print(str(i)+" "+str(text_process[i]))
"""
# Topic Text classification

Le but de ce projet est de classifier à un document de la MAIF (post/tweet) à l'une des 9 classes.

Pour lancer le projet il suffit de lancer

         python train.py
Le répertoire TextClassification contient les scripts suivants:

  - *Twitter_scraping.py* : pour télécharger automatiquement des tweets à partir des mots clés
  - *preprocessor.py* : pour effectuer les prétraitements sur les tweets
  - *models.py* : pour définir l'architecture du réseau de neurones 
  - *utils.py* : contient l'ensemble des fonctions importante pour ce projet
  - *train.py* : pour l'ancer l'apprentissage du réseau de neurones 
  - *data_loader.py* : pour lire les données, le fichier de configuration, etc.
   
  - *config.json*: est le fichier de configuration


## Text Processing

 Text processing to filter the noise from the raw text:
     - All words are lowercase. E-mails, URLs and user handles are normalized,
     - Remove common, uninformative words that don't add meaning to the sentence,
     - etc.


	text_processor = TextPreProcessor (
	    normalize=['hashtag','user','email', 'phone', 'url','date','time'], 
		decode = True,
		remove = ['stop_list','punctuation','number'],
		config_preprocess = config

	)
	data['text'] = text_processor.preprocessing_docs(data['text'])

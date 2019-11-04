# Topic Text classification

Le but de ce projet est de classifier à un document de la MAIF (post/tweet) à l'une des 9 classes.

Pour lancer la classification, il suffit de lancer

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

 Pour la tâche de la classification, les tweets contiennent plusieurs sources de bruit. L'étape de prétraitement consiste à les   préparer pour un traitement automatique efficace.:
     - Convertir tous les mots en minuscule, supprimer les informations parasites telles
que les mots non porteurs de sens (e.g. le, de, ce, etc.)
     - Normaliser les emails, hashtag, les pseudos, ...
     - etc.


	text_processor = TextPreProcessor (
	    normalize=['hashtag','user','email', 'phone', 'url','date','time'], 
		decode = True,
		remove = ['stop_list','punctuation','number'],
		config_preprocess = config

	)
	data['text'] = text_processor.preprocessing_docs(data['text'])

## Word embeddings
Le word embedding est une représentation de mots dans un espace à n dimensions apprise à partir de réseaux de neurones. Chaque mot est représenté par un vecteur de nombres réels capturant la sémantique des mots.  Notre choix fut de construire notre propre représentation
vectorielle, à partir de tweets récoltés sur internet, pour disposer d'une représentation vectorielle plus
robuste et adaptée au problème que certains modèles trouvables sur le net. Nos sources proviennent plus d’
1 million de tweets de différentes catégories relatives aux données de la maif (@maif, @macif, ...)
	
	from twitterscraper import  query_tweets_from_user
	tweet = query_tweets_from_user('@maif',limit=50000)

Pour lancer le télechargement des données il faut lancer la commande 

		python Twitter_scraping.py
Les représentations vectorielles ont été obtenues en utilisant l'outil Gensim. Les words embeddings utilisés dans ce
travail sont de 200 dimensions.

## Apprentissage
Le script train.py permet de lancer l'apprentissage d'un réseau de neurone de type BLSTM. 

Les paramètres des pretraitements et de l'apprentissage sont définis dans le fichier de config *config.json*

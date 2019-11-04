# -*- coding: utf-8 -*-


from twitterscraper import query_tweets
from twitterscraper import  query_tweets_from_user
import re

words = ['carte verte assurance','pass cinéma','véhicule','maif','assurrance','maaf','prix','accident','actuaire','contrat', 'risque', 'partenaire', 'décès','taux', 'macif', 'matmut','vie', 'assuré', 'auto', 'cotisation','contrats','bénéficiaire','tarif','bonus','malus','carte','code sécurité', 'constat','amiable','axa','mma','société','gestion',
'budget','service','produit','innovation','gmf', 'direct assurance', 'lcl assurance', 'bnp assurance', 'permis', 'cycliste', 'piéton', 'maison', 'location', 'voiture', 'appel à candidature', 'inscription', 'gratuit', 'crédit', 'economie', 'corporate', 'entreprise', 'startup', 'millions euros', 'sinistre', 'millions dollar', 'million', 'milliard', 
'association', 'annoncer', 'banque', 'internet', 'appli', 'projet', 'heureux', 'tous risque', 'sécurité routière', 'tiers de confiance', 'engagement', 'concurrence', 'travail', 'client', 'innovante', 'métier', 'facture', 'France', 'lauréat', 'smartphone', 'volant', 'appartement', 'vol', 'fondation', 'audace', 'matmut','esprit critique', 'niort',
'assureur', 'management', 'mutuelle', 'mutualiste', 'protection', 'sociétaire', 'plateforme', 'collaborative', 'famille', 'victime', 'biron', 'action', 'actionnaire', 'prévention', 'témoignages', 'macsf', 'militant', 'offre', 'expérience sociale', 'expérience client', 'avenir', 'garantie', 'assurance vie', 'prévoyance', 'attentat', 'mgen', 'prefon', 
'camif', 'talent', 'remboursement', 'dirigeant', 'engagé', 'prestation', 'dommages', 'partenariat', 'chèque', 'chèques cadeaux', 'confiance', 'Percuter', 'devis', 'séisme', 'magnitude', 'soutien','départ', 'chauffeur', 'départ de ses client', 'anticipé', 'utilisateurs', 'jeune','recrutement', 'salons', 'plafond', 'partenaire officiel', 'numérique', 'contact', 
'vélo', 'santé', 'assurance maladie', 'inscrivez-vous', 'bourse de paris', 'crédit agricole', 'bnp-paribas', 'crédit mutuel', 'rendez-vous', 'rdv', 'ouragan irma', 'irma', 'volontaire', 'responsabilité civile', 'protection civile', 'exposition gratuite', 'innondation', 'expertise', 'Monptivoisinage', 'indemniser', 'défis', 'alerte jaune', 'alerte rouge', 
'alerte orange', 'résultat', 'contactez notre', 'contactez', 'rupture digitale', 'covoiturage', 'covoiturage-libre', 'vignette', 'conducteur', 'voiture sans assurance', 'baisse de', 'economique', 'collosale', 'voiture autonome', 'abonnement', 'appel nationale', 'abonnez-vous', 'rejoignez-nous', 'financement', 'financement participatif', 'acheter', 'habitation', 
'propriétaire', 'prêt', 'investissement', 'social club', 'application mobile', 'site service', 'service client', 'conseiller', 'sponsor', 'agence', 'trésorerie', 'capital', 'inco', 'annonce', 'acteurs', 'épargne', 'expert sinistres', 'prevention_maif', 'assurance auto', 'Pascal Demurger', 'fonds', 'mutualisme', 'banque Edel', 'maif social club', 'Fintech','qualité du service',
'#sgam','#Matmut','#MMA','#Apgis','#assurance','#Macif','#bénévoles','#JeunesOfficiels','#héritage','#MAIFPartenaire','#chaqueactecompte','#Amelie','#association','#solidaire','#santé','@FondationMacif','@MAAFAssurances','@MAAFvousrepond','@mabanque_bnpp','@Hellobank_fr','@AXAFrance',
'#assurancescolaire','#Prevention','#MacifAvantages','#trimaranMACIF','#HelloBank','#banque']

users = ['@MAIF','@GroupeMacif','@Matmut','@MMAssurances','@Paris2024','@Paris','@FondationMAIF','@LCL', '@VigiMeteoFrance','@ProtecCivilefr','@pascaldemurger','@dominique_mahe','@MSC_Officiel','@Ollitom72','@TwitterFrance','@DirectAssurance','@FFA_assurance','@CreditMutuel','@argusassurance','@ameli_actu',
'@Cnlibourne','@ville_libourne','@UnssMontpel' , '@AriasStephane', '@unss', '@FFRXIII', '@UnssMontpel', '@AriasStephane', '@nicolasvillemot', '@AvironMelun', '@NaviguerEnAquit', '@ville_libourne',  
'@360Learning', '@generalifrance', '@MsieurLeProf', '@MAAFAssurances', '@monptivoisinage', '@babgi', '@SolenneDim', '@derosnayjoel', '@Netexplo', '@BlockchainFra', '@GuestToGuest', '@FUTUREMAGfr', '@ZenparkFr', '@Ollitom72', '@Toutsur', '@OuiShare_Fr', '@SalsaHayek', '@pterrasse', 
'@EspritRoue', '@ninebotFR','@VixWorld','@axellelemaire', '@AVidalies' ,'@hishuhome', '@MedorDu27', '@donjuan_dvro', '@Moovway', '@GMF_assurances', '@CNP_Assurances', '@MercedesBenz', '@reputationsquad', '@MaPiDuval', '@Preventionrout', '@Sdis02', '@axellelemaire', '@pascaldemurger', '@EqConfiance', '@dominique_mahe', 
'@lebaratelier', '@filleduweb', '@yoannmonnat', '@DdDenier'

]

users2=['@hmutuelle','@mutuelleMNT','@Thelem_Officiel','@LeLynxfr','@MalakoffMH','@La_LMDE',
       '@Groupe_MACSF','@HSBC_FR','@GroupeSMA','@TwitterFrance','@AIG_Unesco','@SwissLife_Fr','@AvivaFrance','@Smeba_Officiel',
        '@natixis','@bfmbusiness','@integralebourse','@NatixisPayments','@money2020','@MonEpargneEtMoi',
        '@teixeira_nun','@FinforTomorrow','@FrenchFounders','@SwissLife_Fr','@FranceAlzheimer',
        '@Fonda_SwissLife','@allianzfrance','@Mutuelledelest','@Gan_Assurances','@AIGinsurance',
        '@AIGemea','@LaManifPourTous','@Place_Beauvau','@FFAthletisme','@JMarc_WILLMANN',
        'NEOVIA_Retraite','@Retraite','@HSBC ','@ESgloballaw','@FinancialNews','@MACSFetvous',
        '@VoileMACSF','@Prevention_Med','@Prevention_Med','@meteofrance','@VigiMeteoFrance',
        '@Meteovilles','@Boursorama','@BPCErecrutement','@GroupeBPCE','@CE_LoireCentre', '@AmandineBauer', '@cmarkea'
       ]  

words2=['#vivinter',  '#captiveinsurance', '#captiveinsurancesolutions', '#RentaCaptive', '#Amelie', '#VigilanceOrange', '#vents',
 '#maifsocialclub', '#AssuranceConstruction', '#TempêteAmélie', '#orage','#protectioncivile','#urgence','#secours' ]

def download_tweets_keywords(words):
	'''
	Scraping Twitter with package TweetScraper. 
	Collecting a large number of historical tweets.
	Data collected are used to bluid our word2vec.
		- URL: https://github.com/taspinar/twitterscraper
		- To install twitterscraper:
			       !pip install twitterscraper		
	
	parameters:
		list of words: search for tweets from a specific words (queries)
	return: 
		files (file for each word)
	'''

	i=0    
	for word in words2:
		file_name= 'tweets2'+'/'+word+'.txt'
		with open(file_name, 'w') as f:
			for tweet in query_tweets(word,1000,lang='fr'):
				tweet=tweet.text.replace('\n', ' ')
				f.write(str(i)+'\t'+tweet+'\n')
				i=i+1
			f.close()

def download_tweets_user(users):

	i=0
	for user in users2:
		file_name= 'tweets2'+'/'+user+'.txt'
		with open(file_name, 'w') as f:
			for tweet in query_tweets_from_user(user,limit=50000):
				tweet=tweet.text.replace('\n', ' ')
				f.write(str(i)+'\t'+tweet+'\n')
				i=i+1
			f.close()

download_tweets_user(users)
download_tweets_keywords(words)

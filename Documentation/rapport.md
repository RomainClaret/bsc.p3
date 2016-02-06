# Projet TA: Gestionnaire d’appels d’urgence
- No Projet: 16INF-TA221
- Auteur: Claret Romain
- Professeur: Ghorbel Hatem
- Language: Python
- Abstract: Développement d'une application pour l'analyse de priorité et la classification pour des appels d'urgences de police secours.


# Résumé
## Français

Actuellement, tous les appels d'urgence passent par une centrale téléphonique dans l'ordre d’appel. Les appels sont donc pris un par un selon les ressources (standardistes) disponibles. Malheureusement, les urgences ne sont pas toujours de priorités équivalentes et les ressources perdent souvent du temps sur des cas considérés moins importants, mettant ainsi en attente des cas considérés comme plus importants. L’idée est donc de mettre en place une application qui permettra de répondre de façon simultanée à tous les appels reçus au central pour analyser rapidement le contenu et le contexte de la conversation, et ainsi rediriger ces appels aux ressources compétentes disponibles.

## English

Currently, all emergency calls go through a call center in the bid order. Calls are then taken one by one depending on the resources (operators) available. Unfortunately, emergencies are not always of equivalent priorities and the resources often lose time on cases considered less important, putting on hold cases considered more important. The idea is to develop an application that will respond simultaneously all calls received at the central to quickly analyze the content and context of the conversation, and then redirect those calls to available resources with targeted expertise.

# Table des matières
- Introduction..................................................................................................7
- Objectifs.......................................................................................................7
- Cahier des charges.........................................................................................7
- Étude de l'existant........................................................................................9
  - Produits similaires................................................................................9
  - Enregistrements d'appels d'urgence.....................................................10
  - Reconnaissance vocale (Speech-to-Text)..............................................10
  - Traitement du son...............................................................................12
  - Analyseur de textes.............................................................................12
- Analyse.......................................................................................................13
  - Partie audio et reconnaissance vocale...................................................13
  - Partie traitement du texte...................................................................15
- Implémentation...........................................................................................17
	- Partie exploration................................................................................17
	- Partie reconnaissance vocale................................................................18
	- Partie traitement du texte...................................................................18
	- Fusion des deux parties........................................................................19
- Évaluation...................................................................................................21
	- Tests....................................................................................................22
	- Résultat final.......................................................................................23
- Conclusion..................................................................................................25
- Procédure de déploiement..........................................................................29
- Utilisation..................................................................................................31
- Bibliographie..............................................................................................33
	- Différents tutoriels.............................................................................33
	- Outils.................................................................................................33
	- Références..........................................................................................34

# Préface
## Introduction
Nous avons créé une application d'analyse à la volée pour des appels téléphoniques dans un cadre d'urgence. La rapidité et la précision d'analyse sont très importantes dans ce contexte. L'interlocuteur doit pouvoir expliquer son cas dans n'importe quel contexte émotionnel et être soit mis en attente, soit redirigé vers le service de prise en charge concerné, dans un court délai. Enfin, le service doit récolter et transmettre des informations sur le statut de la conversion déjà effectuée (lieu, incident, etc..).
Nous utiliserons une reconnaissance vocale, une librairie d'analyse lexicale, et l'algorithme K-Means pour l'apprentissage et classification des appels reçus.

## Objectifs
Ce projet a pour objectif de développer une application capable d’analyser des appels téléphoniques audio d'urgence de police secours et de les classifier en différentes classes d'urgences. Nous devons donc explorer les possibilités existantes pour faire de la reconnaissance vocale dite speech-to-text et les possibilités existantes pour faire du traitement de corpus, dans le but d'en extraire le contexte. Une fois les points précédents accomplis, nous devrons mettre en oeuvre une manière de classifier les différents corpus entre eux  et finalement être capable avec un corpus non entraîné, de le grouper avec une classe créée lors de l'apprentissage.


## Cahier des charges
###Les spécifications du projet ont été de:

- Faire des démarches pour obtenir des enregistrements audio et/ou des transcriptions d’appels d’urgences en situations réelles.
- Faire des démarches pour obtenir des statistiques sur les types d’appels reçus à police secours et leurs classifications en interne.
- Dans le cas où les situations réelles ne sont pas disponibles, créer des mises en scène d’appels d’urgence pour simuler les appels selon les statistiques internes obtenues.
- Faire l'exploration d'outils pour transcrire automatiquement les enregistrements audio en texte (speech-to-text).
- Faire l'exploration d'outils pour analyser et segmenter les corpus de textes.
- Extraire le contexte des corpus d'appels d'urgences et détecter leur pertinence.
- Classifier les appels reçus selon leur contexte.
- Classifier les appels reçus selon leur niveau d’importance.
-	Tenter de regrouper de multiples appels dans un intervalle de temps.
-	Rediriger les appels sur la bonne ressource avec un rapport détaillé.

###Les contraintes ont été de:

- Utiliser la langue de programmation Python
- Utiliser la libraire NLTK
- Utiliser un outil de reconnaissance vocale (speech-to-text)


# Étude de l'existant
Pour initier le projet, il a été important d'effectuer un travail de recherche pour cibler les besoins de ressources et les technologies existantes qui seraient potentiellement utilisables pour ce projet. Nous allons donc dans ce chapitre effectuer une recherche pour trouver des produits similaires, partir à la recherche d'enregistrement audio d'appels d'urgences, et trouver comment effectuer sur eux du traitement à la volée pour en extrait les corpus.  Finalement, il s'agira d'analyser les corpus eux-mêmes pour en extraire le contexte.

## Produits similaires
Il existe des projets ou idées de projets similaires dans le domaine de l'analyse des informations d'urgence et émotionnelles.

- La société suisse YMC, faisant parfois des reviews technologiques, propose un concept pour analyser les états d'urgence à l'aide de Twitter et en informer les services d'urgences. [1]

- À New York City (USA), le département administratif a lancé un système de répondeur automatique pour répondre à des questions basiques de tous les jours. [2]

- Le service d'urgence téléphonique de la police américaine utilise une plateforme dans le cloud pour analyser différentes informations au sujet des appels téléphoniques. [3]

- Une plateforme intéressante qui analyse les tendances émotionnelles dans le monde en direct. Elle utilise NLTK pour analyser les principalement les informations des médias. [4]

## Enregistrements d'appels d'urgence
Le but du projet étant de comprendre la situation lors d'un appel téléphonique, il faut pouvoir entraîner notre application à comprendre ce qui est dit au téléphone.

- La première étape a été d'essayer d'obtenir des enregistrements pour des appels d'urgence. *M. Hobi*, Chef du service de la Sécurité urbaine à Neuchâtel, a indiqué que ces enregistrements ne peuvent pas être donnés à des tiers, dû à des droits de confidentialité. Cependant, un contact a été pris avec *M. Viuille*, Chef CET de la police neuchâteloise, résultant à **l'obtention de statistiques** avec le **classement des appels d'urgence** reçus sur le canton de Neuchâtel et des compliments sur l'idée du projet. *M. Viuille* a permis de prendre contact avec *Mme Fasel Lauzon* de l'université de Neuchâtel, qui a effectué un travail d'enregistrement et d'anonymisation (avec des bips) sur une période de quelques mois d'appels d'urgence reçus à la police neuchâteloise. Suite au contact avec *Mme Fasel Lauzon*, il n'a malheureusement pas été possible de trouver un accord pour partager les données audios appartenant à la police neuchâteloise qu'elle a récupérées et anonymisées.

- Deuxièmement, il a été trouvé sur internet un site web recensant des **enregistrements audio d'appels d'urgence américains** (911), Documenting Reality http://www.documentingreality.com/forum/f218/. Il a été demandé explicitement à *M. Viuille*, Chef CET de la police neuchâteloise, ce qu'il en était de la légalité d'utiliser des enregistrements audio considérés confidentiels en Suisse. Celui-ci a répondu que nous avions le droit d'utiliser ce qu'on trouve sur internet, car ces enregistrements doivent être publics; sinon ils ne seraient pas disponibles sur internet. Suite à des tests à l'aide de reconnaissance vocale, il s'est avéré que ces enregistrements ne sont malheureusement pas facilement utilisables.

- Finalement, grâce à la discussion avec *M. Hobi*, Chef du service de la Sécurité urbaine à Neuchâtel, il a été possible de **reproduire 4 appels audios** à partir des exemples donnés par celui-ci.

## Reconnaissance vocale (Speech-to-Text)
Lors d'un appel téléphonique, les gens parlent, nous avons donc besoin que la machine puisse comprendre ce que l'interlocuteur dit, et ainsi pouvoir analyser la conversation. L'analyse de la conversation se fait sous format texte. C'est pourquoi la mise en place d'un convertisseur de voix vers du texte est indispensable.

- **Nuance Dragon** est un logiciel propriétaire très réputé dans le domaine de la reconnaissance vocale. Il utilise un processus d'apprentissage de la voix du propriétaire pour reconnaître de façon précise les mots. Il est principalement utilisé pour le traitement de texte vocal. C'est-à-dire que l'interlocuteur parle et que le texte est rédigé par la machine. Cependant, le problème principal est qu'il n'est capable de comprendre qu'une seule personne correctement, ce qui est problématique dans notre cas, où il est impossible de demander à quelqu'un dans la détresse de d'abord entraîner la machine avec sa voix. [5][6]

- **SpeechRecognition 3.1.0** est une librairie python qui facilite l'intégration des 4 principaux fournisseurs d'API de reconnaissance vocale dans le cloud (*Google Speech Recognition*, *Wit.ai*, *IBM Speech to Text*, et *AT&T Speech to Text*). Cependant le résultat de ces trois plateformes reste très décevant, il y a encore beaucoup de travail à faire dans le domaine de la reconnaissance vocale au niveau du cloud. Après de nombreux tests, il a été trouvé que Google fournit la meilleure reconnaissance vocale, mais dans un environnement silencieux, où les interlocuteurs parlent calmement et clairement. Autant dire que dans un cas pratique, il est impossible pour la reconnaissance de fonctionner correctement. Un exemple flagrant est l'auto sous-titrage sur YouTube, qui utilise l'API de Google. [7][8][9]

- **MU Sphinx** est une des solutions software pour la reconnaissance vocale. Il est très performant, cependant la configuration et la mise en place de ce système sont incroyablement complexes. Il faut de plus faire l'apprentissage des sons et des mots. Une fois l'outil pris en main, il prend facilement beaucoup de temps pour initialiser son utilisation. De plus, il faut un environnement silencieux pour un fonctionnement optimal. [10]

- **Htk** est une solution très performante pour la reconnaissance vocale. Cependant, je n'ai pas approfondi son fonctionnement plus en détail, car il n'est pas supporté par python nativement. [11]

- **Tropo** est une solution tout-en-un pour l'analyse d'appels audio proposée par Cisco (Automatisation des communications, connexions du code à la voix et à des messages. Dans le cloud, avec une communication en temps réel avec l'application du développeur...). Malgré l'offre très alléchante, les communications téléphoniques depuis la Suisse ne sont pas supportées gratuitement par l'offre gratuite développeur. De plus, je n'ai pas eu un bon à priori sur la documentation développeur. Ne pas avoir pu tester cette solution m’a laissé sur ma faim. [12]

- **VoxForge** est une solution open source et communautaire, qui propose des modèles acoustiques en différentes langues pour des outils comme Sphinx. Chacun de ces modèles a été entrainé par de multiples enregistrements audio. Il n'y a pas encore de modèle pour le français en ce moment. [13]

## Traitement du son
Dans le domaine de l'analyse des appels audio, il y a certes la reconnaissance vocale qui est primordiale, mais également des éléments de la structure de l'appel qui sont importants. Par exemple les pauses entre les mots ou les phrases, le niveau d'aigus dans la voix, etc. Ces informations permettraient de récupérer un niveau d'émotion dans l'appel.

- **SoX - Sound eXchange** est un utilitaire qui permet justement ce genre d'analyses. Il permet aussi le découpage des fichiers audios, ainsi que d'autres fonctionnalités intéressantes pour le traitement sonore. [14]

## Analyseur de textes
Une fois résolue la question de l'extraction des émotions et de la mise sous format texte de ce que dit notre interlocuteur, la machine doit maintenant pouvoir comprendre ce qui est dit. Elle analyse le texte pour extraire les informations et les classifier.

- **NLTK** est un des outils les plus performants, il est utilisé pour faire de l'analyse de corpus. Il permet de catégoriser et trouver les similitudes entre les mots facilement. [15]

- **TextBlob** est un outil très performant dans la détection des émotions. [16]
- **TreeTagger** est un outil utilisé par NLTK ou TextBlob pour découper les phrases en éléments (déterminant, verbe, nom, adjectif, etc.). [17]

# Analyse
Le projet peut être découpé en deux parties. La partie traitant de l'audio, et la partie traitant des corpus. En effet, la complexité a été ici de fusionner deux mondes, le monde du traitement du signal, et le monde de l'analyse de donnée pour en obtenir une application innovante.

## Partie audio (enregistrements audios) et reconnaissance vocale

La difficulté principale a été de récupérer des données audio cohérentes pour des appels d'urgence. Les portes se sont fermées les unes après les autres lors du processus de récupération de données.

- Beaucoup d'efforts et de volonté ont été déployés pour obtenir des données originales et légales. Malheureusement, le manque de bonne volonté externe, ainsi qu'une demande de modification du cahier des charges, ont eu raison de la possibilité d'avoir des données dites originales.

- Des recherches ont été faites pour trouver des appels d'urgence en français. Elles ont mené à la conclusion que le projet devrait utiliser comme langue l'anglais et non le français, dû à la complexité de ce dernier et à la reconnaissance vocale encore non performante pour le français.

- Des appels d'urgence 911 (USA) ont été essayés, mais la reconnaissance vocale a été catastrophique, principalement à cause du bruit de fond.

- Des efforts ont été faits pour créer des simulations d'appels d'urgence audio, mais ils se sont rapidement montrés vains, à cause de la piètre qualité de reconnaissance vocale en français. Il a été difficile de trouver un camarade pour enregistrer un appel en français, et trouver un camarade pour enregistrer un appel cohérent en anglais a touché à l'impossible.

- Le transcript des conversations en français a été effectué et a donné un résultat, cependant le texte était en français. Il a fallu faire ensuite une traduction pour obtenir des résultats avec l'analyseur de texte.

- L'installation, la configuration et la compréhension de nouveaux outils comme **Sphinx**, **Htk**, ou **Nuance Dragon** a pris un temps considérable, pour un résultat quasi nul. Heureusement, des APIs dans le cloud existaient au moment des recherches, et ont permis de donner un espoir dans la reconnaissance vocale.

- L'API de Google fonctionne suffisamment bien pour des phrases complètes, malgré les conditions qui demandent que la phrase soit enregistrée quasiment en qualité studio et que l'enregistrement audio ne dépasse pas les 15 secondes.

- Maintenant qu'une reconnaissance vocale potable a été trouvée, et malgré des contraintes non réalistes, il faut malgré tout trouver une solution pour obtenir un corpus compréhensible. Dans un cas réel, notre application doit pouvoir comprendre continuellement ce que l'interlocuteur dit pour pouvoir catégoriser l'appel le plus rapidement possible et le rediriger vers l'interlocuteur humain du bon service concernant le sujet. J'ai donc utilisé **SoX** pour découper la conversation à chaque pause dans la phrase (une respiration, ou un moment d'hésitation par exemple). On obtient donc une quantité assez importante de fichiers audios. Les fichiers sont transférés directement à Google au fur et à mesure qu'ils sont découpés. Malgré le temps de réponse laissant parfois à désirer, nous obtenons des surprises désagréables.

- Un problème majeur s'est présenté lors de l'utilisation de l'envoi de message audio coupé à des silences. L'API de Google ne fonctionne tout simplement pas lorsque ce sont des mots ou des bouts de phrases qui lui sont transmis, peu importe la condition d'enregistrement. Dans un cas réel, il faudrait donc utiliser une technique pour détecter la fin de phrase avec du traitement audio et ensuite envoyer la phrase à Google pour recouper son contenu sous format texte... Ce qui n'est malheureusement pas envisageable. Ou bien, envoyer des packs de son, avec l'espoir qu'il y ait des phrases entières dedans et de ne pas perdre les mots clés importants dans la phrase qui sera coupée.

- La conclusion a été que les APIs dans le cloud ne sont, actuellement, pas assez performantes pour faire du traitement textuel avancé comme nous en avons besoin pour ce projet. Les risques de perdre des mots clés sont très élevés, et obtenir des textes avec un sens assez approximatif n'est pas l'objectif.
- Finalement, malgré l'énergie dépensée et l'espoir de trouver la solution miracle, les résultats pour la reconnaissance vocale sont très décevants. Je garde espoir qu'un jour la technologie sera suffisamment avancée pour avoir une vraie reconnaissance vocale qui permettrait de mener convenablement ce projet à bien.


## Partie traitement du texte
Une fois en possession d'un corpus, la machine a besoin d'en extraire le sens pour le comprendre. Grâce aux statistiques obtenues de *M. Viuille*, Chef CET de la police neuchâteloise, il a été possible de catégoriser les appels d'urgence en 17 classes. (Problèmes routiers: {accidents, pannes, stationnement}, disputes, voies de fait, tapage, bruit, disparitions, fugues, levées de corps, tentatives de suicide, vol en tout genre, cambriolages, vandalisme, dommages à la propriété, animaux perdus, écrasés).

- L'aventure a commencé avec la prise en main de NLTK. Cette librairie est performante, mais ne gère pas la langue française. Elle a donc été abandonnée au profit de TextBlob, qui lui supporte la langue française.
- TextBlob a été très simple d'utilisation, sa documentation est assez prometteuse et contient de nombreux exemples. Dans l'absolu, le temps pour sa prise en main a été assez court, mais m'a semblé comme un éternité couplé au problème, en parallèle, de la reconnaissance vocale.
- TextBlob contient des méthodes de classification, d'apprentissage et d'autoévaluation assez avancées, il a été donc très intéressant de travailler avec cette librairie. Cela m'a permis de réaliser que cet outil permettrait une compréhension de corpus très avancée avec le temps nécessaire, et serait idéal pour l'avenir du projet.
- Après l'abandon de l'utilisation de la reconnaissance vocale à la volée, il fallait malgré tout trouver une solution pour quand même fournir le classement d'un corpus dans une des 17 classes d'appels de police secours. Ma solution pour perdre le moins de temps possible a été de prendre les textes bruts de Wikipedia pour chacune de ces classes, et d'entraîner mon algorithme de classification sur ces textes. À partir de ce point, le travail d'analyse de corpus sera en exclusivement en anglais.

- La première étape d'analyse a été de:

  - Récupérer touts les mots (séparés par un espace) du texte.
  - Extraire les caractères et combinaisons de caractères parasites tels que (* , . I in the).
  - Rechercher la base de données de mots wordnet pour utiliser un syn_set unique pour tous les synonymes.
  - Calculer la fréquence normalisée d'apparition de chacun des mots basés sur le nombre total de mots dans le texte.

- La deuxième étape a été de répéter la première étape pour tous les textes et créer un espace vectoriel multidirectionnel avec tous les mots utilisés dans les textes de façon ordonnée et populée avec les vecteurs des fréquences des textes. Lorsqu'un mot n'est pas présent dans le texte, il sera naturellement mis à zéro.

- La troisième est le regroupement, à l'aide de l'algorthime K-Means, des vecteurs en clusters en utilisant l'angle du cosinus pour distance.
- Finalement, nous avons à présent le choix:
  - Soit de continuer à entraîner nos clusters avec de nouveaux textes.
  - Soit de décider que l'apprentissage est terminé et de commencer à utiliser les clusters pour détecter la catégorie d'un corpus. Dans ce cas, il faut déterminer le sens de chacun des clusters. Pour trouver le sens, il faut récupérer le top 5 des fréquences de mots les plus utilisés de chacun des textes d'apprentissage et appliquer le nom du texte qui en porte le sens (accident, injury, road, etc.) aux clusters avec les mots clés dominants.

# Implémentation

Au début du projet, j'étais parti du principe que l'application résultante de ce projet saurait un prototype. C'est pourquoi ma façon de développer s'est orientée dans ce sens. J'ai principalement travaillé avec des fonctions et non des classes, pour des raisons de flexibilités. En effet, j'ai effectué beaucoup de tests avec des librairies différentes, créer des classes et les modifier m'aurait à mon sens fait perdre plus temps étant donné que je ne savais pas exactement où j'allais. De plus, Python, n'est pas une langue dite de prototypage pour rien; elle m'a permis de travailler avec le recul des classes sans me l'imposer.

Ma stratégie a été de couper le travail en quatre:

- explorer les différentes librairies (reconnaissance vocale + traitement du texte)
- la partie reconnaissance vocale
- la partie de traitement du texte
- la fusion des deux parties

## Partie exploration
J'ai commencé par essayer de prendre en main NLTK [15]. Les débuts ont été assez difficiles, car je ne comprenais pas le fonctionnement derrière. Les notions de tokenization [23], lemmatisation [24], wordnet [21], synsets [20], etc. n'avaient vraiment que très peu de sens pour moi. Après un peu d'acharnement, je me suis rendu compte que NLTK ne supportait le français qu'avec des manipulations très compliquées [22].

J'ai alors trouvé TextBlob [16] qui supporte le français, et qui est extrêmement performant; c'est le concurrent de NLTK. J'ai alors passé du temps à comprendre son fonctionnement et à effectuer des tests en français. Le concept de blob est assez simple à prendre en main.

À partir là, j'ai commencé à faire des recherches plus avancées sur la reconnaissance vocale. J'ai pu essayer à l'aide du package python SpeechRecognition [6] tester 4 différentes API de reconnaissance vocale en ligne (cloud computing). Les résultats ont été en faveur de Google.

Une bataille a été livrée avec Sphinx [10] et HTK [11] pour leur installation. J'ai abandonné HTK car je n'ai tout simplement pas compris comment le faire marcher malgré la documentation et des tutoriels. Et Sphinx ne m'a pas beaucoup inspiré lorsque j'ai dû commencer à lui enseigner des syllabes. Au niveau rapidité, l'API de Google était largement plus intéressante.

## Partie reconnaissance vocale
Voilà le morceau qui a pris le plus de temps pour un résultat bien inférieur à celui espéré. Il faut également dire que je n'ai pas eu de matière première (enregistrements audios) pour travailler cette partie comme il faut. Après avoir dépensé du temps à tweaker l'API, à faire de tests avec de faux enregistrements en français, à comprendre que Google n'accepte pas de fichier audio de plus de 15 secondes, j'ai réalisé que je n'obtiendrais finalement pas d'enregistrement audio en français. Il a fallu trouver une solution rapidement. Je suis parti d'enregistrements en anglais, principalement d'affreuse qualité pour Google [25]. Il n'a pas été difficile de modifier les scripts pour changer de langue, mais il a été difficile de mettre un terme à l'espoir que peut-être des enregistrements en français tomberaient du ciel.

On a maintenant des enregistrements audio, en anglais, et de mauvaise qualité. Il faut avancer avec ces derniers malgré tout. J'avais un souci avec la limitation de 15 secondes de google pour la longueur des fichiers audios. Jusqu'à présent je faisais la découpe dans Audacity. J'en ai eu assez, et j'ai automatisé le processus avec SoX [14]. J'ai également profité d'utiliser sa puissance pour faire des coupures aux silences au lieu d'un temps fixe, ce qui a l'avantage ne ne pas avoir de coupe au milieu d'un mot.

Nous avons donc des fonctions qui permettent de découper des fichiers audios aux silences, et de les transcrire avec la reconnaissance vocale de Google. Il est temps d'essayer d'incorporer la transcription de Speech-to-Text à TextBlob.

## Partie traitement du texte

Je me suis vite rendu compte que les transcriptions des enregistrements audios coupés à 15 secondes et ceux coupés à la respiration ne gardaient pas des mots clés, et pire encore ne donnaient parfois plus le même sens. Bien qu'à ce moment là, cela semblait être une véritable catastrophe, je me suis rendu compte avec le recul qu'avec un peu de tweaking avec les coupures des fichiers audios (augmenter le nombre de respirations par fichier), je pouvais arriver à une transcription plus ou moins correcte.

Le temps de mettre en place une matrice de vecteurs multidimensionnels pour contenir l'espace des connaissances est ensuite venu, avec la démarche suivante: Appliquer l'algorithme du K-Means sur cet espace pour récupérer les clusters; Donner un nom au cluster; Finalement, permettre de regrouper n'importe quel vecteur de la même dimension que l'espace avec la distance du cosinus. Sur le moment, je n'ai rien compris de ce qui m'était demandé.
J'ai alors commencé par récupérer la liste des fréquences des mots dans un corpus. Et de normaliser cette liste, c'est-à-dire faire la frequence_du_mot / total_des_mots.

Ensuite, j'ai construit une matrice qui contenait dans sa première colonne la liste de tous les mots du corpus en utilisant ma liste de fréquences. Et j'ai rempli les autres colonnes de la matrice avec les fréquences des corpus que j'avais à disposition (des articles de Wikipédia en totalité). J'avais bien entendu pris le soin d'ordonner mon espace de mots et de compléter les vecteurs de fréquences avec des 0 les mots n'existant pas dans le vecteur de fréquence.

J'ai donc maintenant un espace vectoriel multidimensionnel NxM

  - N: corpus + liste des mots
  - M: nombre de mots de la liste de mots

Ce principe de K-Means à n dimensions m'a posé beaucoup de problèmes conceptuels. Malgré de nombreuses documentations parcourues, je n'arrivais pas à conceptualiser un barycentre (centroid) pour un espace à plus que 3 dimensions. Il a fallu un éclair de génie à un moment improbable pour comprendre l'univers à n dimensions. À partir de là, rechercher le web avec les bons mots clés est beaucoup plus simple, et les APIs de SciPy pour le clustering deviennent soudainement beaucoup plus clairs [26].

## Fusion des deux parties

Toutes les fonctionnalités ont été créées, il ne reste maintenant plus qu'à les utiliser pour créer notre application. Je remercie ma méthode de prototypage ici. Chaque fichier du projet contient une feature, chacun de ces features contient une main avec un exemple de fonctionnement. Il alors très facile de reprendre les exemples et de les exécuter de façon séquentielle. Il manquait juste à donner une signification (un nom) aux clusters et d'automatiser un protocole de tests pour les fichiers audios. Et bien entendu, il fallait rajouté des corpus. J'ai fait du copier-coller de Wikipédia pour des sujets clés.

J'ai quand même rajouté quelques goodies tels que : la sérialisation de la matrice de vecteurs multidimensionnels et des transcriptions de fichiers audio; Le choix pour l'utilisateur de voir soit le nom des clusters basé sur le nom des corpus ou un top de fréquences les plus élevées; Et j’ai remplacé textblob avec NLTK, lors de la création des fréquences des mots d’un corpus. Ce sont donc les synset qui sont utilisés pour les adjectifs, verbes, adverbes, et noms uniquement. J’ai ainsi un vecteur de mots qui représente un corpus propre de mot inexistant dans le WordNet, et sans synonymes.

# Évaluation

Dans l'optique d'évaluer les performances de l'application, nous avons mis au point une expérience de classification d'appels d'urgences impliquant 2 humains et notre application. Pour les humains, le but de l'expérience est d'écouter une série d'appels d'urgence et de les classifier chacune dans une classe d'urgence mise à disposition. Suite à ça nous comparons les classifications des humains avec notre application. Si l'application trouve la même classification ou un synonyme, alors elle réussit le test et se voit ajouter 1 à son score. Sinon elle reçoit 0 point. Nous calculerons le pourcentage de réussite du test.

Pour éviter de fausser les résultats de l'analyseur de context, les enregistrements utilisés sont des appels d'urgence sur lesquels la reconnaissance vocale fonctionne de façon pertinente, c'est-à-dire qu'elle ne retourne pas de résultat nul ou quasi nul, et que la langue ne soit pas autre que l'anglais, auquel cas les résultats sont considérés comme non analysable et sont exclues du test.

Notons également que les clusters ont été générés avec comme indication d'essayer d'atteindre 100 clusters.

Les classes mises à disposition sont:

- Voiture, panne, stationnement, transport public, accident, trafic
- Vélo, vélomoteur, moto
- Disputes, voies de fait, voisinage
- Tapage, bruit
- Disparition, fugues, levées de corps, tentatives de suicide
- Vols en tout genre, cambriolage
- Vandalisme, dommages à la propriété, feu, eau
- Animaux perdus, animaux écrasés
- Homme, femme, enfant
- Signe de détresse

## Tests

### Nom du fichier: **en-arlington-heights-drowning**

- Classement humain 1: panne, voiture, eau
- Classement humain 2: femme. panne, voiture
- Classement de l'application: wikipedia-car
- Resultat: 1

### Nom du fichier: **en-jersey-city-fire**

- Classement humain 1: feu, voisinage
- Classement humain 2: feu, signe de détresse, homme, femme
- Classement de l'application: Wikipédia-fire
- Resultat: 1

### Nom du fichier: **en-metrolink-crash**

- Classement humain 1: traffic, accident, transport public
- Classement humain 2: transport public, accident, homme, signe de détresse
- Classement de l'application: Wikipédia-traffic
- Resultat: 1

### Nom du fichier: **en-orlando-kidnapping**

- Classement humain 1: disparition, enfant, voisinage, femme
- Classement humain 2: disparition, fugues
- Classement de l'application: Wikipédia-childbirth, wikipedia-neighbours, wikipedia-young_adult
- Resultat: 1

### Nom du fichier: **en-wheelchair**

- Classement humain 1: Signe de détresse, femme
- Classement humain 2: enfant, signe de détresse
- Classement de l'application: wikipedia-distress_signal
- Resultat: 1


## Résultat final
- L'application a obtenu un score de 5 sur 5 soit 100% de compréhension du contexte pour les corpus en leurs totalité.
- Nous pouvons avancer que lorsque les conditions de propreté du son imposé par la reconnaissance vocale sont respectées, l'application peut extraire des informations clés pouvant rediriger un appel vers le bon interlocuteur, soit lors de notre test: problème de voiture, service du feu, problème de traffic, enfant, et signe de détresse globale.

# Conclusion

- Dans la dernière itération du projet, l'application est capable de d'apprendre et classifier des corpus complets et de trouver le contexte d'un nouveau corpus basé sur son apprentissage.

- Une très grande partie du temps dédié au projet d'automne de 3e année s'en est allée dans la reconnaissance vocale. Le résultat de recherches et tests a permis de mettre en avant un problème technologique à ce niveau. Il faudrait idéalement que quelqu'un, ou un groupe de recherche, travaille sur le problème et propose une solution avancée. Les solutions software propriétaire sont multiples, mais pas vraiment meilleures que les solutions dites gratuites, une fois qu'on a investi beaucoup de temps pour leur apprentissage d'utilisation. Les solutions limitées au nombre de requêtes (généralement 10'000 requêtes journalières) dans le cloud ont cependant été plus facile à prendre en main pour des résultats parfois satisfaisants.

- La récupération de contenus originaux de la police d'urgence, autant au niveau audio que corpus, a été une expérience très intéressante personnellement. Elle m'a permis de prendre contact avec des personnes aux perspectives différentes et enrichissantes, autant pour l'entraide et que pour l'opportunité de tirer profit de situations inattendues.

- L'analyse de corpus avec la librairie NLTK a été la plus agréable découverte de ce projet, malgré un début difficile pour la compréhension des concepts de base. Textblob quant a lui m'a permis de comprendre plus facilement le contexte d'analyse lexicale. Les possibilités qu'offre NLTK et Textblob dépassent largement ce que je m'imaginais de la technologie dans ce domaine à ce jour. Mais il faut noter que mon appréciation se base sur l'analyse de corpus en anglais. Les tests que j'ai effectués avec des corpus en français m'ont cependant assez impressionné malgré le manque de précision parfois sur la tokenization des mots, mais rien de bien dramatique, à la même manière que la reconnaissance vocale.

- L'apprentissage des corpus est fait avec l'algorithme K-Means, qui s'occupe de créer des clusters avec un sens commun. J'ai perdu du temps sur la conceptualisation et la compréhension d'un espace à N dimensions, car j'était bloqué dans un univers à maximum 3 dimensions. Cependant, une fois le déclic, il a été facile de mettre en place cet algorithme.

- Notons également que la fonctionnalité de récupération du lieu, de l'incident, etc. ainsi que de la détection d'un niveau d'importance dans le corpus n'a malheureusement pas été développée par manque de temps. Cependant, les outils déjà développés permettront une réalisation de ces fonctionnalités de façon plus simplifiée.

- Au niveau du planning, le temps m'a semblé très court cette année avec les problèmes de prise en main des logiciels et des technologies, pour au final se rendre compte que l'avancée technologique au niveau de la reconnaissance vocale est inadéquate pour les objectifs du projet. Le planning n'a donc pas été respecté rigoureusement, et le produit final n'est pas celui attendu. Cependant, les performances dans le contexte d'enregistrement dit propre sont très satisfaisantes.

- L'idéalisation des capacités possibles de l'application comme par exemple, l'analyse à la volée d'un appel ou le regroupement d'appels en simultané n'a pas pu être explorée correctement de façon à en tirer une conclusion avancée. Notons cependant que lors de tests pour tâter le domaine, je me suis rendu compte que le principal problème est la reconnaissance vocale. En effet, les performances de compréhension d'un seul mot ou un groupe de très peu de mots sont très mauvaises en comparaison d'un ensemble de mots. Cela est dû je pense à l'algorithme utilisé pour la reconnaissance vocale, qui essaie de regrouper les sons qui sont le plus souvent ensemble pour essayer de donner une correspondance.

- À nouveau, l'application n'a pas abouti à ses espérances, et la redirection des appels n'est pas implémentée en tant que tel, cependant il est facile pour l'utilisateur de l'application en l'état de voir ce qu'elle a compris du contexte et prendre les mesures nécessaires. De plus avec les capacités de l'application à nouveau en l'état, il est tout à fait possible d'implémenter le reste des fonctionnalités imaginées pour l'application alors qu'elle était encore au stade de pensée, lorsque la reconnaissance vocale sera capable de comprendre un mot dans un environnement mauvais.

- Mais globalement, je ne suis pas particulièrement content de la tournure du projet. Avant de proposer le projet à *M. Ghorbel*, j'avais effectué quelques recherches de l'existant. Ces recherches avaient mis en avant le fait que ce projet était possible, et j'avais donc comme ambition d'obtenir au moins un prototype fonctionnel, et de pouvoir continuer ce projet dans la suite de mon bachelor. Cependant, il s'est avéré que je m'étais trompé sur un point: les technologies prometteuses en reconnaissance vocale ne sont malheureusement pas encore d'actualité. Résultant en un projet plutôt orienté dans l'exploration technologique, et une application capable d'apprendre des corpus et de comprendre un fichier audio plus ou moins clair.


# Procédure de déploiement

Afin de pouvoir utiliser l'application, il faudra installer les dépendances du projet. La procédure qui suit est valide pour un univers UNIX. De plus, notons que la librairie SoX qui est incluse dans les sources fonctionne out-of-the-box sur une architecture UNIX uniquement. Pour plus de détails concernant SoX, veuillez vous référer à la documentation [14].

## Étape 1: Python > 3.0
Pour pouvoir exécuter l'application il faut primordialement installer l'interpréteur python et de préférence de version 3.0 ou supérieure. Généralement, c'est la version 2.7 qui est installée par défaut sur votre machine, et accessible via le terminal avec la commande *python*.

- Rendez-vous sur https://www.python.org/downloads/ télécharger et installez la dernière version de l'installeur 3.x.x où les x représentent des nombres.
- Depuis votre terminal, exécuter *python3 --version*, vous deviez recevoir comme résultat: Python 3.x.x

## Étape 2: Python Pip
Notre application tourne effectivement avec l'interpréteur Python, cependant, elle a aussi besoin de packages (librairies) pour fonctionner. Pour installer ces packages, il faut installer l'installateur de packages *pip*.

- Pour vérifier si vous avez déjà pip installé pour python3, exécutez dans votre terminal *pip3 --version*, si vous obtenez un résultat vous pouvez ignorer le prochain point.
- Executer dans votre terminal: *python3 get-pip.py*. Après l'installation, essayez à nouveau *pip3 --version*. , vous devriez obtenir un résultat similaire: pip x.x.x from .../lib/python3.x/site-packages (python 3.x)

## Étape 3: Python Packages
- Nous allons maintenant installer les packages, lancez les commandes suivantes depuis votre terminal:
  - *pip3 install SpeechRecognition*
  - *pip3 install kmeans*
  - *pip3 install nltk*
  - *pip3 install numpy*
  - *pip3 install scipy*

# Utilisation
Vous devez tourner sur une architecture UNIX pour la garantie de l'utilisation de l'application.

À la racine de l'application, vous trouverez 8 fichiers et 5 dossiers.

- **audioRaw** est un dossier contenant les fichiers audios au format wav. Ce dossier est à remplir avec un fichier audio pour le classifier.

- **audioProcessed** est un dossier contenant les fichiers audios découpés au format wav. Ce dossier est géré par le programme.

- **serializedData** est un dossier contenant les fichiers de sérialisation. Vous trouverez ici la matrice vectorielle multidimensionnelle de connaissance de l'application, ainsi que des fichiers dans le sous-dossier audioTranscripts contenant les sauvegardes des corpus speech-to-text.

- **sox** est un dossier contenant les binaires de l'application SoX, qui est un programme servant à manipuler les fichiers audios.

- **trainingCorpus** est un dossier contenant les corpus sous format texte pour l'entrainement de la base de connaissance de notre application. Ce dossier est à remplir pour améliorer les capacités de compréhension de l'application.

- **main.py** est une démonstration des capacités de l'application.
Lors de son exécution *python3 main.py*, ce programme fait appel aux autres fichiers dans le but de:
  - Procéder à l'entraînement de sa base de connaissances et les classifier.
  - Decouper les fichiers audios aux silences.
  - Extraire le corpus de fichiers audio avec la reconnaissance vocale.
  - Donner un contexte aux fichiers audio basés sur ses connaissances.
  - Mémoriser la base de connaissances et les corpus des fichiers audios pour accélérer le temps des prochaines exécutions.
En ce qui concerne son utilisation, ce fichier et particulièrement bien documenté avec les commentaires, de façon d'aider à reproduire certains comportements.

- **audio_spliter.py** permet de découper les fichiers audios aux silences.
Lors de son exécution *python3 audio_spliter.py*, ce programme découpera tous les fichiers audios présents dans le dossier audioRaw et les enregistrera dans le dossier audioProcessed dans le sous-répertoire portant le nom du fichier. Les fichiers porteront un suffixe à 3 chiffres indiquant leurs ordres.

- **speech_to_text.py** permet de lire les fichiers audios et d'effectuer une reconnaissance vocale.
Lors de l'exécution *python3 speech_to_text.py*, ce programme effectuera le transcript du premier fichier audio (dans l'ordre alphabétique) du dossier rawAudio.

- **kmeans_nD.py** permet d'effectuer la classification de N vecteurs à M dimensions sous forme de clusters. Vous pouvez obtenir plus d’informations au sujet de l'algorithme K-Means avec la documentation [19].
Lors de l'exécution *python3 kmeans_nD.py*, ce programme effectuera un exemple de clustering avec les données suivantes:
  - nombre de clusters = 3
  - le data sample = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 3.5], [7, 2.5], [8, 1.5], [0, 0]]
  - vecteur à classer = [1.5, 1.5]

- **part_of_speech.py** permet de nettoyer et effectuer la tokenization d'un corpus avec les synsets [20] de wordnet [21].
Lors de l'exécution *python3 part_of_speech.py*, ce programme prendra le premier corpus dans le dossier trainingCorpus (dans l'ordre alphabétique) et affichera le résultat de la tokenization.

- **meaning_space.py** permet de construire un espace vectoriel multidirectionnel de mots.
Lors de l'exécution *python3 meaning_space.py*, ce programme construira un espace vectoriel multidimensionnel avec les 2 premiers corpus dans le dossier trainingCorpus (dans l'ordre alphabétique), et affichera celle-ci.

- **common_functions.py** contient toutes les fonctions communes utilisées au travers de l'application.
Ce programme ne peut pas être directement exécuté.

- **tweaks.py** contient toutes les valeurs utilisées au travers de l'application.
Ce programme ne peut pas être directement exécuté.

# Bibliographie
## Différents tutoriels
Lors de l'exploration des différentes technologies, il a été important de tomber sur de bons tutoriels. Ci-dessous une liste que j'ai trouvée bien faite.

- NLTK Book: 
	- http://www.nltk.org/book/
- Named Entity Recognition: 
	- http://www.nltk.org/book/ch07.html
- NLTK Quickstart: 
	- http://www.nltk.org
- TextBlob Quickstart: 
	- https://textblob.readthedocs.org/en/dev/quickstart.html
- Speech recognition helloworld in Python + Sphinx: 
	- http://kermit.epska.org/2011/python-speech-recognition-helloworld/
- The SoX of Silence: 
	- http://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/

## Outils
- dOxygen pythonblocks: 
	- https://www.stack.nl/~dimitri/doxygen/manual/docblocks.html#pythonblocks

## Références
- [1] Geo-based tweet analysis to alert emergency services:
	- http://www.ymc.ch/en/geo-based-tweet-analysis-to-alert-emergency-services
- [2] Putting Robots To Work To Make New York City’s 311 A Better-Oiled Machine: 
	- http://www.fastcoexist.com/3031202/putting-robots-to-work-to-make-new-york-citys-311-a-better-oiled-machine
- [3] ECaTS and SQLstream Deliver Cloud Platform for Real-Time 911 Call Analytics: 
	- http://www.sqlstream.com/blog/tag/real-time-analytics/
- [4] The idea of Sentdex is to quantify the qualitative: 
	- http://sentdex.com
- [5] Dragon Speech Recognition Software: 
	- http://www.nuance.com/dragon/index.htm
- [6] Speech recognition extension library: 
	- https://pypi.python.org/pypi/dragonfly/0.6.5
- [7] Library for performing speech recognition with support for Google Speech Recognition, Wit.ai, IBM Speech to Text, and AT&T Speech to Text: 
	- https://pypi.python.org/pypi/SpeechRecognition
- [8] The Chromium Projects API Keys: 
	- http://www.chromium.org/developers/how-tos/api-keys
- [9] Console Google APIs: 
	- https://console.developers.google.com/
- [10] Pocketsphinx wrappers with SWIG for Ruby and Javascript: 
	- http://cmusphinx.sourceforge.net
- [11] The Hidden Markov Model Toolkit: 
	- http://htk.eng.cam.ac.uk
- [12] Tropo makes it simple to automate communications, connecting your code to the phone network with both voice and messaging: 
	- https://www.tropo.com
- [13] VoxForge was set up to collect transcribed speech for use: 
	- http://www.voxforge.org
- [14] Swiss Army knife of sound processing programs: 
	- http://sox.sourceforge.net
- [15] Natural Language Toolkit: 
	- http://www.nltk.org
- [16] TextBlob is a Python (2 and 3) library for processing textual data: 
	- https://textblob.readthedocs.org/en/dev/index.html
- [17] The TreeTagger is a tool for annotating text with part-of-speech and lemma information: 
	- http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/
- [18] Tutorial on PocketSphinx with Python 3.4: 
	- http://depado.markdownblog.com/2015-05-13-tutorial-on-pocketsphinx-with-python-3-4
- [19] K-Means Clustering, from Wikipedia, the free encyclopedia: 
	- https://en.wikipedia.org/wiki/K-means_clustering
- [20] Synsets, from Wikipedia, the free encyclopedia: 
	- https://en.wikipedia.org/wiki/Synonym_ring
- [21] WordNet, from Wikipedia, the free encyclopedia: 
	- https://en.wikipedia.org/wiki/WordNet
- [22] Adding a French Wordnet to NLTK? Google Group Discussion: 
	- https://groups.google.com/forum/#!topic/nltk-users/N6ueNs-k084
- [23] Tokenization (lexical analysis): 
	- https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)
- [24] Lemmatisation: 
	- https://en.wikipedia.org/wiki/Lemmatisation
- [25] Real 911 Calls and Police Dispatch Audio : 
	- http://www.documentingreality.com/forum/f218/
- [26] K-means clustering and vector quantization: 
	- http://docs.scipy.org/doc/scipy/reference/cluster.vq.html
	
# Dédicace
Je tiens personnellement remercier *M. Viuille*, Chef CET de la police neuchâteloise, pour sa gentillesse lors de notre rencontre, d'avoir cru en mon projet, et pour l'aide précieuse qu'il m'a apportée.

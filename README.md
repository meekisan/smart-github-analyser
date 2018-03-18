# smart-git hub-analyser

>*Projet de certification "  BIG DATA : Récolte et analyse des données volumineuses*"


# Auteur et copyright


 1. **Cécile Gracianne** [*(Research](https://www.researchgate.net/profile/Cecile_Gracianne) | [*LinKedIn*)*](https://www.linkedin.com/in/cecilegracianne/)
 Docteur en Biologie et Agronomie, a travaillé à l'INRA de Rennes et VetAgro-Sup de Clermont-Ferrand

 2. **Alexandre Blukacz** [*(LinKedIn)*](https://www.linkedin.com/in/alexandre-blukacz-4286103/)
Développeur, a travaillé pour Claranet, Agarik et dernièrement MobParner sur la partie adserving et statistique.

 3. **Paul-Arnaud PY**  [*(LinKedIn)*](https://www.linkedin.com/in/paularnaudpy/)
 A conduit, en tant que CTO de Météo France Régie, de 2008 à 2017 *(Publicité Digital web et mobile)*, de nombreux  [POC](https://business.lesechos.fr/entrepreneurs/marketing-vente/six-regles-pour-reussir-son-proof-of-concept-avec-un-grand-groupe-311352.php)

  # État du projet

     [/!\] A date ce projet n'est pas exploitable  [/!\]

**Version alpha**

Tous les fichiers présentés ont pour objet d'être déployés en production à travers un ensemble de [docker](https://www.docker.com/) *( logiciel libre automatisant le déploiement d'applications dans des conteneurs logiciels ; c'est-à-dire qui permettent aux architectures applicatives d'évoluer vers un modèle distribué de microservices optimisé pour piloter des processus de déploiement continu sans couture)* .  
*Notre objectif, à travers ces dockers, est de présenter un POC  facilement évolutif et où chacune des parties peut être travaillée indépendamment les unes des autres.*

# Rapide description

A partir de données publiques liées à Github, archivées ou non, nous vous présentons dans ce document les réflexions et autres livrables permettant de stocker les données utiles à la construction d’un générateur de commits et de fichiers aléatoires en vue de refléter au mieux les données permettant de valider un moteur de recommandation ainsi qu’un moteur de recherche.
Enfin, et à partir d’une analyse dynamique et répondant aux besoins d’un maximum utilisateurs, nous proposons d’afficher les projets qui répondent le mieux aux besoins exprimés et quelle que soit l’ancienneté projetée du projet.

Ce guide, à partir de données publiques, a pour objectif de permettre de partager, d’apprendre et de travailler ensemble dans le traitement et l’analyse de données volumineuses.

> Les dataset publics de Github évoluent tous les jours et ne sont pas disponibles directement ni en csv ni en [ndjson](http://ndjson.org/) .


# Techno Utilisées

L'ensemble des moyens et outils utilisés a été rendu possible à travers les offres de découvertes, souvent gratuites, de différentes sociétés.


**Base de données**

Les outils ci-après disposent soient de connecteurs soit permettent  d'exporter/importer nativement des données.   

> **[Google Big Query](https://cloud.google.com/bigquery/?hl=fr)** : Infrastructure en tant que service public (IaaS) qui permet l'analyse interactive massive de grands ensembles de données en collaboration avec l'espace de stockage Google.   

> **[MongoDB](https://www.mongodb.com/fr)** : système de gestion de base de données orientée documents, répartissable sur un nombre quelconque d'ordinateurs et ne nécessitant pas de schéma prédéfini des données

> **[Neo4j](https://neo4j.com)** : système de gestion de base de données au code source libre basée sur les graphes


**Programmation**

Les langages, package et format de données utilisés ici sont soit directement liés aux traitements de données volumineuses soit parfaitement adaptés à leur exploitation.

> **[Python](https://www.python.org)** : langage de programmation objet, multi-paradigme et multiplateformes. Il favorise la programmation impérative structurée, fonctionnelle et orientée objet

> **[R](https://www.r-project.org)** : langage de programmation dédié aux statistiques et à la science des données

> **[Shiny](https://shiny.rstudio.com)** : package offrant une solution de data visualisation pour le logiciel _R_

> **[json](https://www.json.org)** :  format de données textuelles dérivé de la notation des objets du langage JavaScript et permet de représenter de l’information structurée.  (*json = JavaScript Object Notation)*

> [**php**](https://secure.php.net/) : _Hypertext Preprocessor_ langage de programmation libre, principalement utilisé pour produire des pages Web dynamiques via un serveur HTTP


**NoteBook**

> **[Jupyter](http://jupyter.org/)** : application web utilisée pour programmer dans plus de 40 langages de programmation et permet de réaliser des notebooks ; c'est-à-dire des programmes contenant à la fois du texte en "markdown" et du code.


**Architecture**

Cette architecture répond à un besoin de "Map/Reduce" performant et visuel  

> **[ElasticSearch](https://www.elastic.co/fr/)** : serveur utilisant Lucene pour l'indexation et la recherche des données. Il fournit un moteur de recherche distribué et multi-entité à travers une interface REST

> **[Kibana](https://www.elastic.co/fr/products/kibana)** : client pour ElasticSearch qui fournit à l'utilisateur une interface graphique (UI) accessible par un navigateur web


**Infrastructure**

L’infrastructure déployée ici permet de prendre en compte la génération de fichier depuis Big Query ainsi que leurs traitements selon l'ordre d'arrivé et de sortie attendu

> **[RabbitMQ](https://www.rabbitmq.com)** : logiciel d'agent de messages open source qui implémente le protocole Advanced Message Queuing

> **[Google Cloud](https://cloud.google.com/?hl=fr)**: Platform qui permet de développer et d'héberger des applications ainsi que des sites Web, de stocker des données et de les analyser, le tout au sein de l'infrastructure évolutive de Google.

> **[AWS](https://aws.amazon.com/fr/)** : _Amazon Web Services_  propose des services de cloud computing fiables, évolutifs et économiques. Inscription gratuite et paiement à l'utilisation. Il permet, contrairement à Google Cloud, d'avoir une connexion RabbitMQ en natif.


Enfin, pour réaliser ce repository, nous avons travaillé à distance à travers des outils disponibles dont :

> **[Slack](https://slack.com/intl/fr-fr)** : plate-forme de communication collaborative propriétaire

> ***_Appear.in_*** : outil collaboratif qui permet de créer des vidéoconférences à partir d'un navigateur

> [**Google Drive**](https://www.google.com/intl/fr_ALL/drive) :  service de stockage et de partage de fichiers dans le cloud de Google et indépendant du service Google Cloud


*En mars 2018, nous avons profité de l'offre de découverte de 300$US par utilisateur et proposée par Google afin d'accéder à un ensemble de produits et services de Google dont :  Big Query et Google Cloud.*


# Mise en place, utilisation rapide

Décompressez ce projet dans un dossier de votre ordinateur ; par exemple, dans le dossier *github/smart-github-analyser* et accessible à :

    C:\github\smart-github-analyser\


Activez ensuite  l'application Docker. *Si vous ne l'avez pas encore, vous pouvez suivre  ce lien pour l'installer :* [*https://docs.docker.com/install/*](https://docs.docker.com/install/)

Une fois l'application Docker lancée, parcourez votre espace pour vous dirigez dans le répertoire où se trouve ce projet ; utilisez les commandes `ls` pour lister les dossiers et fichiers contenues dans le répertoire et `cd` pour *changer de directory* (répertoire) afin de lister.  Dans notre exemple, saisissez la commande suivante :

    C:\ cd github/smart-github-analyser/

Une fois dans le  dossier, écrivez la [ligne de commande shell](https://doc.ubuntu-fr.org/shell)  :

    docker-compose up --build -d


> cette commande permet de construire les images dockers correspondantes à chacun des _Dockerfile_ ([cf. doc](https://docs.docker.com/)).

Quand l'installation est terminée, vous devez vérifier l'état de vos images.  Pour cela il vous faut écrire comme commande shell :

    docker-compose ps

Le contenu suivant, indiquant le nom de vos images, les commandes correspondantes, l'état et le port pour y accéder s'affichent.

|Name              |Command                          |State   |Ports
|------------------|---------------------------------|--------|----------------------------------------------------------------------------
|apache-php        |/usr/sbin/apache2ctl -D FO ...   |Up      |443/tcp, 0.0.0.0:81->81/tcp
|githubarchive     |/bin/sh -c cron && tail -f ...   |Up      |
|broker-consumer   |/bin/sh -c /usr/bin/python ...   |Up      |
|datastorage2      |docker-entrypoint.sh mongod      |Up      |0.0.0.0:27017->27017/tcp, 0.0.0.0:27018->27018/tcp, 0.0.0.0:27019->27019/tcp
|kibana            |/bin/bash /usr/local/bin/k ...   |Up      |0.0.0.0:5601->5601/tcp
|prediction        |/bin/sh -c sleep infinity        |Up      |0.0.0.0:4040->4040/tcp, 8888/tcp, 0.0.0.0:8889->8889/tcp
|rabbitmq          |docker-entrypoint.sh rabbi ...   |Up      |15671/tcp, 0.0.0.0:15672->15672/tcp, 25672/tcp, 4369/tcp, 5671/tcp, 5672/tcp
|recommandation2   |/docker-entrypoint.sh neo4j      |Up      |7473/tcp, 0.0.0.0:7474->7474/tcp, 0.0.0.0:7687->7687/tcp
|search            |/usr/local/bin/docker-entr ...   |Up      |0.0.0.0:9200->9200/tcp, 9300/tcp


Pour évoluer dans ce projet, vous aurez besoin de vous connecter à un certaine interface dont :

> **Rabbitmq**  sur le port avec 15672. Par exemple via l'url  http://localhost:15672 et avec comme identifiant/mot de passe :  *guest/guest*

> **neo4j**  sur le port avec 7474. Par exemple via l'url  http://localhost:7474

> **kibana**  sur le port avec 5601. Par exemple via l'url  http://localhost:5601

> **Moteur de recommandation et de recherche**  sur le port avec 81. Par exemple via l'url  http://localhost:81


# Licence(s)

[Licence MIT](https://opensource.org/licenses/MIT)

Copyright  2018
Cécile Gracianne & Alexandre Blukacz & Paul-Arnaud PY

Par les présentes, la permission est accordée, sans frais, à toute personne qui obtient une copie de ce logiciel et des fichiers de documentation associés (dit le "Logiciel"), afin de traiter les éléments suivants dans le Logiciel sans restriction, y compris, sans limitation sur les droits d'auteur, d'utiliser, copier, modifier, fusionner, publier, distribuer, sous-licencier et/ou vendre des copies du Logiciel, et de permettre aux personnes à qui le Logiciel est destiné à cet effet, sous réserve des conditions suivantes :

L'avis de droit d'auteur ci-dessus et le présent avis d'autorisation doivent être inclus dans tous les documents suivants des copies ou des portions substantielles du Logiciel.

LE LOGICIEL EST FOURNI "EN L'ÉTAT", SANS GARANTIE D'AUCUNE SORTE, EXPRESSE OU NON IMPLICITE, Y COMPRIS, MAIS SANS S'Y LIMITER, LES GARANTIES DE QUALITÉ MARCHANDE, L'APTITUDE À UN USAGE PARTICULIER ET L'ABSENCE DE CONTREFAÇON. EN AUCUN CAS, LES AUTEURS OU LES DÉTENTEURS DE DROITS D'AUTEUR SONT RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE.

LA RESPONSABILITÉ, QU'IL S'AGISSE D'UNE ACTION EN RESPONSABILITÉ CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DE, EN DEHORS OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES TRANSACTIONS DANS LE CADRE DE L'UTILISATION DU LOGICIEL OU D'AUTRES TRANSACTIONS DANS LE CADRE DE L'UTILISATION DU LOGICIEL OU D'AUTRES TRANSACTIONS DANS LE CADRE DE L'UTILISATION DU LOGICIEL OU DES TRANSACTIONS DANS LE CADRE DE L'UTILISATION DU LOGICIEL OU DES TRANSACTIONS DANS LE CADRE DE L'UTILISATION DE L'UTILISATION DU LOGICIEL.



# Documentation courte et/ou page pointant vers documentation longue (ou page d’exemple)

> voir le fichier portant sur la présentation


# Méthode de rapport de bug, contribution

A ce stade, et compte tenu que le projet n'est pas encore en phase de demande de contribution ni d'utilisation, aucune méthode de rapport de bug n'est proposée.
Cet état est temporaire et devrait évoluer dans les jours qui viennent.

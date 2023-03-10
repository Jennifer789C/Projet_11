# OpenClassRooms - Python - Projet 11 : Güdlft

Ce projet consiste à débugger une application rédigée par un autre 
développeur et poursuivre le développement :  
<!-- 2 espaces à la fin de la ligne pour un saut de ligne -->
	- utilisation du framework Flask,
	- utilisation du framework de test Pytest,
    - utilisation du package Locust pour l'élaboration de tests de performance,
	- débogage d'un code d'application,  
	- mise en place de différents tests.


## Application du script

A partir du terminal, se placer dans le répertoire souhaité

### 1. Récupérer le repository GitHub et créer un environnement virtuel

Cloner le repository GitHub :
```bash
git clone https://github.com/Jennifer789C/Projet_11.git
```
Puis se placer dans le répertoire du projet :
```bash
cd Projet_11
```
*Pour ma part, je travaille sous Windows et avec l'IDE PyCharm, la création d'un environnement virtuel se fait via les paramètres de l'IDE*

Depuis un terminal sous Windows :
```bash
python -m venv env
env/Scripts/activate
```

Depuis un terminal sous Linux ou Mac :
```bash
python3 -m venv env
source env/bin/activate
```

### 2. Installer les packages du fichier requirements.txt

Dans l'environnement virtuel, télécharger l'ensemble des packages indiqués 
dans le fichier requirements.txt :
```bash
pip install -r requirements.txt
```

### 3. Lancer le serveur

Vous devez indiquer à Flask que votre app est sur le fichier server.py :

*Pour ma part, je travaille sous Windows et avec Powershell*

Depuis Powershell :
```bash
$env:FLASK_APP = "server.py"
flask run
```

Depuis l'invite de commande de Windows :
```bash
set FLASK_APP=server.py
flask run
```

Depuis un terminal sous Linux ou Mac :
```bash
export FLASK_APP=server.py
flask run
```


### 4. Autres détails

Les mails de connexion des clubs sont dans le fichier clubs.json  
Si vous souhaitez vérifier les tests :  
- pour les tests unitaires et d'intégration :
```bash
pytest
```
- pour la couverture de tests :
```bash
pytest --cov=.
```
- pour les tests de performance, lancer le serveur flask sur un premier 
  terminal, puis sur un second :
```bash
cd tests/tests_performance
locust
```
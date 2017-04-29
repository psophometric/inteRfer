# inteRfer

## Description
Programmes [Python](https://www.python.org/) qui permettent de travailler sur la problématique des interférences GSM-R / GSM-Public, à partir du jeu de données de l'Anfr [Les installations radioélectriques de plus de 5 watts](https://www.data.gouv.fr/fr/datasets/donnees-sur-les-installations-radioelectriques-de-plus-de-5-watts-1/)

- **inteRfer-up**
Equivalent à un update/upgrade sur le jeu de données.
- **inteRfer-distance**
Extraction des sites GSM-Public situés autour des sites GSM-R.
- **inteRfer-azimut**
[TODO] WorkInProgress..

## Dépendances
- [Folium](https://github.com/python-visualization/folium)
- [Geopy](https://github.com/geopy/geopy)

## Installation (Linux Debian / Ubuntu)
Pré-requis (Pip, Git)
```
sudo apt-get install python-pip
sudo apt-get install git
```
Dépendances<br>
`pip install folium`<p>

`pip install geopy`<p>

Récupérer le dépôt <br>
`git clone https://github.com/psophometric/inteRfer.git`<p>
Initialisation de la base
```
cd inteRfer/
python inteRfer-up.py
```

## Usage
`python inteRfer-up.py`
Vérifie que la version du jeu de données dans le répertoire est bien à jour. Si nécessaire : télécharge et décompresse le jeu de données. **A exécuter en premier, après l'installation pour initialiser les bases.**<p>


`python inteRfer.py -d 5` Affiche les supports GSM-Public distants de moins de 5 km avec un support GSM-R.<br>
`python inteRfer.py -d 5 -f 75` Affiche les supports GSM-Public distants de moins de 5 km avec un support GSM-R situés dans le département 75.<p>

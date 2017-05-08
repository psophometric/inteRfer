# -*- coding: utf-8 -*-
import csv
import folium
from geopy.distance import vincenty
from geopy.distance import VincentyDistance
from geopy.distance import Point
import argparse

#### https://gist.github.com/sunny/13803
limit = {
"01":["38","39","69","71","73","74"],
"02":["08","51","59","60","77","80"],
"03":["18","23","42","58","63","71"],
"04":["05","06","26","83","84"],
"05":["04","26","38","73"],
"06":["04","83"],
"07":["26","30","38","42","43","48","84"],
"08":["02","51","55"],
"09":["11","31","66"],
"10":["21","51","52","77","89"],
"11":["09","31","34","66","81"],
"12":["15","30","34","46","48","81","82"],
"13":["30","83","84"],
"14":["27","50","61","76"],
"15":["12","19","43","46","48","63"],
"16":["17","24","79","86","87"],
"17":["16","24","33","79","85"],
"18":["03","23","36","41","45","58"],
"19":["15","23","24","46","63","87"],
"2A":["2B"],
"2B":["2A"],
"21":["10","39","52","58","70","71","89"],
"22":["29","35","56"],
"23":["03","18","19","36","63","87"],
"24":["16","17","19","33","46","47","87"],
"25":["39","70","90"],
"26":["04","05","07","38","84"],
"27":["14","28","60","61","76","78","95"],
"28":["27","41","45","61","72","78","91"],
"29":["22","56"],
"30":["07","12","13","34","48","84"],
"31":["09","11","32","65","81","82"],
"32":["31","40","47","64","65","82"],
"33":["17","24","40","47"],
"34":["11","12","30","81"],
"35":["22","44","49","50","53","56"],
"36":["18","23","37","41","86","87"],
"37":["36","41","49","72","86"],
"38":["01","05","07","26","42","69","73"],
"39":["01","21","25","70","71"],
"40":["32","33","47","64"],
"41":["18","28","36","37","45","72"],
"42":["03","07","38","43","63","69","71"],
"43":["07","15","42","48","63"],
"44":["35","49","56","85"],
"45":["18","28","41","58","77","89","91"],
"46":["12","15","19","24","47","82"],
"47":["24","32","33","40","46","82"],
"48":["07","12","15","30","43"],
"49":["35","37","44","53","72","79","85","86"],
"50":["14","35","53","61"],
"51":["02","08","10","52","55","77"],
"52":["10","21","51","55","70","88"],
"53":["35","49","50","61","72"],
"54":["55","57","67","88"],
"55":["08","51","52","54","88"],
"56":["22","29","35","44"],
"57":["54","67"],
"58":["03","18","21","45","71","89"],
"59":["02","62","80"],
"60":["02","27","76","77","80","95"],
"61":["14","27","28","50","53","72"],
"62":["59","80"],
"63":["03","15","19","23","42","43"],
"64":["32","40","65"],
"65":["31","32","64"],
"66":["09","11"],
"67":["54","57","68","88"],
"68":["67","88","90"],
"69":["01","38","42","71"],
"70":["21","25","39","52","88","90"],
"71":["01","03","21","39","42","58","69"],
"72":["28","37","41","49","53","61"],
"73":["01","05","38","74"],
"74":["01","73"],
"75":["92","93","94"],
"76":["14","27","60","80"],
"77":["02","10","45","51","60","89","91","93","94","95"],
"78":["27","28","91","92","95"],
"79":["16","17","49","85","86"],
"80":["02","59","60","62","76"],
"81":["11","12","31","34","82"],
"82":["12","31","32","46","47","81"],
"83":["04","06","13","84"],
"84":["04","07","13","26","30","83"],
"85":["17","44","49","79"],
"86":["16","36","37","49","79","87"],
"87":["16","19","23","24","36","86"],
"88":["52","54","55","67","68","70","90"],
"89":["10","21","45","58","77"],
"90":["25","68","70","88"],
"91":["28","45","77","78","92","94"],
"92":["75","78","91","93","94","95"],
"93":["75","77","92","94","95"],
"94":["75","77","91","92","93"],
"95":["27","60","77","78","92","93"]
}

def insee(n_insee):
    """Ajoute des DATA Nom commune et n°département du dictionnaire insee
    au dictionnaire Support selon le code insee indiqué"""
    commune = d_insee.get(n_insee) # code insee
    if commune == None: # Pour gerer les erreurs Insee
        commune = ["","","","","","","","","","","","","","","","","","","",""]
    resultat = [commune[5],\
                commune[16]]
    return resultat

def conversion(coord_DMS) :
    """Converti les coordonnées DMS en DD"""
    if coord_DMS[3] == "N" or coord_DMS[3] == "E":
        coord_DD = coord_DMS[0] + (coord_DMS[1] * 1/60) + (coord_DMS[2] * 1/3600)
    if coord_DMS[3] == "S" or coord_DMS[3] == "W":
        coord_DD = (coord_DMS[0] + (coord_DMS[1] * 1/60) + (coord_DMS[2] * 1/3600)
                   )*(-1)
    return coord_DD

def chargement_fichier(chemin,i):
    """Ouvre et enregistre le fichier dans un dictionnaire.
    Suppression de la première ligne (labels)
    Key : le champs i
    Data : ensemble des champs"""
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=";"))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    dictionnaire = {}
    for definitions in liste :
        key_dico = definitions[i]   # n°STATION
        data_dico = definitions[0:] # Toutes les colonnes
        dictionnaire[key_dico] = data_dico
    return dictionnaire

def liste_unique(chemin,techno):
    """Extrait les émetteurs et retourne une liste unique des stations
    appartenant à la techno spécifiée"""
    fichier = open(chemin, "rb")
    liste = list(csv.reader(fichier,delimiter=";"))
    liste.pop(0) #suppression 1ere ligne
    fichier.close()
    liste_station = []
    liste_support = []
    liste_echec = []
    for emetteur in liste :
        if emetteur[1] in techno:
            liste_station.append(emetteur[2])
            try :
                support = d_support[emetteur[2]]
                liste_support.append(support[0])
            except :
                liste_echec.append(emetteur[2])
    #liste sans doublons :
    liste_station = set(liste_station)
    liste_support = set(liste_support)
    return liste_support, liste_station

def chargement_support(chemin):
        dictionnaire={}
        fichier = open(chemin, "rb")
        liste = list(csv.reader(fichier,delimiter=";"))
        liste.pop(0) #suppression 1ere ligne
        fichier.close
        for support in liste :
            n_support = support[0] # n°SUPPORT
            n_station = support[1]   # n°STATION
            id_nature = support[2]
            lat_dms = (float(support[3]), float(support[4]), float(support[5]), support[6])
            lat = conversion(lat_dms)
            lon_dms= (float(support[7]), float(support[8]), float(support[9]), support[10])
            lon = conversion(lon_dms)
            ville_dept = insee(support[18])
            data_station = d_station.get(n_station) #RECUPERATION DES VALEURS DU LA STATION
            try:
                exploitant=data_station[1]
            except:
                expl="none"
            #### CREATION DICTIONNAIRE ###
            try :
                data = dictionnaire[n_support]
            except:
                liste = []
                liste.append([lat, lon]) #0
                liste.append(ville_dept) #1
                liste.append([n_station])  #2
                liste.append([exploitant]) #3
                dictionnaire[n_support] = liste
                ##### CREATION DICO DEPT & DEPT_GEO ####
                try :
                    datadept_geo = d_dept_geo[ville_dept[1]]
                    datadept = d_dept[ville_dept[1]]
                except:
                    d_dept_geo[ville_dept[1]] = [(n_support,lat, lon)]
                    d_dept[ville_dept[1]] = [n_support]
                else :
                    datadept_geo.append((n_support, lat, lon))
                    datadept.append(n_support)
            else :
                data[2].append(n_station) # n°STATION
                data[3].append(exploitant)
        return dictionnaire, d_dept, d_dept_geo # Dictionnaire contenant par support : les différentes stations sous forme tuple (n°,exploitant)

def recherche_voisin(support, distance):
    data_sup = d_les_supports[support]
    dept_limitrof = limit[data_sup[1][1]]
    dept_limitrof.append(data_sup[1][1])
    geo_gsmr=data_sup[0]
    lat1, lon1 = geo_gsmr
    liste=[]
    origin = Point(lat1, lon1)
    limit0 = VincentyDistance(kilometers=distance).destination(origin, 0).format_decimal()
    limit90 = VincentyDistance(kilometers=distance).destination(origin, 90).format_decimal()
    lat0, lon0 = limit0.split(', ')
    lat90, lon90 = limit90.split(', ')
    dif0 = float(lat0) - lat1
    dif90 = float(lon90) - lon1
    latmini = lat1 - dif0
    latmaxi = float(lat0)
    lonmini = lon1 - dif90
    lonmaxi = float(lon90)
    for dept in set(dept_limitrof) :
        for support_P in d_dept_geo[dept]:
            if latmini <= support_P[1] <= latmaxi:
                if lonmini <= support_P[2] <= lonmaxi:
                    if support_P[0] in l_support_GsmP_seuls:
                        liste.append(support_P[0])
    return liste

def liste_voisin(liste, distance):
    l = []
    for support in liste :
        voisin = recherche_voisin(support,distance)
        l.extend(voisin)
    return l

def affichage_support(liste, couleur):
    for support in liste :
        data_sup = d_les_supports[support]
        geo=data_sup[0]
        html=str(support)
        iframe = folium.IFrame(html=html, width=275, height=175)
        popup = folium.Popup(iframe, max_width=2650)
        folium.Marker(geo,\
        popup=popup, icon = folium.Icon(color=couleur)).add_to(marker_cluster)


B900 = ['GSM 1800/GSM 900' , 'GSM 900' , 'GSM 900/GSM 1800' , 'GSM 900/UMTS 2100' , 'UMTS 2100/UMTS 900' , 'UMTS 900']
GsmR = ['GSM R']
d_dept, d_dept_geo = {}, {}

############################### PARSER #########################################
parser = argparse.ArgumentParser()
parser.add_argument('-d', action='store', dest='distance',
                    help='Ecart en km', type=int)
parser.add_argument('-f', action='store', dest='departement',
                    help='Filtre pour afficher un seul déartement', type=str)
results = parser.parse_args()
if results.distance:
    distance = results.distance
if results.departement:
    departement = results.departement
else:
    departement = False

################### Chargement des fichiers ####################################
d_support=chargement_fichier("csv/SUP_SUPPORT.txt", 1)
d_station=chargement_fichier("csv/SUP_STATION.txt", 0)
d_insee=chargement_fichier("csv/code-insee.csv", 4)
l_support_GsmR, l_station_GsmR = liste_unique("csv/SUP_EMETTEUR.txt",GsmR)
l_support_GsmP, l_station_GsmP = liste_unique("csv/SUP_EMETTEUR.txt",B900)
d_les_supports, d_dept, d_dept_geo=chargement_support("csv/SUP_SUPPORT.txt")

### CREATION DES LISTES DE SITES GSM ###
l_support_GsmP_seuls = l_support_GsmP - l_support_GsmR
l_support_GsmR_seuls = l_support_GsmR - l_support_GsmP
l_support_Gsm_mixte = l_support_GsmP & l_support_GsmR

### FILTRER UN SEUL DEPARTEMENT (option) ###
if departement:
    l_filtre = d_dept[departement]
    l_support_GsmR_seuls = l_support_GsmR_seuls & set(l_filtre)
    l_support_Gsm_mixte = l_support_Gsm_mixte & set(l_filtre)

### RECHERCHE DES SITES VOISINS ###
l_voisin_GsmR = liste_voisin(l_support_GsmR_seuls, distance)
print "voisins GSM-R ok"
l_voisin_Mixte = liste_voisin(l_support_Gsm_mixte, distance)
print "voisins Mixte ok"
l_voisin_unique = set(l_voisin_GsmR) | set(l_voisin_Mixte)
print len(l_voisin_unique)

### CREATION DE LA CARTE ###
map_osm = folium.Map(location=[48.8589, 2.3469], zoom_start=12,
                   tiles='Stamen Toner')
marker_cluster = map_osm

print "Création de la carte en cours"
affichage_support(l_support_GsmR_seuls,"green")
print "Points GsmR ok"
affichage_support(l_support_Gsm_mixte, "blue")
print "Points Mixte ok"
affichage_support(l_voisin_unique, "red")
print "Points Voisin ok"

if departement :
    map_osm.save("inteRfer-Map_"+departement+".html")
else :
    map_osm.save("inteRfer-Map.html")

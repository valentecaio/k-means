##########################################IMPORTS############################
from k_means import *
import matplotlib.pyplot as plt
########################################EXEC#################################

print("################# kmeans ######################")
print("1 - charger les données iris ")
print("2- appliquer kmeans sur des données générée aléatoirement")
print("3- visualiser le comportement de l'aglorithme en 2D")
mode = int(input("choisissez le mode: "))

if mode == 1:
    k_means_iris()
    print ("Verifiez les fichiers iris_centers et iris_results pour voir les resultats de l'appel.")
    #print "le nombre d'erreurs faites est: "+str(nbr_errors(groups))
   
elif mode == 2 :
    nbrPoints = int(input("choisissez le nombre de points: "))
    nbrAttributs = int(input("choisissez le nombre d'attributs de chaque point(la dimension): "))
    nbrClusters = int(input("choisissez le nombre de classes: "))
    k_means(nbrPoints,nbrClusters,nbrAttributs)
    print ("Verifiez les fichiers centroids et results pour voir les resultats de l'appel")
    
elif mode == 3 :
    print("###########################################################")
    
    nbrPoints = int(input("choisissez le nombre de points: "))
    nbrClusters = int(input("choisissez le nombre de classes: "))
    values=k_means(nbrPoints,nbrClusters,2)
    x=[values[i][1] for i in range(len(values))]
    y=[values[i][2] for i in range(len(values))]
   

##########################################IMPORTS############################
from k_means import *
import matplotlib.pyplot as plt

########################################EXEC#################################
def getParameters():
	f = open("parameters.txt",'r')
	lines = f.read().split('\n')

	parameters = {}
	for line in lines:
		# remove spaces to avoid errors
		line = line.replace(' ','')
		
		data = line.split(':')
		if len(data) > 1:
			parameters[data[0]] = int(data[1])
	return parameters
		
if __name__ == '__main__':
	param = getParameters()

	print("################# kmeans ######################")
	print("1 - charger les données iris")
	print("2 - appliquer kmeans sur des données générées aléatoirement")
	print("3 - tester la methode Elbow sur des données aleatoires")
	mode = int(input("choisissez le mode: "))

	if mode == 1:
		points = read_iris_data()
		k_means(points, param['numberOfClusters'], param['maxNumberOfRepetitions'], iris = True)
		print ("Verifiez les fichiers iris_centers et iris_results pour voir les resultats de l'appel.")

	elif mode == 2:
		points = generatepoints(param['numberOfDatas'], param['dataDimension'],	param['minRandomNumber'], param['maxRandomNumber'])
		k_means(points, param['numberOfClusters'], param['maxNumberOfRepetitions'])
		print ("Verifiez les fichiers centroids et results pour voir les resultats de l'appel")
		
	elif mode == 3:
		print("###########################################################")
		points = generatepoints(param['numberOfDatas'], param['dataDimension'])
		elbow(points)

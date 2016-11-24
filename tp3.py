# -*- coding: utf-8 -*-
################################################## IMPORTS #############################################
from random import uniform, randint
from copy import deepcopy

################################################## READ AND WRITE FUNCTIONS #############################################

'''
Loads data from a csv file and returns the corresponding list.
All data are expected to be floats, except in the first column.

@param filename: csv file name.


@return: a list of lists, each list being a row in the data file.
	Rows are returned in the same order as in the file.
	They contains floats, except for the 1st element which is a string
	when the first column is not ignored.
'''
def read_iris_data():
	#same as read_data, modified so it can work ok the iris files
	f = open("irisData.txt",'r')
	data = []
	i = 1
	for line in f:
		line = line.split(",")
		line.pop() #remove the last element in the line wich is a comment
		line = [ float(x) for x in line ]
		line = [i] + line+[-1] #add a column for data index and an other for classification wich take -1 as default value
		i += 1
		data.append(line)
	f.close()
	return data

def write_data(datas, filename, writeCluster = False):
	'''
	Writes data in a csv file.

	@param data: a list of lists

	@param filename: the path of the file in which data is written.
	The file is created if necessary; if it exists, it is overwritten.
	'''
	
	f = open(filename, 'w')
	f.write(';'.join(["# no_obseravtion"]+["attribut_"+str(i+1) for i in range(len(datas[0])-2)]))
	if writeCluster:
		f.write(';'.join(["no_classe"]))
	f.write('\n')
	
	for data in datas:
		f.write(';'.join([repr(data[i]) for i in range(len(data)-1)]))
		if writeCluster:
			f.write(';'.join(repr(data[-1])))
		f.write('\n')
	f.close()

def write_centers(centers, filename):
	'''
	Writes centroids in a csv file
	@param centroids: a hashtable containing the attributs of each center
	@param filename: the path of the file in which data is written.
		The file is created if necessary; if it exists, it is overwritten.
	'''
	f = open(filename,"w")
	f.write(';'.join(["# no_center"]+["attribut_"+str(i+1) for i in range(len(centers[0])-2)]))
	f.write('\n')
	for j in range (len (centers)):
		f.write(';'.join([str(j)]+[repr(centers[j][i]) for i in range (1,len(centers[j])-1)]))
		f.write('\n')
	f.close()



##################################################  FUNCTIONS #############################################



'''
description:
	generates n random points in a specific interval of values
in:
	n is the number of points,
	dimension is the point dimension
out:
	returns a matrix with one point in every line,
	whose the last column is -1,
	the first column is the id of the point,
	and the others columns are his attributs
'''
def generatepoints(n, dimension, min_ = 0, max_ = 1000):
	points = []
	for j in range(n):
		point = [0 for i in range(dimension+2)]
		point[0] = j+1
		for h in range(1,dimension+1):
			point[h] = uniform(min_,max_)
		points.append(point)

	# to begin, all the points are from the group -1
	for i in range(n):
		points[i][-1] = -1

	return points

'''
description:
	chose n random centers from disponible point
in:
	n is the number of centers
	points is the point matrix
out:
	returns a matrix with the chosen centers references
'''
def choseRandomicCenters(n, points):
	nb_objet = len(points)
	centers = []
	i = 0
	while (i<n) :
		new_entry = points[randint(0,nb_objet-1)]

		#verfify if the new line was already chosen
		entry_exist = False
		for j in range(i):
			if new_entry == centers[j]:
				# if the line was already chosen, 
				# stop this loop and continue the other
				# in order to redo the action
				entry_exist = True
				break
		if entry_exist:
			continue

		# only copy point if it wasn't copied before
		i += 1
		centers.append(new_entry)

	# puts group id in points last index
	for i in range(n):
		centers[i][-1] = i

	return centers



'''
description:
	calculate the euclidean distance between two points.
	if the points have differents dimensions,
	the smallest dimension will be considered in the calcul
@param:
	two points
@returns:
	returns the euclidean distance between the two points
'''
def euclideanDistance(point_1,point_2):
	
	dimension = min(len(point_1),len(point_2))
	s = 0
	for i in range (1,dimension):
		s += (point_1[i]-point_2[i])**2
	return s**(0.5)
	'''
	coeff = [0.7826,0.4194,0.9490,0.9565]
	distance = 0
	for i in range(1,len(point_1)-1):
		distance += coeff[i-1]*(point_1[i] - point_2[i])**2
	distance = distance**0.5
	return distance
	'''
def distance_iris(point_1,point_2):
	'''
	computes the euclidian distance taking in consideration the 		iris parametrs
	standardized Euclidean distance
	'''
	
	
	coeff = [0.7826,0.4194,0.9490,0.9565]
	distance = 0
	for i in range(1,len(point_1)-1):
		distance += coeff[i-1]*(point_1[i] - point_2[i])**2
	distance = distance**0.5
	return distance
	

def which_distance(point_1,point_2,iris=False):
	'''
	make a decision to chose which distance we are going to use
	'''
	if iris:
		return distance_iris(point_1,point_2)
	return euclideanDistance(point_1,point_2)

'''
description:
	find the nearest neighbour from a point
@param:
	point, is the observed point
	neighbours, is the neighbours list of the observed point
@return:
	returns the reference of the nearest neighbour
'''
def nearestNeighbour(point, neighbours,iris=False):
	# to begin, the first neighbour is the nearest one
	minDistance = which_distance(point,neighbours[0],iris)
	nearest = neighbours[0]

	for i in range(1,len(neighbours)):
		distance =which_distance(point,neighbours[i],iris)
		if distance < minDistance:
			minDistance = distance
			nearest = neighbours[i]
	return nearest

'''
description:
	agroups points according to theirs nearest centers
@param:
	points, is the points matrix
	centers, is the centers matrix
@return:
	the points matrix is modified
	the function adds the group id in each point last column
	the stop condition to stop classifying
'''
def classificatePoints(points, centers,iris=False):
	No_change=True
	previous_points=deepcopy(points)
	for point in points:
		center = nearestNeighbour(point, centers,iris)
		point[-1] = center[-1]
	if previous_points==points :
		return No_change
	return False
'''
description:
	calculates the barycenter point of a group
@param:
	points, the points matrix
	groupNum, the group index
@return:
	returns the group barycenter point
'''
def barycenter(points, groupNum):
	filtredPoints = pointsOfGroup(points, groupNum)
	
	'''
	# uncomment only to debug
	print('filtering by group', groupNum)
	printMatrix(filtredPoints, str('filtering by group' + str(groupNum)) )
	'''
	tot = len(filtredPoints)
	#the exception of a group with no points
	if tot!=0:
		#dimension ignores the first and the last column
		dimension = len(filtredPoints[0])-2
		bary = [0 for i in range(dimension+1)]
		# ignores the first column (point index)
		
		for k in range(1,dimension+1):
			for i in range(tot):
				bary[k] += filtredPoints[i][k]/tot
	
		# fills the first index with the group id
		for i in range(len(bary)):
			bary[0] = groupNum
	
		return bary
	return points[randint(0,len(points)-1)]
	
'''
description:
	Filters the points matrix by a specific group
@param:
	points, the points matrix
	groupNumber, the group to filter
@return:
	returns a new matrix with the filtred point references
'''
def pointsOfGroup(classifiedPoints, groupNumber):
	filtredPoints = []
	for point in classifiedPoints:
		if point[-1] == groupNumber:
			# copy only the reference
			filtredPoints.append(point)
	return filtredPoints
	
'''
description:
	calculates and returns the barycenters of all groups
@param:
	points, the points matrix
	numberOfCenters, the quantity of available centers
@return:
	returns a new matrix whose each row is a group barycenter
	and the first index of the row is his group id
'''
def calculateBaryCenters(points, numberOfCenters):
	baryCenters = []
	
	for groupNum in range(numberOfCenters):
		bary = barycenter(points, groupNum)
		baryCenters.append(bary)
	return baryCenters
	
'''
description:
	recalculates group centers based on group barycenters
in:
	points, the points matrix
	centers, the centers matrix
out:
	the centers matrix is modified
'''
def updateCenters(points, centers,iris=False):
	numberOfGroups = len(centers)
	baryCenters = calculateBaryCenters(points, numberOfGroups)

	# for each barycenter
	for groupNum in range(numberOfGroups):
		'''
		# filters points by the iteration group number
		# TODO: check if this filter is necessary
		filtredPoints = pointsOfGroup(points, groupNum)
		'''
		# finds the nearestpoint point
		# from the baryCenter of this group
		nearestPoint = nearestNeighbour(baryCenters[groupNum], points,iris)

		# substitutes old center in centers matrix
		centers[groupNum] = nearestPoint

'''
description:
	Prints a matrix, row by row
'''
def printMatrix(mat, title = ''):
	print(title)
	for i in mat:
		print(i)
	print('\n')

################################################## MAIN FUNCTIONS #############################################

'''
description:
	-Read the datas
	-Save those datas in an adequate form
	-Choose 3 random centroids among those datas
	-Classify datas
	-Upload several times centroids and datas by calculating groups barycenters
	-Save datas and centroids in a csv file  
	-Reclassify datas
		@return: updated centrois

	@param: -The datas number 
			-The dimension (number of attributs)
			-The optional iris
	@return:-Centers 

'''
def k_means(points, k, iris = False):
	# TODO: verify this write_data
	fileToWrite = "iris_nonClassifiedDatas.csv" if iris else "nonClassifiedDatas.csv"
	write_data(points, fileToWrite)
	centers = choseRandomicCenters(k, points)
	printMatrix(points, 'points')
	printMatrix(centers, 'centers')
	No_change=False
	i=0
	# if there is no change in datas the classification is done and the algorithms stops
	# also stops if the iterations number reachs the maximum
	while ((not No_change) and i<300):
		No_change=classificatePoints(points, centers)
		printMatrix(points, 'classified points:')

		baryCenters = calculateBaryCenters(points, len(centers))
		printMatrix(baryCenters, 'barycenters:')

		updateCenters(points, centers)
		printMatrix(centers, 'updated centers:')
		i+=1
		
	# writes the results
	fileToWrite = "iris_results.csv" if iris else "results.csv"
	write_data(points, fileToWrite, writeCluster = True)
	fileToWrite = "iris_centers.csv" if iris else "centers.csv"
	write_centers(centers, fileToWrite)

	return points,centers

################################################## Iris Error FUNCTION #############################################
def nbr_errors(points):
	'''
	computes the number of errors on a kmeans algorithm call on iris data
	@param groups : a hashtable containing the number of the point as keys and the correspondant group as values
	@return : the number of errors
	'''
	groups = [-1,-1,-1]
	i = 0
	for tuple in [[0,50],[50,100],[100,150]]:
		c = [0,0,0]
		for k in range(tuple[0], tuple[1]):
			c[points[k][-1]] += 1	
		groups[i] = c.index(max(c))
		i += 1
	
	
	
	a=0
	b=0
	d=0	
	
	
	error = 0
	for point in points :
		if point[0]<=50 :
			if point[-1] == groups[0] :
				a+=1
			elif point[-1] == groups[1] :
				b+=1
				error+=1
			else :
				d+=1
				error+=1
				
		if point[0]>50 and point[0]<=100:
			if point[-1] == groups[0] :
				a+=1
				error+=1
			elif point[-1] == groups[1] :
				b+=1
			else:
				d+=1
				error+=1
				
		if point[0]>100 and point[0]<=150:
			if point[-1] == groups[0] :
				a+=1
				error+=1
			elif point[-1] == groups[1] :
				b+=1
				error+=1
			else:
				d+=1
				
	print("Nous obtenons des groupes de: ",a,b,d,groups)
	print("Le nombre d'erreurs est: ",error)
	return error

################################################## Iris TESTS (Elbow method) #############################################

def variance(data,centers):
	'''
	computes the sum of squared error of a kmeans call
	'''
	V = 0
	groupsNumber=len(centers)
	for i in range (groupsNumber):
		partition=pointsOfGroup(data,i)
		for point in partition :
			dist = euclideanDistance(point,centers[i])
			V += (dist)**2
		return V

def elbow(data):
	'''
	draws the elbow graph of 9 kmeans call for k from 2 to 9
	'''
	import matplotlib.pyplot as plt
	
	Vsums = []
	for k in range(2,10):
		print(k)
		centers = k_means(data, k, iris = True)
		Vsums.append(variance(data,centers))
	ks =[i for i in range(2,10)]
	plt.xlabel("nombres de groupes")
	plt.ylabel("variance")
	plt.plot(ks,Vsums)
	plt.scatter(ks,Vsums)
	plt.show()


#elbow(generatepoints(400,4))
points = read_iris_data()
#elbow(points)


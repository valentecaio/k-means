from random import uniform, randint
from copy import deepcopy

'''
description:

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
    returns a matrix with one center point in each row
'''
def choseRandomicCenters(n, points):
	nb_objet = len(points)
	centers = []
	i = 0
	while (i<n) :
		new_entry = deepcopy(points[randint(0,nb_objet-1)])

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

	for i in range(n):
		# remove last element, because centers
        # doesn't have nearests-centers
		centers[i][-1] = i
	return centers

def read_data(filename, skip_first_line=False, ignore_first_column=False):
	'''
    Loads data from a csv file and returns the corresponding list.
    All data are expected to be floats, except in the first column.

    @param filename: csv file name.

    @param skip_first_line: if True, the first line is not read.
        Default value: False.

@param ignore_first_column: if True, the first column is ignored.
        Default value: False.

    @return: a list of lists, each list being a row in the data file.
        Rows are returned in the same order as in the file.
        They contains floats, except for the 1st element which is a string
        when the first column is not ignored.
    '''

	f = open(filename, 'r')
	if skip_first_line:
		f.readline()

	data = []
	for line in f:
		line = line.split(",")
		line[1:] = [float(x) for x in line[1:]]
		if ignore_first_column:
			line = line[1:]
		data.append(line)
	f.close()
	return data


def write_data(data, filename):
    '''
    Writes data in a csv file.

    @param data: a list of lists

    @param filename: the path of the file in which data is written.
    The file is created if necessary; if it exists, it is overwritten.
    '''
    # If you're curious, look at python's module csv instead, which offers
    # more powerful means to write (and read!) csv files.
    f = open(filename, 'w')
    for item in data:
        f.write(','.join([repr(x) for x in item]))
        f.write('\n')
    f.close()

'''
description:
	calculate the euclidean distance between two points.
	if the points have differents dimensions,
	the smallest dimension will be considered in the calcul
in:
	two points
out:
	returns the euclidean distance between the two points
'''
def euclideanDistance(point_1,point_2):
	dimension = min(len(point_1),len(point_2))
	s = 0
	for i in range (1,dimension):
		s += (point_1[i]-point_2[i])**2
	return s**0.5

'''
description:
	find the nearest neighbour from a point
in:
	point, is the observed point
	neighbours, is the neighbours list of the observed point
out:
	returns the reference of the nearest neighbour
'''
def nearestNeighbour(point, neighbours):
	# to begin, the first neighbour is the nearest one
	minDistance = euclideanDistance(point, neighbours[0])
	nearest = neighbours[0]

	for i in range(1,len(neighbours)):
		distance = euclideanDistance(point, neighbours[i])
		if distance < minDistance:
			minDistance = distance
			nearest = neighbours[i]
	return nearest

'''
description:
	group points according to theirs nearest centers
in:
	points, is the points matrix
	centers, is the centers matrix
out:
	the points matrix is modified
	the function adds the group id in each point last column
'''
def classificatePoints(points, centers):
	for point in points:
		center = nearestNeighbour(point, centers)
		point[-1] = center[-1]

'''
description:
	calculates the barycenter point of a group
in:
	points, the points matrix
	groupNum, the group index
out:
	returns the group barycenter point
'''
def barycenter(points, groupNum):
	filtredPoints = pointsOfGroup(points, groupNum)
	'''
	# uncomment only to debug
	print('filtering by group', groupNum)
	printMatrix(filtredPoints)
	'''
	tot = len(filtredPoints)
	dimension = len(filtredPoints[0])-1
	bary = [0 for i in range(dimension)]
	# ignores the first column (point index)
	# TODO: check this matemagic
	for k in range(1,dimension):
		for i in range(tot):
			bary[k] += filtredPoints[i][k]/tot

	# fills the first index with the group id
	for i in range(len(bary)):
		bary[0] = groupNum

	return bary

'''
description:
	Filters the points matrix by a specific group
in:
	points, the points matrix
	groupNumber, the group to filter
out:
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
in:
	points, the points matrix
	numberOfCenters, the quantity of available centers
out:
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
def updateCenters(points, centers):
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
		nearestPoint = nearestNeighbour(baryCenters[groupNum], points)

		# substitutes old center in the centers matrix
		centers[groupNum] = nearestPoint

'''
description:
	Prints a matrix, row by row
'''
def printMatrix(mat):
	for i in mat:
		print(i)
	print('\n')


'''
description:

in:

out:

'''
def k_means(points, k):
	centers = choseRandomicCenters(k, points)
	print('centers:')
	printMatrix(centers)

	for i in range(10):
		classificatePoints(points, centers)
		print('classified points:')
		printMatrix(points)

		baryCenters = calculateBaryCenters(points, len(centers))
		print('barycenters:')
		#printMatrix(baryCenters)

		updateCenters(points, centers)
		print('updated centers:')
		printMatrix(centers)


points = generatepoints(100, 2, max_ = 1000)
print('points:')
printMatrix(points)

k_means(points, 5)



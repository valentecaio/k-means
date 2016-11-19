from random import uniform, randint
from copy import deepcopy

'''
description:

in:
    n is the number of points,
    dimension is the point dimension
out:
    a matrix with one point in every line,
    where the last column is zero,
    the first column is the id of the point,
    and the others columns are his attributs
'''
def generatepoints(n,dimension, min_ = 0, max_ = 100):
	tab = []
	for j in range(n):
		sub_tab = [0 for i in range(dimension+2)]
		'''here new''' # diff
		sub_tab[0] = j+1
		for h in range(1,dimension+1):
			sub_tab[h] = uniform(min_,max_)
		tab.append(sub_tab)
	return tab

'''
description:
	chose n random centers from disponible point
in:
    n is the number of centers
    tab_obj is the point matrix
out:
    a matrix with one center point in every line
'''
def choseRandomicCenters(n, tab_obj):
	nb_objet = len(tab_obj)
	tab_center = []
	i = 0
	while (i<n) :
		new_entry = deepcopy(tab_obj[randint(0,nb_objet-1)])

		#verfify if the new line was already chosen
		entry_exist = False
		for j in range(i):
			if new_entry == tab_center[j]:
				# if the line was already chosen, 
				# stop this loop and continue the other
                # in order to redo the action
				entry_exist = True
				break
		if entry_exist:
			continue

		# only copy point if it wasn't copied before
		i += 1
		tab_center.append(new_entry)

	for i in range(n):
        # recalculate id
		tab_center[i][0] = i+1
        # remove last element, because centers
        # doesn't have nearests-centers
		tab_center[i].pop()
	return tab_center

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
	the euclidean distance between the two points
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
	the minimum distance found and
	the reference of the nearest neighbour
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
	return minDistance, nearest

'''
description:
	group points according to theirs nearest centers
in:
	points, is the points matrix
	centers, is the centers matrix
out:
	add the group id in each point last column
'''
def classification(points, centers):
	for point in points:
		distance, center = nearestNeighbour(point, centers)
		point[-1] = center[0]

'''
description:

in:

out:

'''
def barycenter(points):
	tot = len(points)
	barycenter = [0 for i in range (len(points[0]))]
	# ignore the first column (point index)
	# and the last (group index)
	for k in range (1,len(points[0])-1):
		for i in range (tot):
			barycenter[k] += points[i][k]/tot
	
	return barycenter 
	
'''
description:

in:

out:

'''
def pointsOfGroup(classifiedpoints, groupNumber):
	tab = []
	for point in classifiedpoints:
		if point[-1] == groupNumber:
			tab.append(point)
	return tab
	
'''
description:

in:

out:

'''
def barycenters(classifiedpoints, centers):
	barycenters = []
	
	for groupNum in range(1,len(centers)+1):
		tab = pointsOfGroup(classifiedpoints, groupNum)

		baryCenter = barycenter(tab)
		baryCenter[0] = groupNum
		barycenters.append(baryCenter)
	return barycenters
	
'''
description:

in:

out:

'''
def updateCenters(classifiedpoints,centers):
	baryCenters = barycenters(classifiedpoints, centers)
	#printMatrix(baryCenters)
	newCenters = []
	for i in range (1,len(baryCenters)+1):
		tab = pointsOfGroup(classifiedpoints, i)
		a,nearestpoint = nearestNeighbour(baryCenters[i-1],tab)
		
		nearestpoint[0] = i
		nearestpoint.pop()
		newCenters.append(nearestpoint)
	#printMatrix(newCenters)
	return newCenters

'''
description:

in:

out:

'''
def printMatrix(points):
	for i in points:
		print(i)
	print('\n')


'''
description:

in:

out:

'''
def k_means(points,k):
	centers = choseRandomicCenters(k,points)
	
	
	for i in range(3):
		classification(points, centers)
	
		centers = updateCenters(points,centers)
		print(centers)
		
		
	
	


points = generatepoints(10,2)
print('points:')
printMatrix(points)

centers = choseRandomicCenters(3,points)
print('centers:')
printMatrix(centers)

classification(points, centers)
print('classified points:')
printMatrix(points)

centers = updateCenters(points,centers)
print('updated centers:')
printMatrix(centers)

classification(points, centers)
print('classified points:')
printMatrix(points)

centers = updateCenters(points,centers)
print('updated centers:')
printMatrix(centers)

classification(points, centers)
print('classified points:')
printMatrix(points)



'''
for i in center:
	print i	

dist = euclideanDistance(point[2],point[1])
print dist'''

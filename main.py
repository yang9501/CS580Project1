import numpy as np
from copy import copy, deepcopy

def generateArray(n, k):
	return np.random.randint(0,2, size=(n,k))

def reverseNumber(x):
	if x == 0:
		return 1
	elif x == 1:
		return 0

def objective(n, k, array):
	missingCombinations = 0
	for x in range(k) :
		for y in range(x, k):
			if(x == y):
				continue
			#walk down the column and compare the combinations and find out how many are missing.
			allCombinations = {(0,0): 0, (0,1): 0, (1,0): 0, (1,1): 0}  
			#print(allCombinations)
			#Counts the number of combinations per pair value
			for z in range(n):
				#print((array[:,x][z], array[:,y][z]))
				if (array[:,x][z], array[:,y][z]) in allCombinations.keys():
					allCombinations[(array[:,x][z], array[:,y][z])] += 1
				
			#print(allCombinations)
			#Counts the number of missed combinations
			for i in allCombinations.values():
				if i==0:
					missingCombinations += 1
			#print(missingCombinations)
			#print("---------")
	#print("Total missing combinations for this array: " + str(missingCombinations))
	return missingCombinations

def neighborhood(n, k, array):
	randColumnIndex = np.random.randint(0, k)
	#print ("Random column index:" + str(randColumnIndex))
	column = array[:,randColumnIndex]
	#print(column)
	#GENERATE NEIGHBORS
	neighborhoodArray = []
	for x in range(n):
		neighbor = deepcopy(array)
		#print(neighbor[:,randColumnIndex])
		neighbor[x][randColumnIndex] = reverseNumber(neighbor[x][randColumnIndex])
		#print(neighbor[:,randColumnIndex])
		neighborhoodArray.append(neighbor)
		#print("---------")
	return neighborhoodArray

def analyze(n, k, mainArray, neighbors):
	mainArrayObjective = objective(n, k, mainArray)
	neighborsObjective = []
	for i in range(len(neighbors)):
		neighborsObjective.append(objective(n, k, neighbors[i]))
		print(neighbors[i])
		print(objective(n,k,neighbors[i]))
		print("-------------")
	print(mainArrayObjective)
	print(neighborsObjective)
	#THE index of a neighbor array corresponds to the objective index of neighborsObjective.  That is, neighborsObjective[i] == objective(n,k,neighbors[i])

#set k here
k = 5
n = 5
temperature = k
initialStateArray = generateArray(n, k)
print (initialStateArray)
neighbors = neighborhood(n, k, initialStateArray)
#print (neighbors)
#####I AM HERE RIGHT NOW.  OBJECTIVE AND NEIGHBOR BOTH WORK, MAYBE NOT FOR ALL EDGE CASES FOR VALUES. NEED TO TEST FOR N.  NEED TO WRITE CODE TO USE OBJECTIVE TO EVALUATE EACH NEIGHBOR
analyze(n, k, initialStateArray, neighbors)

#TODO: Figure out how to get the value of N.  Watch the sudoku simulated annealing video
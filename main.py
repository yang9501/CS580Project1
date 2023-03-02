import numpy as np
from copy import copy, deepcopy
from math import comb
import math

def generateArray(n, k):
	return np.random.randint(0,2, size=(n,k))

def reverseNumber(x):
	if x == 0:
		return 1
	elif x == 1:
		return 0

#Returns the number of missing combinations for an array
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
		#print(neighbors[i])
		#print(objective(n,k,neighbors[i]))
		#print("-------------")
	#print(mainArrayObjective)
	#print(neighborsObjective)
	#THE index of a neighbor array corresponds to the index of neighborsObjective.  
	#That is, neighborsObjective[i] == objective(n,k,neighbors[i])
	#pick and return lowest value
	minimumIndex = neighborsObjective.index(min(neighborsObjective))
	#print(minimumIndex)
	return neighbors[minimumIndex]

def simulatedAnnealing(maxIterations, temperature, k, n ,v, t, initialArray, frozenFactor): 
	currentArray = initialArray
	stagnationCounter = 0

	#TODO: Figure out how to get the value of N.  Watch the sudoku simulated annealing video
	print("frozenFactor: " + str(frozenFactor))
	for i in range(maxIterations):
		print(currentArray)
		print(objective(n, k, currentArray))
		if objective(n, k, currentArray) == 0:
			print("FOUND OBJECTIVE")
			return currentArray
		if temperature == 0:
			print("TEMPERATURE REACHED")
			return currentArray
		if frozenFactor == stagnationCounter:
			print("FROZEN FACTOR REACHED")
			return currentArray

		neighbors = neighborhood(n, k, currentArray)
		#print (neighbors)
		
		#retrieve best neighbor array with the lowest objective score
		bestNeighborArray = analyze(n, k, currentArray, neighbors)

		#Determine whether the neighbor is better than the current
		deltaE = objective(n, k, bestNeighborArray) - objective(n, k, currentArray)
		#print("objective currentArray: " + str(objective(n, k, currentArray)))
		#print("objective bestNeighborArray: " + str(objective(n, k , bestNeighborArray)))
		#print("deltaE: " + str(deltaE))
		if deltaE < 0: #If the value of the lowest objective score neighbor is lower than the current score
			#print("Adopting neighbor, who has lower cost")
			currentArray = bestNeighborArray
			stagnationCounter = 0
		else:
			print("temperature: " + str(temperature))
			acceptProbability = np.exp(-deltaE/temperature)   #####THIS IS PROBABLY THE SOURCE OF THE ISSUES!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			#print("acceptProbability: " + str(acceptProbability))
			randomSeed = np.random.uniform(1,0,1)
			#print("randomSeed: " + str(randomSeed))
			if randomSeed < acceptProbability:
				#print("Adopting neighbor through probability")
				currentArray = bestNeighborArray
			else:
				stagnationCounter+=1

		#reduce temperature
		temperature = temperature * coolingFactor
		#print("---------------")

	print ("MAX ITERATIONS REACHED")
	return currentArray

#set k here
k = 5
n = 5
v = 2
t = 2

temperature = k
maxIterations = 100000
frozenFactor = (v**t) * comb(k, t) #number of iterations threshold where best-so-far objective score has not improved
coolingFactor = 0.99

initialArray = generateArray(n, k)
print (initialArray)

print(simulatedAnnealing(maxIterations, temperature, k, n, v, t, initialArray, frozenFactor))

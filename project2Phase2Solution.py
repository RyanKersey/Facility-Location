#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 16:43:51 2024

@author: sriram
"""

# CS1210: Project 2 Phase 1 [5 functions to complete]
###############################################################################
# Complete the signed() function, certifying that:
# 1) the code below is entirely your work, and
# 2) it has not been shared with anyone outside the instructional team.
#
# ToDo: Change the words "hawkid" between the two double quote marks
# to match your own hawkid. Your hawkid is the "login identifier" you use
# to login to all University services, like `https://myUI.uiowa.edu/'
#
#
# Note: we are not asking for your password, just the login
# identifiers: for example, mine is "sriram".
#
###############################################################################
def signed():
    return(["hawkid"])


###############################################################################
#
# Specification: This "helper" function extracts the city name and state name
# from the given "city line" and returns these, concatenated in the correct
# format, as a single string.
#
###############################################################################
def extractCityStateNames(line):
    pieces = line.split(",")
    return pieces[0] + pieces[1][:3]

###############################################################################
#
# Specification: This "helper" function extracts the latitude and longitude
# from the given "city line" and returns these, in a size-2 list of integers.
#
###############################################################################
def extractCoordinates(line):
    pieces = line.split(",")
    return [int(pieces[1].split("[")[1]), int(pieces[2].split("]")[0])]


###############################################################################
#
# Specification: This "helper" function extracts the city population
# from the given "city line" and returns this an an integer.
# 
###############################################################################
def extractPopulation(line):
    pieces = line.split(",")
    return int(pieces[2].split("]")[1])


###############################################################################
#
# Specification: Reads information from the files "miles.txt" and loads all the 
# data from the file into a giant dictionary and returns this dictionary. The 
# organization of this dictionary has been specified in detail in the Project 2 handout. 
# If, for some reason, "miles.txt" is missing, your function should gracefully
# finish, returning the empty dictionary {}.
# 
###############################################################################
def loadData():
    f = open("miles.txt")
    
    # The dictionary that will hold all the city information
    cityDataDict = {}
    
    # Tracks which city we are currently processing
    cityIndex = 0
    
    # Keeps track of the list of all city/state names
    cityStateNamesList = []
    
    # Reads from the file, one line at a time
    for line in f:
        
        # Checks if the line is a "city line", i.e., contains information about
        # the city
        if line[0].isalpha():
                            
            cityStateName = extractCityStateNames(line)
            coords = extractCoordinates(line)
            pop = extractPopulation(line)         
            cityDataDict[cityStateName] = [coords, pop, {}]            
            cityStateNamesList.append(cityStateName)
            index = -2
            cityIndex = cityIndex + 1
        
        # Checks if the line is a "distance line", i.e., contains information
        # distances from this city to previous cities            
        elif line[0].isdigit():
            distancesInThisLine = [int(x) for x in line.split()]
            
            for i in range(len(distancesInThisLine)):
                destinationCity = cityStateNamesList[index]
                index = index - 1
                cityDataDict[cityStateName][2][destinationCity] = distancesInThisLine[i]
                cityDataDict[destinationCity][2][cityStateName] = distancesInThisLine[i]
            
    
    return cityDataDict
            
###############################################################################
#
# Specification: takes the dictionary that contains all the information associated 
# with the cities and a particular city name and returns the coordinates (which is a 
# list of 2 integers) of the given city. If, for some reason, cityName is not a key
# in cityDataDict, it returns None.
#
###############################################################################
def getCoordinates(cityDataDict, cityName):
    if cityName in cityDataDict:
        return cityDataDict[cityName][0]
    else:
        return None

###############################################################################
#
# Specification: takes the dictionary that contains all the information associated 
# with the cities and a particular city name and returns the population (which is a 
# positive integer) of the given city. If, for some reason, cityName is not a key
# in cityDataDict, it returns None.
#
###############################################################################
def getPopulation(cityDataDict, cityName):
    if cityName in cityDataDict:
        return cityDataDict[cityName][1]  
    else:
        return None

###############################################################################
#
# Specification: takes the dictionary that contains all the information associated 
# with the cities and two city names and returns the distance (an integer) 
# between cities cityName1 and cityName2. If cityName1 and cityName2 are identical, 
# it returns 0. If either cityName1 or cityName2 are not in cityDataDict, it returns
# None.
#
###############################################################################    
def getDistance(cityDataDict, cityName1, cityName2):
    if (cityName1 in cityDataDict) and (cityName2 in cityDataDict):
        if (cityName1 != cityName2):
            return cityDataDict[cityName1][2][cityName2]
        else:
            return 0
    else:
        return None

###############################################################################
#
# Specification: The function takes 3 paramaters:
#    
# cityDataDict: the dictionary that contains all the information associated 
# with the cities
# 
# cityName: is a name of a city
#
# r: is a non-negative floating point number
#
# The function returns a list of cities at distance at most r from the given city,
# cityName. This list can contain the names of cities in any order. If cityName is
# not a key in cityDataDict, the function should return None.
#
###############################################################################
def nearbyCities(cityDataDict, cityName, r):
    if cityName not in cityDataDict:
        return None
    
    nearbyCityList = [cityName]
    for city in cityDataDict:
        if (city != cityName) and (cityDataDict[cityName][2][city] <= r):
            nearbyCityList.append(city)

    return nearbyCityList


###############################################################################
#
# Specification: returns the number of unserved cities within distance r of city. 
# This number includes city itself, it has not been served.
# served is a boolean list indicating which cities have been served. CityList is
# the list of city names.
# 
###############################################################################
def numNotserved(served, cityDataDictionary, name, r) :    
    allCitySet = set(cityDataDictionary.keys())
    notServedSet = allCitySet - served
    return len(notServedSet & set(nearbyCities(cityDataDictionary, name, r)))


###############################################################################
#
# Specification: Returns the name of the city that can serve the most as-yet-unserved 
# cities within radius r. Returns None if all cities are already served. If there is a tie,
# this function returns the city that appears earliest in alphabetical order. 
# 
###############################################################################
def nextFacility(served, cityDataDictionary, r) :

    facility = None      # Name of city that will be the next service facility
    numberServed = 0     # Number of cities that facility will serve

    cityList = sorted(list(cityDataDictionary.keys()))

    # For each city
    for c in cityList:
        # compute how many unserved cities will be served by city c
        willBeServed = numNotserved(served, cityDataDictionary, c, r)
        if (willBeServed > 0):
            print(c, willBeServed)
        
        # if it can serve more cities than the previous best city
        if willBeServed >  numberServed:
            # make it the service center
            facility = c
            numberServed = willBeServed
            
    print("**********************")
    print("Picked: ", facility)
    print("**********************")
    
    return facility


###############################################################################
#
# Implements the greedy algorithm to find a set of facilities such that all
# cities are with r units of the selected facilities. In the greedy step, where
# a city that serves the maximum number of as-yet-unserved cities is selected,
# ties are broken in favor of the city that comes alphabetically first.
# 
###############################################################################
def greedyFacilitySet(cityDataDictionary, r) :
    print("**********************")
    
    # Set of cities that are served by current facilities
    served = set()

    # List of cities that are at which facilities are located
    facilities = []

    # Get the city that is the next best service facility
    facility = nextFacility(served, cityDataDictionary, r )

    # While there are more cities to be served
    while facility :

        # Mark each city as served that will be served by this facility
        newlyServed = set(nearbyCities(cityDataDictionary, facility, r))
        served |= newlyServed

        # Append the city to the list of service facilities
        facilities.append(facility)

        # Get the city that is the next best service facility
        facility = nextFacility(served, cityDataDictionary, r)

    return facilities

###############################################################################
#
# Helper function that returns True if the facilityList contains a collection
# of cities such all 128 cities are served by these facilities with radius of
# coverage r. Returns False otherwise.
# 
###############################################################################
def feasible(cityDataDictionary, facilityList, r):
    coveredCities = set()
    for cityName in facilityList:
        coveredCities |= set(nearbyCities(cityDataDictionary, cityName, r))
        
    return len(coveredCities) == 128

###############################################################################
#
# Helper function that scans a list in which each element is a list of
# facilities. Returns the first list of facilities that is feasible. Returns
# the empty list, if no list of facilities is feasible. 
# 
###############################################################################
def firstFeasible(cityDataDictionary, listFacilityLists, r):
    for facilityList in listFacilityLists:
        if feasible(cityDataDictionary, facilityList, r):
            return facilityList
    return []

###############################################################################
#
# Recursive brute-force helper function that generates subsets of facilities
# of size k or less from cityList and returns the first feasible set of facilities
# that it generates. 
# 
###############################################################################
def bruteForceFacilityLocation(cityDataDictionary, cityList, r, k):
    
    # Base cases
    if k == 0:
        return [[], [[]]]
    
    if len(cityList) == k:
        if feasible(cityDataDictionary, cityList, r):
            return [cityList, [cityList]]
        else:
            return [[], [cityList]]
    
    # Recursive case
    L = bruteForceFacilityLocation(cityDataDictionary, cityList[1:], r, k-1)
    if L[0] != []:
        return L
    else:
        L[1] = [[cityList[0]] + elem for elem in L[1]]
        L[0] = firstFeasible(cityDataDictionary, L[1], r)
        if L[0] != []:
            return L
        
    LL = bruteForceFacilityLocation(cityDataDictionary, cityList[1:], r, k)
    if LL[0] != []:
        return LL
    else:
        L[1].extend(LL[1])
        return L
    
###############################################################################
#
# Returns an optimal solution to the facility location problem, if there is a solution
# of size len(oneSolution)-1 or less. Otherwise, returns the empty list.
# 
###############################################################################
def optimalFacilitySet(cityDataDictionary, r, oneSolution):
    cityList = list(cityDataDictionary.keys())
    return bruteForceFacilityLocation(cityDataDictionary, cityList, r, len(oneSolution)-1)[0]

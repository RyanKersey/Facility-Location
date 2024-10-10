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
    return(["kersey"])

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
    try:
        dataDict = {}
        distances = []
        lastCity = ""
        f = open("miles.txt",'r')
        lineCount = 0
        
        for line in f:
            if lineCount > 3:
                if not line[0].isdigit():
                    city,numbers = line.split('[')
                    city = city.replace(',','')
                    if lineCount == 4:
                        lastCity = city
                    
                    locationPart,population = numbers.split(']')
                    location = locationPart.split(',')
                    dataDict[city] = [[int(location[0]),int(location[1])],int(population)]
                    
                    dataDict[lastCity].append(distances)
                    lastCity = city
                    distances = []
                else:
                    distances.extend(line.split())
            lineCount += 1
        return dataDict
            
    except FileNotFoundError:
        print("Error")
        return {}
    except ValueError:
        dataDict[lastCity].append(distances)
        return dataDict
    
###############################################################################
#
# Specification: takes the dictionary that contains all the information associated 
# with the cities and a particular city name and returns the coordinates (which is a 
# list of 2 integers) of the given city. If, for some reason, cityName is not a key
# in cityDataDict, it returns None.
#
###############################################################################
def getCoordinates(cityDataDict, cityName):
    try:
        return cityDataDict[cityName][0]
    except:
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
    try:
        return cityDataDict[cityName][1]
    except:
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
    if cityName1 == cityName2:
        return 0
    try: 
        keyList = list(cityDataDict.keys())
        index1 = keyList.index(cityName1)
        index2 = keyList.index(cityName2)
        if index1 > index2:
            index = index2
            fartherInDict = cityName1
        else:
            index = index1
            fartherInDict = cityName2

        return int(cityDataDict[fartherInDict][2][abs(index1-index2)-1])
    except:
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
    try:
        nearbyCitiesList = []
        distanceList = []
        keyList = list(cityDataDict.keys())
        index = keyList.index(cityName)
        for x in keyList:
            if getDistance(cityDataDict, cityName, x) <= r:
                nearbyCitiesList.append(x)
    
        return nearbyCitiesList
    except:
        return None

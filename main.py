from ortools.algorithms import pywrapknapsack_solver
import os
import random
import pandas as pd
import time

def getDataFromTest(fileDir):
    test = [int(x) for x in open(fileDir).read().split()]
    n = test[0]
    test.pop(0)
    capacities = [test[0]]
    test.pop(0)
    values = []
    weights = []
    for _ in range(n):     
        values.append(test[0])
        weights.append(test[1])
        test.pop(0)
        test.pop(0)
    return values, [weights], capacities

TIME_LIMIT = 3
timeStamp = 0
def solve(fileDir):
    timeStamp += 1
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    
    values, weights, capacities = getDataFromTest(fileDir)
    solver.Init(values, weights, capacities)
    solver.set_time_limit(TIME_LIMIT)
    timeBegin = time.time()
    computed_value = solver.Solve()
    timeEnd = time.time()
    timeToRun = timeEnd - timeBegin
    total_weight = 0
    print('Current: ', timeStamp)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            total_weight += weights[0][i]
    return str(computed_value), str(total_weight), str(capacities[0]), str(timeToRun), str(timeEnd-timeBegin<TIME_LIMIT)

def chooseTestCases():
    # get all test group name
    cwd = os.getcwd()
    testDir = os.path.join(cwd, "test/kplib")
    testGroupList = [dir for dir in os.listdir(testDir) if os.path.isdir(os.path.join(testDir, dir))]

    # For each group of test case: try all test size
    chosenTests = []
    for testGroup in testGroupList:
        currentTests = []
        testGroupDir = os.path.join(testDir, testGroup)
        for nSize in os.listdir(testGroupDir):
            allTest = []
            testSizeDir = os.path.join(testGroupDir, nSize)
            for root, dir, files in os.walk(testSizeDir):
                for file in files:
                    allTest.append(os.path.join(root, file))
            currentTests.append(random.choice(allTest))
        chosenTests.append(currentTests)
    chosenTest = "chosentest.txt"
    chosenTestFile = open(chosenTest, "w")
    content = ""
    for group in chosenTests:
        for test in group:
            content += str(test) + '\n'
    chosenTestFile.write(content)
    chosenTestFile.close()    

from collections import defaultdict
if __name__ == '__main__':
    if not os.path.exists("chosentest.txt"):
        chooseTestCases()   
    testFile = open("chosentest.txt", "r")
    testList = [line.strip() for line in testFile.readlines()]
    testDict = defaultdict(list)
    for test in testList:
        testName = '/'.join(test.split('/')[-4:])
        value, weight, capacity, timeToRun, optimal = solve(test)
        testDict['TestName'].append(testName)
        testDict['Value'].append(value)
        testDict['Weight'].append(weight)
        testDict['Capacity'].append(capacity)
        testDict['Time to run'].append(timeToRun)
        testDict['Optimal'].append(optimal)
    testDataFrame = pd.DataFrame(testDict)
    testDataFrame.to_csv('testResult.csv')
from ortools.algorithms import pywrapknapsack_solver


def getDataFromTest():
    test = [int(x) for x in open("test/kplib/00Uncorrelated/n00050/R01000/s006.kp").read().split()]
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

def main():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')
    
    values, weights, capacities = getDataFromTest()
    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()
    packed_items = []
    packed_weights = []
    total_weight = 0
    print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    print('Total weight:', total_weight)
    print('Packed items:', packed_items)
    print('Packed_weights:', packed_weights)


if __name__ == '__main__':
    main()
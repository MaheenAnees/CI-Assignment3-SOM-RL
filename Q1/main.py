import random
from valueIterationAgent import *
def createGrid(x,y):
    grid = []
    for j in range(x):
        temp = []
        for i in range(y):
            temp.append(0)
        grid.append(temp)    
    for i in range(x):
        for j in range(y):
            p = random.random()
            if p <= 0.1:
                grid[i][j] = -100
            else:
                grid[i][j] = -1
    rewardPosX = random.randint(0, x - 1)
    rewardPosY = random.randint(0, y - 1)
    grid[rewardPosX][rewardPosY] = 100    
    return grid

grid = createGrid(20,20)
agent = ValueIteration(0.9, 0.1, grid)
policy, iterations = agent.findPolicy()
for i in policy:
    print(i)
print('Total iterations:', iterations)
agent.visualizePolicy(policy)
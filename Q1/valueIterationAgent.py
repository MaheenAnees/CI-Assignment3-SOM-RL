import math
import numpy as np 
import copy
import random
from PIL import Image, ImageDraw

class ValueIteration:
    def __init__(self, discountFactor, theta, reward_ = None):
        if reward_ != None:
            self.reward=  reward_
        else:
            self.reward = [[-1 for i in range(10)],
                [-1 for i in range(10)],
                [-1,-1,-1,-1,-100,-100,-100,-100,-1,-100],
                [-1 for i in range(10)],
                [-1 for i in range(10)],
                [-1 for i in range(10)],
                [-1,-1,-100, -1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-100,-100,-1,-1,-100,-100,-100,-1],
                [-1,-1,-100, -1,-1,-1,-1,-1,-1,-1],
                [-1,-1,-100,-100,-100,-100,-100,-100,-100,100]]
        self.discountFactor = discountFactor
        self.theta = theta
        self.dimension = (len(self.reward), len(self.reward[1]))
        self.values = copy.deepcopy(self.reward)
        self.Moves = {'Right' : 0, 'Left' : 1, 'Up':2, 'Down': 3}
    
    def returnStates(self):
        states = []
        for i in range(self.dimension[0]):
            for j in range(self.dimension[1]):
                states.append((i,j))
        return states
    
    def findPolicy(self):
        iterations = 0
        states = self.returnStates()
        policy = copy.deepcopy(self.reward)
        convergence = math.inf

        while convergence >= self.theta:
            convergence = 0
            iterations += 1
            for i, j in states:
                if self.reward[i][j] == -1:
                    val = self.values[i][j]
                    lst = []
                    if i != (self.dimension[1] - 1):
                        lst.append((self.reward[i][j] + self.discountFactor*self.values[i+1][j] , self.Moves['Down']))
                    if i != 0:
                        lst.append((self.reward[i][j] + self.discountFactor*self.values[i-1][j], self.Moves['Up'])) 
                    if j != 0:
                        lst.append((self.reward[i][j] + self.discountFactor*self.values[i][j-1], self.Moves['Left']))
                    if j != (self.dimension[1] - 1):
                        lst.append((self.reward[i][j] + self.discountFactor*self.values[i][j+1], self.Moves['Right']))
                    self.values[i][j] = max(lst)[0]
                    policy[i][j] = max(lst)[1]
                    convergence = max([convergence , np.abs(val - self.values[i][j])])
        return policy, iterations
    
    def visualizePolicy(self,policy):
        height = (self.dimension[0]*100)//2
        width = (self.dimension[1]*100)//2
        image = Image.new(mode='RGB', size=(height, width), color='#FFFFFF')
        dim = len(policy)
        step = int(image.width / dim)
        draw = ImageDraw.Draw(image)
        arrow = Image.open("arrow.jpg").convert("RGBA")
        arrow = arrow.resize((step, step))        
        for i in range(dim):
            for j in range(dim):
                if policy[i][j] == 100:
                    draw.rectangle([(j*step,i*step),((j+1)*step,(i+1)*step)],fill="green")
                elif policy[i][j] == -100:
                    draw.rectangle([(j*step,i*step),((j+1)*step,(i+1)*step)],fill="red")
                elif policy[i][j] == 2:
                    image.paste(arrow.rotate(90), (j*step, i*step), arrow.rotate(90))
                elif policy[i][j] == 3:
                    image.paste(arrow.rotate(270), (j*step, i*step), arrow.rotate(270))
                elif policy[i][j] == 1:
                    image.paste(arrow.rotate(180), (j*step, i*step), arrow.rotate(180))
                elif policy[i][j] == 0:
                    image.paste(arrow.rotate(0), (j*step, i*step), arrow.rotate(0))   
        image.save('result.png')
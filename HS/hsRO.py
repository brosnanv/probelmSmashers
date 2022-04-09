
import random as _r_
import numpy as np
from timeit import default_timer as timer


''''


This is an intended improvement to Harmony search by having the harmoy initialisation 
be done with ro selction rather than the initially proposed random selection

Brosnanv code a2 harmony search 
'''





## Harmonic memory consideration rate -HMCR 
## PAR the probability of randomly shifting a note up or down once it has been fixed



def harmony_search(prob, iterations=5000, HMS=100, HCR=.6, PAR=.2):
    start = timer()
    HM = HarmonyMemory(prob, HMS, HCR, PAR)
    for x in range(iterations):
        if HM.memory[0][1] == 0: 
            end = timer()
            break
        HM.improvise()
    else:
        end = timer()
    return (x+1, HM, HM.memory[0], end - start)



class HarmonyMemory():

    def __init__(self,problem,memory_size=50,HMCR=0.9,PAR=0.1):
        self.problem = problem
        self.memory_size = memory_size
        self.HMCR = HMCR 
        self.PAR =PAR 
        self.mask = [((x, y),j) for x, i in enumerate(problem) for y, j in enumerate(i)  if problem[x][y]!=0]

        self.memeory = [self.randSolution(problem) for x in range(memory_size)]
        self.memory =[(s,self.calculatePenalty(s)) for s in self.memeory]
        self.update()

    def randSolution(self, problem):

        

    ##################################################################################
        # randsol = np.random.randint(1, 10, size=(9,9), dtype = int)
        # for tup in self.mask:
        #     randsol[tup[0][0]][tup[0][1]] = tup[1]
    ####################################################################################


        # for row optimized initialization, uncomment the following section

    ######################################################################################
        randsol = np.zeros_like(problem)

        for tup in self.mask:
            randsol[tup[0][0]][tup[0][1]] = tup[1]

        for i in range(9):
            for j in range(9):
                if problem[i][j]==0:
                    choices = [1,2,3,4,5,6,7,8,9]
                    in_row = [n for n in randsol[i] if n!=0]
                    choices = list(set(choices) - set(in_row))
                    # print(choices)
                    randsol[i][j] = _r_.choice(choices)
                    # print(randsol)
    #######################################################################################
        
        return randsol

    def calculatePenalty(self, solution):

        # row element
        row_ele = np.sum(np.abs(np.sum(solution,1) - 45))

        # column element
        row_col = np.sum(np.abs(np.sum(solution,0) - 45))

        # square element
        row_square = 0
        for i in range(0,9,3):
            for j in range(0,9,3):
                row_square += np.abs(np.sum(solution[i:i+3,j:j+3]) - 45)

        return row_ele + row_col + row_square

    def update(self):
        self.memory.sort(key=lambda x:x[1])
        self.memory = self.memory[:self.memory_size]

    def new_harmony(self, i, j):
        hmcr_rand = _r_.random()
        if hmcr_rand >= self.HMCR: 
            new_harmo = _r_.randint(1,9)
        
        else:
            par_rand = _r_.random()
            new_harmo = _r_.choice([x[0][i][j] for x in self.memory])
            
            if par_rand <= self.PAR:
                binomial_rand = _r_.random()
                if binomial_rand >=0.5 and new_harmo!=9: 
                    new_harmo += 1
                elif binomial_rand <0.5 and new_harmo!=1:
                    new_harmo -= 1

        return new_harmo

    def improvise(self):
        new_sol = np.ones_like(self.problem)
        for i in range(9):
            for j in range(9):
                new_sol[i][j] = self.new_harmony(i,j)
        for tup in self.mask:
            new_sol[tup[0][0]][tup[0][1]] = tup[1]

        penalty = self.calculatePenalty(new_sol)

        if penalty < self.memory[-1][1]:
            self.memory[-1] = (new_sol, penalty)
            self.update()
       


if __name__ == "__main__":
    example_board = [[1, 0, 0, 0, 7, 0, 3, 0, 0],
                    [0, 8, 0, 0, 2, 0, 7, 0, 0],
                    [3, 0, 0, 0, 8, 9, 0, 0, 4],
                    [8, 4, 0, 0, 0, 1, 9, 0, 3],
                    [0, 0, 3, 7, 0, 8, 5, 0, 0],
                    [9, 0, 1, 2, 0, 0, 0, 7, 8],
                    [7, 0, 0, 3, 5, 0, 0, 0, 9],
                    [0, 0, 9, 0, 4 ,0 ,0 ,5 ,0],
                    [0, 0, 4, 0, 1, 0, 0, 0, 2]]
    # example_board = [[0, 5, 0, 3, 0, 6, 0, 0, 7],
    #                 [0, 0, 0, 0, 8, 5, 0, 2, 4],
    #                 [0, 9, 8, 4, 2, 0, 6, 0, 3],
    #                 [9, 0, 1, 0, 0, 3, 2, 0, 6],
    #                 [0, 3, 0, 0, 0, 0, 0, 1, 0],
    #                 [5, 0, 7, 2, 6, 0, 9, 0, 8],
    #                 [4, 0, 5, 0, 9, 0, 3, 8, 0],
    #                 [0, 1, 0, 5, 7 ,0 ,0 ,0 ,2],
    #                 [8, 0, 0, 1, 0, 4, 0, 7, 0]]
    iters, _, sol, tim = harmony_search(example_board, iterations=500, HMS=100)
    
    print("Value of min penalty function",sol[1])
    print(f'Iterations: {iters} \n Time taken: {tim}s')
   
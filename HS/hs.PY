
import random as _r_
import numpy as np


''''
Code for AI Assignment 2 
Implementation based on algorithim propsed by Zong Woo Geem in the paper 
Harmony Search Algorithim for solving sudoku 



In its basic version this algorithm is a heuristic method for solving discrete combinationl optimization problems 
initialize the Parameters for Problem and Algorithm.
Initialize the Harmony Memory (HM).
Improvise a New Harmony.
Update the Harmony Memory if the new harmony is better than the worst harmony in the memory.
Check the stopping criterion, and if we can continue, go back to 3.



In the HS algorithm, each musician (= decision variable)
 plays (= generates) a note (= a value) for finding a best harmony (= global optimum) 
 all together.
'''





## Harmonic memory consideration rate -HMCR 
## PAR the probability of randomly shifting a note up or down once it has been fixed



def harmony_search(prob, iterations=5000, HMS=100, HCR=.6, PAR=.2):
    HM = HarmonyMemory(prob, HMS, HCR, PAR)
    for x in range(iterations):
        if HM.memory[0][1] == 0: break
        HM.improvise()
    return (x+1, HM, HM.memory[0])



class HarmonyMemory():
    
    def __init__(self,problem,memory_size=50,HMCR=0.9,PAR=0.1):
        self.problem = problem
        self.memory_size = memory_size
        self.HMCR = HMCR 
        self.PAR =PAR 
        self.mask = [((x, y),j) for x, i in enumerate(problem) for y, j in enumerate(i)  if problem[x][y]!=0]
        ## this is initialised randomly 
        self.memeory = [self.randSolution(problem) for x in range(memory_size)]
        self.memory =[(s,self.calculatePenalty(s)) for s in self.memeory]
        self.update()
        # print(self.memory)

    def randSolution(self, problem):
        randsol = np.random.randint(1, 10, size=(9,9), dtype = int)
        # randsol = np.zeros_like(problem)

        for tup in self.mask:
            randsol[tup[0][0]][tup[0][1]] = tup[1]
         
        # for tup in self.mask:
        #     randsol[tup[0][0]][tup[0][1]] = tup[1]
        return randsol

    def calculatePenalty(self, solution):
        '''
        this function calculates the quality of each harmony 
        this function is being minimised
        '''
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
            # print (penalty, self.memory[-1][1])
            self.memory[-1] = (new_sol, penalty)
            self.update()
        # print(new_sol, penalty)
        # print(self.memory)    



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
    dd0,dd1,dd2 = harmony_search(example_board, iterations=5000, HMS=100)
    """
    the best harmony and minimu quality found is stored in HM[0]
    Prints out the the optimal solution board and the minimum penalty associated with it

    -- due to the random nature of filling the memory the solutions are different for each run  
    """

    print("The optimal solution and the associated optimal quality")
    print(dd2)
   
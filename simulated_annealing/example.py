#!/usr/bin/python

from __future__ import print_function
from builtins import range

from lib_simulated_annealing import simulated_annealing
from lib_sudoku import Sudoku
import matplotlib.pyplot as plt
import numpy


arr = numpy.loadtxt("test_samples.csv", delimiter=",", dtype=str)
for i in range (1,31):
    j=0
    for j in range (2):
        x = numpy.array(list(arr[i][j]), dtype=int)
        a = x.reshape(9,9)
        print(a.shape)
        if j == 0:
            numpy.savetxt("problem.dat", a, fmt = '%d')
        else:
            numpy.savetxt("solution.dat", a, fmt = '%d')    

    print("Solving puzzle: ", i)
    S = Sudoku('problem.dat')

    cooling_rate = 2e-2
    beta_min = 0.25
    beta_max = 1e2
    S, E, e_time = simulated_annealing(S,
                                    beta_min=beta_min, beta_max=beta_max,
                                    cooling_rate=cooling_rate,
                                    n_steps_per_T=1000, E_min=0)
    S.print_puzzle()

    plt.title('cooling_rate=%g' % cooling_rate)
    plt.xlabel('step', fontsize=18)
    plt.ylabel('energy', fontsize=18)
    plt.plot(E)
    plt.ylim(bottom=0)
    plt.savefig('fig.pdf', bbox_inches='tight')
    plt.show()

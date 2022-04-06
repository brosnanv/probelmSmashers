import numpy as np





import numpy as np
quizzes = np.zeros((20, 81), np.int32)
solutions = np.zeros((20, 81), np.int32)
for i, line in enumerate(open('test_samples.csv', 'r').read().splitlines()[1:]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s



quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))


quiz=0

for quiz in quizzes:
    print(quizzes[quiz])
    quiz = quiz+1


with open('file.txt','w') as f:
    for quiz in quizzes:
        f.write("Board"+str(quiz) % quiz )

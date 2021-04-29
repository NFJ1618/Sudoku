from solver import valid
from solver import solver
from random import randint
from random import shuffle
from time import time


def generator(sudoku):
    arr2 = [i%10 for i in range(1,30) if i%10 != 0]
    shuffle(arr2)
    i = 0
    j = 0
    stuck = 0
    while arr2:
        if sudoku[i][j] == 0:
            sudoku[i][j] = arr2.pop(0)
            if valid(sudoku):
                stuck = 0
                j += 1
                if j > 8:
                    j = j % 9
                    i += 1
            else:
                stuck += 1
                arr2.append(sudoku[i][j])
                sudoku[i][j] = 0
                if stuck == 10:
                    break

    if solver(sudoku, 0, 0):
        return sudoku
    else:
        return False



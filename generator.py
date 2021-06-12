from solver import valid
from solver import solver
from random import randint
from random import shuffle
from time import time


def generator(sudoku):
    arr2 = [i for i in range(1,10)]
    for i in range(3):
        shuffle(arr2)
        for j in range(3):
            for k in range(3):
                sudoku[3*i +j][3*i+ k] = arr2[3*j + k]

    if solver(sudoku, 0, 3):
        return sudoku
    else:
        return False



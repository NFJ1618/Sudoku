from random import randint
from random import random
from constants import difficulties
from solver import unique_solver
from generator import generator
import copy
from time import time

def remover(sudoku, difficulty):
    solved = copy.deepcopy(sudoku)
    l = -1
    if random() < 0.5:
        l *= -1
    remove = difficulties[difficulty] + randint(0,2) * l
    count = 0
    i = 0
    j = 0
    steps = 0
    while count < 81 - remove:
        if sudoku[i][j] != 0:
            if randint(1, 81) > difficulties[difficulty]:
                temp = sudoku[i][j]
                sudoku[i][j] = 0
                if unique_solver(copy.deepcopy(sudoku), 0, 0) != 1:
                    sudoku[i][j] = temp
                else:
                    count += 1
        j += 1
        steps += 1
        if j > 8:
            i += 1
            j = 0
            if i > 8:
                i = 0
        if steps > 200:
            break

    for i in sudoku:
        print(i)
    print(remove)
    return solved, sudoku


def main(n):
    start = time()
    sudoku = [
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
        [0] * 9,
              ]
    temp = generator(copy.deepcopy(sudoku))
    while not temp:
        temp = generator(copy.deepcopy(sudoku))
    for i in temp:
        print(i)
    print("\n")
    solved, sudoku = remover(temp, n)
    end = time()
    print(end - start)
    print("\n")
    return solved, sudoku


if __name__ == '__main__':
    main(1)
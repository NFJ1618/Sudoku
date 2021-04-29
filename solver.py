import sys
from sys import argv

def valid(sudoku):
    for i in range(9):
        arr1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        arr2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(9):
            arr1[sudoku[i][j]] += 1
            arr2[sudoku[j][i]] += 1
        for j in range(1,10):
            if arr1[j] > 1 or arr2[j] > 1:
                return False
    for i in range(3):
        for j in range(3):
            arr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for k in range(3):
                for l in range(3):
                    arr[sudoku[3*i + k][3*j + l]] += 1
            for m in range(1,10):
                if arr[m] > 1:
                    return False
    return True

def solved(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[8-i][8-j] == 0:
                return False
    return True


def unique_solver(sudoku, r, c):
    count = 0
    if solved(sudoku):
        return 1

    for row in range(r, 9):
        for col in range(c, 9):
            if sudoku[row][col] != 0:
                continue
            for i in range(1, 10):
                sudoku[row][col] = i
                if valid(sudoku):
                    c2 = 0
                    r2 = row
                    for j in range(col+1, 9):
                        if sudoku[row][j] == 0:
                            c2 = j
                            break
                    if c2 == 0:
                        r2 = row + 1
                    count += solver(sudoku, r2, c2)
                    if count > 1:
                        return count
            sudoku[row][col] = 0
        col = 0
    return count

def solver(sudoku, r, c):
    if solved(sudoku):
        return True

    for row in range(r, 9):
        for col in range(c, 9):
            if sudoku[row][col] != 0:
                continue
            for i in range(1, 10):
                sudoku[row][col] = i
                if valid(sudoku):
                    c2 = 0
                    r2 = row
                    for j in range(col+1, 9):
                        if sudoku[row][j] == 0:
                            c2 = j
                            break
                    if c2 == 0:
                        r2 = row + 1
                    if solver(sudoku, r2, c2):
                        return True
            sudoku[row][col] = 0
            return False
        col = 0
    return False

def main(filename):
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

    with open(filename, 'r') as f:

        i = 0
        for line in f:
            arr = line.split()
            sudoku[i] = [int(j) for j in arr]
            i += 1
            if i == 8:
                break
        solver(sudoku, 0, 0)


if __name__ == '__main__':
    file = 'sudokus/s01a.txt'
    main(file)

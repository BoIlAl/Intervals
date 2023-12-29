import numpy as np
from scipy.optimize import linprog

from fuzzy_number import FuzzyNumber
from interval import Interval

def readMartix(filename: str) -> []:
    m_empty = []
    m = []
    try:
        f = open(filename, 'r')
    except OSError:
        return m_empty

    size = -1

    for line in f:
        split = line.split()
        l = []
        for elem in split:
            try:
                l.append(float(elem))
            except ValueError:
                return m_empty
        
        if size == -1:
            size = len(l)
        elif len(l) != size:
            return m_empty

        m.append(l)

    if len(m) != size:
        return m_empty
    return m

def calc_b_2(A, x):
    b = np.dot(A, x)

    fuzzy_b = []

    eps = 0.0001
    for i in range(len(b)):
        fuzzy_b.append(FuzzyNumber(Interval(b[i] - eps, b[i] + eps), b[i] - 2 * eps, b[i] + 2 * eps))
    return fuzzy_b


def left_part(b : [], A):
    n = len(A)
    lp = []
    for i in range(n):
        lp_i = [0] * n
        lp_i[i] = -(b[i].wid / 2)
        lp.append(lp_i + A[i])
    for i in range(n):
        lp_i = [0] * n
        lp_i[i] = -(b[i].wid / 2)
        tmp = [-1 * elem for elem in A[i]]
        lp.append(lp_i + tmp)
    return lp


def right_part(b : []):
    rp = []
    for i in range(len(b)):
        rp.append(b[i].mid)
    for i in range(len(b)):
        rp.append(-b[i].mid)
    return rp


def regression(A, b):
    target_function = [1] * len(b) + [0] * len(A[0])
    lp = left_part(b, A)
    rp = right_part(b)
    n, m = len(A), len(A[0])
    bounds = [(0, None) for _ in range(n)] + [(None, None) for _ in range(m)]
    answer = linprog(c=target_function, A_ub=lp, b_ub=rp, bounds=bounds, method="highs")
    w = answer.x[:n]
    x = answer.x[n:]
    return w, x

def points_solution(A, b):
    b0 = [fuzzy.kernel for fuzzy in b]
    b1 = [fuzzy.support for fuzzy in b]
    _, x0 = regression(A, b0)
    _, x1 = regression(A, b1)
    return x0, x1


#Решение системы с твином/интервал в правой части 
def solution(A, b):
    invA = list(np.linalg.inv(np.array(A)))
    return np.dot(invA, b)

def div_solution(A, b):
    b0 = [fuzzy.kernel for fuzzy in b]
    b1 = [fuzzy.support for fuzzy in b]

    x_in = solution(A, b0)
    x_out = solution(A, b1)

    res = [FuzzyNumber(i, j.left, j.right) for i, j in zip(x_in, x_out)]
    return res


def print_vec(v: []):
    s = ''
    for elem in v:
        s += f'{elem} '
    print(s)

def main():
    A = readMartix("matrix.txt")
    x = [1] * len(A)
    b = calc_b_2(A, x)

    x_in, x_out = points_solution(A, b)
    print_vec(x_in)
    print_vec(x_out)

    x_1 = div_solution(A, b)
    print_vec(x_1)

    x_2 = solution(A, b)
    print_vec(x_2)


if __name__ == '__main__':
    main()
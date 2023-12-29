from math import sqrt
import sys

DIFF_RADIUS = 0.15
DIST_PIXELS = 0.01

def init_pixels(n):
    xt, yt = 3, 0
    x_pixels = 4
    
    if (n == 1):
        k = [0]
        b = [0]
        return k, b

    y, k, b, x = [], [], [], []

    x.append(x_pixels)
    y.append(DIST_PIXELS*(n-1)/2)
    k.append((yt-y[0]) / ( xt - x[0]))
    b.append(y[0] - k[0]*x[0])
    for i in range(1, n):
        x.append(x_pixels)
        y.append(y[i-1]-DIST_PIXELS)
        k.append((yt-y[i]) / ( xt - x[i]))
        b.append(y[i] - k[i]*x[i])
    return k, b

def len_c(a, b, c, d):
    return sqrt(abs(a-b)**2 + abs(c-d)**2)

def intersection_points(r, k, b):
    get_sqrt = pow(r, 2)*(1+pow(k, 2)) - pow(b, 2) 
    if(get_sqrt < 0):
        return 0
    elif(get_sqrt == 0):
        return 1
    else:
        return 2

def matrixA(coef_k, coef_b, m):
    prevD = 0
    D = 0
    n = len(coef_k) #count of pixel

    A = [ [0]*m for i in range(n) ]
    for i in range(n):
        radius = 0
        prevD = 0
        for j in range(m):
            radius += DIFF_RADIUS
            ip = intersection_points(radius, coef_k[i], coef_b[i])
            if(ip == 0):
                continue
            elif(ip == 1):
                A[i][j] = 0
                prevD = D = 0
            else:
                x1 = (-coef_k[i]*coef_b[i] + sqrt(pow(radius, 2)*(1+pow(coef_k[i], 2)) - pow(coef_b[i], 2) )) / ((1+pow(coef_k[i], 2)))
                x2 = (-coef_k[i]*coef_b[i] - sqrt(pow(radius, 2)*(1+pow(coef_k[i], 2)) - pow(coef_b[i], 2) )) / ((1+pow(coef_k[i], 2)))
                y1 = coef_k[i]*x1 + coef_b[i]
                y2 = coef_k[i]*x2 + coef_b[i]
                D = len_c(x1,x2,y1,y2)
                if prevD == 0:
                    A[i][j] = D
                    prevD = D
                else:
                    A[i][j] = abs(D - prevD)
                    prevD = D       
    return A

def is_uint(element: any) -> bool:
    if element is None: 
        return False
    try:
        elem = int(element)
    except ValueError:
        return False

    if (elem < 0):
        return False

    return True

def main():
    for param in sys.argv:
        print (param)
    
    if len(sys.argv) != 3:
        print("Err: Incorrect number of parameters")
        return
    
    if not is_uint(sys.argv[1]):
        print("Err: Incorrect matrix size")
        return
    
    size = int(sys.argv[1])

    if size == 0:
        print("Err: Incorrect matrix size")
        return

    try:
        f = open(sys.argv[2], 'w')
    except OSError:
        print(f"Could not open file: {sys.argv[2]}")
        return
    
    k, b = init_pixels(size * 2)
    A = matrixA(k, b, size)[:size]

    str = ""

    for line in A:
        for elem in line:
            str += f"{elem} "
        str += "\n"

    f.write(str)
    f.close()
    

if __name__ == "__main__":
    main()
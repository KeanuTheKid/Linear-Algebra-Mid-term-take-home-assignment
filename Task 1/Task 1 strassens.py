import numpy as np
import random
import time
import csv
def gen_matrices(size):
    matrix = []
    for k in range(size):#for columns
        row = []
        for i in range(size):
            row.append(random.randint(-99,99)) #generates rows that are "size" long
        matrix.append(row)#appends there rows to the matrix
    return np.array(matrix)#convert to np marix so we can handle it easier

def simple_matrix_multiplication(A, B):  # optimised matrix multiplication
    
    A = np.atleast_2d(A)
    B = np.atleast_2d(B)#I got frustrated debugging this so I somehow gotta make sure its 2d
    # Dimensions n
    n = len(A)        # rows in A
    m = len(A[0])     # columns in A (and rows in B)
    p = len(B[0])     # columns in B
    
    #"prepare" result matrix for easier multiplication later
    C = []
    for i in range(n): 
        row = []    #initialize result row, has to be in the loop so it gets erased after appending
        for j in range(p): #iterate through columns
            row.append(0)
        C.append(row)
    
    # matrix multiplication
    for i in range(n):
        for j in range(p):
            for k in range(m):
                C[i][j] += A[i][k] * B[k][j]
     
    return C
#returns smaller matrices
def split(matrix):
    n = len(matrix)
    a = np.atleast_2d(matrix[:n//2, :n//2])
    b = np.atleast_2d(matrix[:n//2, n//2:])
    c = np.atleast_2d(matrix[n//2:, :n//2])
    d = np.atleast_2d(matrix[n//2:, n//2:])
    return a, b, c, d

#for efficiency and easier coding I will use NumPy.
def strassens_algo(A, B):
    if len(A) <= 2: 
        #if matrices are small anyways we can use normal matrix multiplication. 
        #else splitt them and try again until we can solve every multiplication with the simple algo
        return simple_matrix_multiplication(A, B)
    #split into 4 matrices each
    a, b, c, d = split(A)
    e, f, g, h = split(B)
    #this sends the matrices back up if they aren't small enough. this also initializes the recursion
    # however if they are small enough it finally does the simple multiplication
    p1 = strassens_algo(np.add(a, d), np.add(e, h))
    p2 = strassens_algo(d, np.subtract(g, e))
    p3 = strassens_algo(np.add(a, b), h)
    p4 = strassens_algo(np.subtract(b, d), np.add(g, h))
    p5 = strassens_algo(a, np.subtract(f, h))
    p6 = strassens_algo(np.add(c, d), e)
    p7 = strassens_algo(np.subtract(a, c), np.add(e, f))
    #combination of the solved matrices
    C11 = np.add(np.subtract(np.add(p1, p2), p3), p4)
    C12 = np.add(p5, p3)
    C21 = np.add(p6, p2)
    C22 = np.subtract(np.add(p5, p1), np.add(p6, p7))
    #put them back together
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

#no recursion
#im not using comments we already made those operations earlier.
#instead of splitting the matrices over and over again, we split it once

def strassens_no_rec(A, B):
    if len(A) <= 2: 
        return simple_matrix_multiplication(A, B)
    
    a, b, c, d = split(A)
    e, f, g, h = split(B)
    
    p1 = simple_matrix_multiplication(np.add(a, d), np.add(e, h))
    p2 = simple_matrix_multiplication(d, np.subtract(g, e))
    p3 = simple_matrix_multiplication(np.add(a, b), h)
    p4 = simple_matrix_multiplication(np.subtract(b, d), np.add(g, h))
    p5 = simple_matrix_multiplication(a, np.subtract(f, h))
    p6 = simple_matrix_multiplication(np.add(c, d), e)
    p7 = simple_matrix_multiplication(np.subtract(a, c), np.add(e, f))
    
    C11 = np.add(np.subtract(np.add(p1, p2), p3), p4)
    C12 = np.add(p5, p3)
    C21 = np.add(p6, p2)
    C22 = np.subtract(np.add(p5, p1), np.add(p6, p7))
    
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))
    return C

#speed test
with open('matrix_times.csv', mode='a', newline='') as file:    #use a instead of w because it should add not overwrite
    writer = csv.writer(file)
    
    
    for i in range(4, 200,4): #steps of 4 so i dont have to fill the matrices for simplicity
        A = gen_matrices(i)
        B = gen_matrices(i)

        start_time = time.time()
        multiplication = strassens_algo(A, B)
        end_time = time.time()
        strassens_computing_time = (end_time - start_time)

        
        start_time = time.time()
        np_multiplication = strassens_no_rec(A, B)
        end_time = time.time()
        no_rec_strassens_computing_time = (end_time - start_time)

        print(f"size: {i} strassens: {strassens_computing_time}s , no rec: {no_rec_strassens_computing_time}s")
        writer.writerow([strassens_computing_time, no_rec_strassens_computing_time])    
    
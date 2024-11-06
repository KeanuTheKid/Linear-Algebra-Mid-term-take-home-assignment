import time
import random
import numpy as np
import csv
#matrices are none other than lists of lists
matrix_A = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]
#keeping in mind that python starts to count at 0
matrix_B = [
    [4,5,3],
    [3,4,8],
    [1,2,1]
]
for rows_a in matrix_A:#iterating through rows
    #print(rows_a)
    for element_a in rows_a:#iterating through elements
        #print(element_a)
        pass
 #matrix multiplication is row * column so I need a way to iterate through columns
# this function basically iterates through the rows 
# and takes the "Index" element of a row and puts its in a new list, which gives us a column
def matrix_column(Matrix, Index):
    column = []
    for row in Matrix:
        column.append(row[Index])
    return column
#as we can can get rows easily with a for loop, there is no reason to make a function

#now that we can iterate through rows and columns we can multiply   
def matrix_multiplication(A, B):
    result = [] #result matrix
    for row in A: #iterate through rows
        row_result = [] 
        for column_index in range(len(B[0])): #iterate through columns
            column = matrix_column(B, column_index)
            product_sum = 0
            for i in range(len(row)): #iterates through indices of the elements
                product_sum += row[i] * column[i]
            row_result.append(product_sum) # appends the sum of the products 
        result.append(row_result) # appends result rows to the matrix
    return result

def gen_matrices(size):
    matrix = []
    for k in range(size):#for columns
        row = []
        for i in range(size):
            row.append(random.randint(-99,99)) #generates rows that are "size" long
        matrix.append(row)#appends there rows to the matrix
    return matrix



with open('matrix_times.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # header
    writer.writerow(['size', 'Own Function', 'NumPy'])
    
    
    for i in range(1, 10):
        size = 2**i
        A = gen_matrices(size)
        B = gen_matrices(size)

        start_time = time.time()
        multiplication = matrix_multiplication(A, B)
        end_time = time.time()
        computing_time = (end_time - start_time)

        np_A = np.array(A)
        np_B = np.array(B)
        start_time = time.time()
        np_multiplication = np.matmul(np_A, np_B)
        end_time = time.time()
        np_computing_time = (end_time - start_time)

        print(f"size: {size} own function: {computing_time}s , numpy: {np_computing_time}s")
        writer.writerow([size, computing_time, np_computing_time])


import numpy as np
import random
import time
import csv

#I will use NumPy to write code more efficient. 

def gen_matrices(size):
    return np.random.randint(-99, 99, size=(size, size))

def simple_matrix_multiplication(A, B):
    return np.dot(A, B)

#split matrix into 4
def split(matrix):
    n = matrix.shape[0]
    a = matrix[:n//2, :n//2]
    b = matrix[:n//2, n//2:]
    c = matrix[n//2:, :n//2]
    d = matrix[n//2:, n//2:]
    return a, b, c, d

def strassens_algo(A, B):
#if its 2 or smaller we can use normal matrix multiplication
    if A.shape[0] <= 2:
        return simple_matrix_multiplication(A, B)
    
    # split both matrices into 4
    a, b, c, d = split(A)
    e, f, g, h = split(B)
    
    # recursive computing
    p1 = strassens_algo(a + d, e + h)
    p2 = strassens_algo(d, g - e)
    p3 = strassens_algo(a + b, h)
    p4 = strassens_algo(b - d, g + h)
    p5 = strassens_algo(a, f - h)
    p6 = strassens_algo(c + d, e)
    p7 = strassens_algo(a - c, e + f)
    
    # combine subsubmatrices back together
    C11 = p1 + p2 - p3 + p4
    C12 = p5 + p3
    C21 = p6 + p2
    C22 = p5 + p1 - p6 - p7
    
    # combine submatrices to get the resulting matrix
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))

# not recursive
def strassens_no_rec(A, B):
    a, b, c, d = split(A)
    e, f, g, h = split(B)
    
    p1 = simple_matrix_multiplication(a + d, e + h)
    p2 = simple_matrix_multiplication(d, g - e)
    p3 = simple_matrix_multiplication(a + b, h)
    p4 = simple_matrix_multiplication(b - d, g + h)
    p5 = simple_matrix_multiplication(a, f - h)
    p6 = simple_matrix_multiplication(c + d, e)
    p7 = simple_matrix_multiplication(a - c, e + f)
    
    C11 = p1 + p2 - p3 + p4
    C12 = p5 + p3
    C21 = p6 + p2
    C22 = p5 + p1 - p6 - p7
    
    top = np.hstack((C11, C12))
    bottom = np.hstack((C21, C22))
    return np.vstack((top, bottom))

# Speed-Test
# with open('size_speed_comparison.csv', mode='r') as file:
#     reader = csv.reader(file)
#     rows = list(reader)

# # Step 2: Add new columns
# header = rows[0]  # Extract the header
# header.extend(["Strassen's Optimized", "Another Algorithm"])  # Add new column names

# for row in rows[1:]:  # Skip the header row
#     size = int(row[0])
#     A = gen_matrices(size)
#     B = gen_matrices(size)

#     # Compute new values
#     start_time = time.time()
#     optimized_result = strassens_algo(A, B)
#     end_time = time.time()
#     optimized_time = end_time - start_time

#     start_time = time.time()
#     another_result = strassens_no_rec(A, B)
#     end_time = time.time()
#     another_time = end_time - start_time
#     print(f"size: {size} strassens: {optimized_time}s , no rec: {another_time}s")
#     # Append results to the row
#     row.extend([optimized_time, another_time])

# with open('size_speed_comparison.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(rows)
    


with open('amount_speed_comparison.csv', mode='r') as file:
    reader = csv.reader(file)
    rows = list(reader)

header = rows[0]  # extract the existing header
header.extend(["Strassen's Optimized Time", "Strassen's No Rec Time"])

for row in rows[1:]:  # skip the header row
    num_multiplications = int(row[0])  
    size = 2  

    A = gen_matrices(size)
    B = gen_matrices(size)

    start_time = time.time()
    for _ in range(num_multiplications):
        optimized_result = strassens_algo(A, B)
    end_time = time.time()
    optimized_time = end_time - start_time

    start_time = time.time()
    for _ in range(num_multiplications):
        another_result = strassens_no_rec(A, B)
    end_time = time.time()
    another_time = end_time - start_time

    print(f"Multiplications: {num_multiplications}, Strassen's Optimized Time: {optimized_time:.6f}s, Strassen's No Rec Time: {another_time:.6f}s")
    
    #append results to the current row
    row.extend([optimized_time, another_time])

#write the updated data back to the CSV
with open('amount_speed_comparison.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)
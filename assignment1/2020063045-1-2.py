import numpy as np

# A. Create a 1d array M with values ranging from 2 to 26 and print M.
M = np.array(range(2, 27))
print(M)

# B. Reshape M as a 5x5 matrix and print M.
M = np.reshape(M, [5, 5])
print(M)

# C. Set the value of “inner” elements of the matrix M to 0 and print M.
M[1:-1, 1:-1] = 0
print(M)

# D. Assign M2 to the M and print M.
print(M*M)

# E. Let’s call the first row of the matrix M a vector v. Calculate the magnitude of the vector v and print it.
print(np.sqrt(np.sum(M[0]*M[0])))


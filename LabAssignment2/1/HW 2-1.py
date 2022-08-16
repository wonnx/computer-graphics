import numpy as np

M = np.arange(2,27)
print(M); print()

M = M.reshape(5,5)
print(M); print()

for i in range(1,4):
    for j in range(1,4):
        M[i,j]=0
print(M); print()

M = M@M
print(M); print()

v=0
for i in range(5):
    v+=M[0,i]*M[0,i]
v=np.sqrt(v)
print(v)

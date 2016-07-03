# -*- coding: utf-8 -*-
#
# Dappled tiling
# by S. Kaji
# 17/Jun/2016
# 
# A python implementation of the algorithm discussed in the paper
# "Dappled tiling"
# By S. Kaji and .....
#

import numpy as np
import random

# size of the grid
M = 12
N = 10

# conditions: H[i] is the limit of the length of the horizontal strip with tile i
H = [2,5]
V = [5,2]

# (quick dirty) global variables
# for book-keeping the number of consecutive tiles
VDanger = np.ones((M+1), dtype=np.int)
HDanger = np.ones((M+1), dtype=np.int)

# choose a tile different from t
def chooseTile(t):
    return 1-t

# set barrier
def setbarrier(f,n,m):
    for i in range(n+1):
        f[i,0] = -1
    for j in range(m+1):
        f[0,j] = -1        
    return f

# give a randomised tiling
def randtiling(n,m):
    f = np.zeros((n+1,m+1), dtype=np.int)
    for i in range(1,n+1):
        for j in range(1,m+1):
            f[i,j] = random.randint(0,1)
    return setbarrier(f,n,m)

# give an all-one tiling
def onetiling(n,m):
    f = np.ones((n+1,m+1), dtype=np.int)
    return setbarrier(f,n,m)

# give a diagonal tiling
def diagtiling(n,m):
    f = np.ones((n+1,m+1), dtype=np.int)
    for i in range(1,n+1):
        for j in range(i,min(i+int(m/2),m+1)):
            f[i,j] = 0
    return setbarrier(f,n,m)
    

# compute the number of consecutive tiles of lower weights
def compute_danger(f,i,j):
    if f[i,j]==f[i-1,j]:
        VDanger[j] = VDanger[j]+1
    else:
        VDanger[j] = 1
    if f[i,j]==f[i,j-1]:
        HDanger[j] = HDanger[j-1]+1
    else:
        HDanger[j] = 1

# print tiling patterns
def printtiling(f):
    print(f[1:N+1,1:M+1]) 

# convert any tiling to a dappled one
def dappled(f):
    for w in range(1,N+M+1):
        for i in range(max(1,w-M),min(w,N+1)):
            j = w-i
            prev_vd=VDanger[j]
            compute_danger(f,i,j)
            if V[f[i,j]] < VDanger[j] or H[f[i,j]] < HDanger[j]:
                f[i,j]=chooseTile(f[i,j])
                VDanger[j]=prev_vd
                compute_danger(f,i,j)
                if V[f[i,j]] < VDanger[j]:
                    f[i,j]=f[i-1,j-1]
                    f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
                    HDanger[j]=VDanger[j]=VDanger[j-1]=1
                    if j < M:
                        if f[i-1,j]==f[i-1,j+1]:
                            HDanger[j+1]=2
                elif H[f[i,j]] < HDanger[j]:
                    f[i,j]=f[i-1,j-1]
                    f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
                    VDanger[j]=HDanger[j]=VDanger[j-1]=1
                    if j < M:
                        if f[i-1,j]==f[i-1,j+1]:
                            HDanger[j+1]=2

## main 
if __name__ == "__main__":
    print((M,N))
    f = randtiling(N,M)
#    f = diagtiling(N,M)
#    f = onetiling(N,M)
    print("Initial tiling")
    printtiling(f)

    dappled(f)
             
    print("Dappled tiling")
    printtiling(f)
    exit

            

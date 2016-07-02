# -*- coding: utf-8 -*-
#
# Cyclically Dappled tiling
# by S. Kaji
# 30/Jun/2016
# 
# A python implementation of the algorithm discussed in the paper
# "Dappled tiling"
# By S. Kaji et al
# This program also produces cyclically dappled tilings.
#

import numpy as np
import random

# size of the grid
M = 7
N = 10

# conditions: H[i] is the limit of the length of the horizontal strip with tile i
# set >2 for cyclic version
H = [2,M]
V = [N,2]

# set true for the cyclic version
CYCLIC = True
# set true for bezel version; necessary when min(p)=min(q)=2
BEZEL = True

# set true to print debug information
DEBUG = False

# (quick dirty) global variables
# for book-keeping the number of consecutive tiles
HDanger = np.ones((M), dtype=np.int)
VDanger = np.ones((M), dtype=np.int)
prevHDanger = np.ones((M), dtype=np.int)
prevVDanger = np.ones((M), dtype=np.int)

# choose a tile different from t
def chooseTile(t):
    return 1-t

# give a randomised tiling
def randtiling(n,m):
    f = np.zeros((n,m), dtype=np.int)
    for i in range(n):
        for j in range(m):
            f[i,j] = random.randint(0,1)
    return f

# give a all-one tiling
def onetiling(n,m):
    f = np.ones((n,m), dtype=np.int)
    return f

# give a diagonal tiling
def diagtiling(n,m):
    f = np.ones((n,m), dtype=np.int)
    for i in range(0,n):
        for j in range(i,min(i+int(m/2),m)):
            f[i,j] = 0
    return f

# erroneous examples
def erroneoustiling():
    global N,M
    N=5
    M=5

    # f=np.array([[0, 1, 0, 1, 0],
    #    [1, 0, 1, 0, 1],
    #    [1, 1, 0, 0, 1],
    #    [0, 1, 1, 0, 0],
    #    [1, 0, 0, 1, 1]])

    f=np.array([[0, 1, 0, 1, 1],
            [1, 0, 0, 1, 0],
            [1, 1, 0, 0, 0],
            [0, 0, 1, 0, 1],
            [1, 0, 1, 0, 0]])

    return f


# compute the number of consecutive cells in the up and to the left directions at (i,j)
def compute_danger(f,i,j,n2,m2):
    global VDanger, HDanger
    addH = addV = 0
    if i != 0 and f[i,j]==f[i-1,j]:
        VDanger[j] = prevVDanger[j]+1
    else:
        VDanger[j] = 1
    if CYCLIC:
        if i==n2-1:
            k=1
            while(f[i,j]==f[(i+k) % N,j]):
                addV = addV+1
                k=k+1
        l = 2 if V[f[i,j]]>2 else 1
        if not BEZEL and i==V[f[i,j]]-l:
            addV = addV+l

    if j != 0 and f[i,j]==f[i,j-1]:
        HDanger[j] = prevHDanger[j-1]+1
    else:
        HDanger[j] = 1
    if CYCLIC:
        if j==m2-1:
            k=1
            while(f[i,j]==f[i,(j+k) % M]):
                addH = addH+1
                k=k+1
        l = 2 if H[f[i,j]]>2 else 1
        if not BEZEL and j==H[f[i,j]]-l:
            addH = addH+l
    return (addH,addV)


# fix invalidness of the cell (i,j)
def fix_at(f,i,j,n2,m2):
    (addH,addV)=compute_danger(f,i,j,n2,m2)
    if V[f[i,j]] < VDanger[j]+addV or H[f[i,j]] < HDanger[j]+addH:
        if DEBUG:
            print(prevHDanger,HDanger,addH,addV)
        f[i,j]=chooseTile(f[i,j])
        (addH,addV)=compute_danger(f,i,j,n2,m2)
        if V[f[i,j]] < VDanger[j]+addV or H[f[i,j]] < HDanger[j]+addH:
                f[i,j]=f[i-1,j-1]
                f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
                VDanger[j]=HDanger[j]=prevVDanger[j-1]=prevHDanger[j]=1
                if i > 0 and j < M-1:
                    HDanger[j + 1] = 2 if f[i-1,j]==f[i-1,j+1] else 1
                if j > 0 and i < N-1:
                    VDanger[j - 1] = 2 if f[i,j-1]==f[i+1,j-1] else 1
        if DEBUG:
            print(i,j)
            printtiling(f)


# rectify invalid cells in the region (n1,m1)-(n2-1,m2-1)
def rectify(f,n1,m1,n2,m2):
    global prevHDanger,prevVDanger
    for w in range(n1+m1,n2+m2-1):
        for i in range(max(n1,w-m2+1),min(w+1-m1,n2)):
            fix_at(f,i,w-i,n2,m2)
        if w >= m2-1:
            fix_at(f,w-m2+1,m2-1,n2,m2)
        prevHDanger = HDanger.copy()
        prevVDanger = VDanger.copy()


# turn an input to a dappled one
def dappled(f):
    global HDanger,VDanger,prevHDanger,prevVDanger
    HDanger = np.ones((M), dtype=np.int)
    VDanger = np.ones((M), dtype=np.int)
    prevHDanger = np.ones((M), dtype=np.int)
    prevVDanger = np.ones((M), dtype=np.int)
    g=f.copy()
    if BEZEL:
        bezel(g)
        rectify(g,1,1,N-1,M-1)
    else:
        rectify(g,0,0,N,M)
    return g

# Bezel trick on the boundary
def bezel(f):
    f[N-1,M-1]=f[0,0]
    f[N-1,0]=f[0,M-1]=chooseTile(f[0,0])
    f[0,M-3]=f[N-3,0]
    if M % 2 == 0:
        f[0, M-2] = f[0,0]
        f[N-1,M-2] = chooseTile(f[0,0])
        f[0,M-4] = chooseTile(f[0,M-3])
    if N % 2 == 0:
        f[N-2,0] = f[0,0]
        f[N-2,M-1] = chooseTile(f[0,0])
        f[N-4,0] = chooseTile(f[N-3,0])
    for i in range(int((N-1)/2)):
        f[2*i+1,0] = chooseTile(f[2*i,0])
        f[2*i+1,M-1] = f[2*i,0]
        f[2*i,M-1] = chooseTile(f[2*i,0])
    for j in range(int((M-1)/2)):
        f[0,2*j+1] = chooseTile(f[0,2*j])
        f[N-1,2*j+1] = f[0,2*j]
        f[N-1,2*j] = chooseTile(f[0,2*j])

# check if f is valid at (i,j)
def violate(f, i, j):
    vl = True
    if CYCLIC or j>=H[f[i,j]]:
        if H[f[i,j]] < M:
            for k in range(1,H[f[i,j]]+1):
                if f[i,(j-k) % M] != f[i,j]:
                    vl = False
                    break
            if vl:
                return True
        

    if CYCLIC or i>=V[f[i,j]]:
        if V[f[i,j]] < N:
            for k in range(1,V[f[i,j]]+1):
                if f[(i-k) % N,j] != f[i,j]:
                    vl = False
                    break
            if vl:
                return True
    return False

# return the list of invalid cells
def is_dappled(f):
    return [(i,j) for i in range(0,N) for j in range(0,M) if violate(f,i,j)]

# test the program with many randomly-generated samples
def measure_miss(samples):
    for s in range(samples):
        f = randtiling(N,M)
        g = dappled(f)
        errors = is_dappled(g)
        if len(errors)>0:
            print("Errors at ",errors)
            print("initial tiling")
            print(N,f)
            print("output")
            print(g)
            return False
    return True


# print tiling patterns
def printtiling(f):
    print(f) 


## start here
if __name__ == "__main__":
    print("Size of the board",(M,N))
    print("Maximal number of horizontally consecutive tiles", H)
    print("Maximal number of vertically consecutive tiles", V)

#    if not DEBUG:
#        print(measure_miss(10000))

    f = randtiling(N,M)
#    f = diagtiling(N,M)
#    f = onetiling(N,M)

    print("Initial tiling")
    printtiling(f)

    if CYCLIC:
        print("Cyclically dappled tiling")
    else:
        print("Dappled tiling")

    g=dappled(f)
    printtiling(g)
    print(is_dappled(g))


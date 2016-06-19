# -*- coding: utf-8 -*-
#
# Cyclically Dappled tiling
# by S. Kaji
# 17/Jun/2016
# 
# A python implementation of the algorithm discussed in the paper
# "Dappled tiling"
# By S. Kaji and .....
# This program also produces cyclically dappled tilings.
#

import numpy as np
import random

# size of the grid
M = 12
N = 10

# conditions: H[i] is the limit of the length of the horizontal strip with tile i
H = [2,M+1]
V = [N+1, 2]

# (quick dirty) global variables
# for book-keeping the number of consecutive tiles
HDanger = np.ones((M), dtype=np.int)
VDanger = np.ones((M), dtype=np.int)


# choose a tile different from t
# TODO: extend it for |T|>2
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


#
def compute_danger(f,i,j):
    if f[i,j]==f[i-1,j]:
        VDanger[j] = VDanger[j]+1
    else:
        VDanger[j] = 1
    if f[i,j]==f[i,j-1]:
        HDanger[j] = HDanger[j-1]+1
    else:
        HDanger[j] = 1

## interior
def rectifyInterior(f,n,m):
    for w in range(1,n+m-1):
        for i in range(max(1,w-m+1),min(w,n)):
            j = w-i
            prev_vd=VDanger[j]
            compute_danger(f,i,j)
            if V[f[i,j]] < VDanger[j] or H[f[i,j]] < HDanger[j]:
                f[i,j]=chooseTile(f[i,j])
                VDanger[j]=prev_vd
                compute_danger(f,i,j)
                if V[f[i,j]] < VDanger[j]:
                    if f[i-1,j] == f[i,j-1]:
                        f[i,j] = chooseTile(f[i-1,j])
                        VDanger[j]=HDanger[j]=1
                    else:
                        f[i,j]=f[i-1,j-1]
                        f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
                        HDanger[j]=VDanger[j]=VDanger[j-1]=1
                        if j < M-1:
                            if f[i-1,j]==f[i-1,j+1]:
                                HDanger[j+1]=2
                elif H[f[i,j]] < HDanger[j]:
                    if f[i-1,j] == f[i,j-1]:
                        f[i,j] = chooseTile(f[i,j-1])
                        VDanger[j]=HDanger[j]=1
                    else:
                        f[i,j]=f[i-1,j-1]
                        f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
                        VDanger[j]=HDanger[j]=VDanger[j-1]=1
                        if j < M-1:
                            if f[i-1,j]==f[i-1,j+1]:
                                HDanger[j+1]=2

    
    
# boundary
def rectifyBoundary(f):
    danger = 1
    for i in range(1,N):
        if f[i,0] == f[i-1,0]:
            danger = danger + 1
            if V[f[i,0]] < danger:
                f[i,0]=chooseTile(f[i,0])
                danger = 1
    danger = 1
    for j in range(1,M):
        if f[0,j] == f[0,j-1]:
            danger = danger + 1
            if H[f[0,j]] < danger:
                f[0,j]=chooseTile(f[0,j])
                danger = 1
    
# Bezel trick on the boundary
def bezel(f):
    f[N-1,M-1]=f[0,0]
    f[N-1,0]=f[0,M-1]=chooseTile(f[0,0])
    for i in range(int(N/2)):
        f[2*i+1,0] = chooseTile(f[2*i,0])
        f[2*i+1,M-1] = f[2*i,0]
    for j in range(int(M/2)):
        f[0,2*j+1] = chooseTile(f[0,2*j])
        f[N-1,2*j+1] = f[0,2*j]
    for i in range(1,int(N/2)):
        f[2*i,M-1] = chooseTile(f[2*i,0])
    for j in range(1,int(M/2)):
        f[N-1,2*j] = chooseTile(f[0,2*j])

#
def compute_danger_terminal(f,i,j):
    hd=1
    for k in range(1,min(H[f[i,j]],j)+1):
        if f[i,j-k]==f[i,j]:
            hd=hd+1
        else:
            break
    if f[i,j]==f[i,j+1]:
        hd=hd+1
    vd=1
    for k in range(1,min(V[f[i,j]],i)+1):
        if f[i-k,j]==f[i,j]:
            vd=vd+1
        else:
            break
    if f[i,j]==f[i+1,j]:
        vd=vd+1
    return (hd,vd)
# 
def rectifyTerminal(f):
    for i in range(1,N-2):
        j=M-2
        (hd,vd)=compute_danger_terminal(f,i,j)
        if V[f[i,j]] < vd or H[f[i,j]] < hd:
            f[i,j]=chooseTile(f[i,j])
            (hd,vd)=compute_danger_terminal(f,i,j)
            if V[f[i,j]] < vd:
                f[i,j]=f[i-1,j-1]
                f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
            elif H[f[i,j]] < hd:
                f[i,j]=f[i-1,j-1]
                f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])        
    for j in range(1,M-1):
        i=N-2
        (hd,vd)=compute_danger_terminal(f,i,j)
        if V[f[i,j]] < vd or H[f[i,j]] < hd:
            f[i,j]=chooseTile(f[i,j])
            (hd,vd)=compute_danger_terminal(f,i,j)
            if V[f[i,j]] < vd:
                f[i,j]=f[i-1,j-1]
                f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])
            elif H[f[i,j]] < hd:
                f[i,j]=f[i-1,j-1]
                f[i-1,j]=f[i,j-1]=chooseTile(f[i,j])        

    return f


# print tiling patterns
def printtiling(f):
    print(f) 

if __name__ == "__main__":
    print((M,N))
#    f = randtiling(N,M)
    f = diagtiling(N,M)
#    f = onetiling(N,M)
    print("Initial tiling")
    printtiling(f)

    g=f.copy()        
    print("Dappled tiling")
    rectifyBoundary(f)
    rectifyInterior(f,N,M)
    printtiling(f)

    print("Cyclically dappled tiling")
    bezel(g)
    rectifyInterior(g,N-1,M-1)
    rectifyTerminal(g)
    printtiling(g)

    exit

            

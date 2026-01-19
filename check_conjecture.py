import copy
from permutation import Permutation
n=7
S_n=Permutation.group(n)

mult=[]
def comm_classes(p,l):  
    global count
    if(l==0):
        count=1
        return
    for i in range(1,n):
        if(p[i]>p[i+1]):
            perm=copy.deepcopy(p)
            perm[i],perm[i+1]=perm[i+1],perm[i]
            comm_gen(perm, i, l-1)

def comm_gen(p,i,l):
    global count
    if(l==0):
        count+=1
    for j in range(i+1,0,-1):
        if(i==n-1 and j==i+1):
            continue
        if(p[j]>p[j+1]):
            p[j],p[j+1]=p[j+1],p[j]
            comm_gen(p, j, l-1)
            p[j],p[j+1]=p[j+1],p[j]
            
def red_gen(p,l):
    global count_red
    if(l==0):
        count_red+=1
    else:
        for j in range(1,n):
            if(p[j]>p[j+1]):
                p[j],p[j+1]=p[j+1],p[j]
                red_gen(p,l-1)
                p[j],p[j+1]=p[j+1],p[j]


for p in S_n:
    count=0
    count_red=0
    perm=list(p.to_image(n))
    perm.insert(0, 0)

    comm_classes(perm,p.inversions())
    perm=list(p.to_image(n))
    perm.insert(0, 0)
    red_gen(perm,p.inversions())
    if(count>count_red/2+1):
        print(perm)
    
        
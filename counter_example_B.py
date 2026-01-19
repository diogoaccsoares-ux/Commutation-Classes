import copy
from permutation import Permutation
import itertools
n=6
S_n=Permutation.group(n)

class Word:
    def __init__(self,w):
        self.word=w
        self.r_ord=[]
        self.r_braid_pos=[]
        
    def compute_r_order(self):
        id_perm=[i for i in range(n+1)]
        for s in self.word:
            if(s!=0):
                im_1=id_perm[s]
                im_2=id_perm[s+1]
                self.r_ord.append((im_1,im_2))
                id_perm[s],id_perm[s+1]=id_perm[s+1],id_perm[s]
            else:
                im_1=-id_perm[1]
                im_2=id_perm[1]
                self.r_ord.append((im_1,im_2))
                id_perm[1]=-id_perm[1]
                
    def compute_braid_pos(self):
        for i in range(len(self.word)):
            s=self.word[i]
            if(s!=0):
                if(s!=n-1 and i>0 and i!=len(self.word)-1):
                    pos=[]
           
                    for j in range(i-1,-1,-1):
                        if(self.word[j]==s or self.word[j]==s+2):
                            break
                        if(self.word[j]==s+1):
                            pos.append(j)
                            break
                    if(len(pos)==1):
                        for j in range(i+1,len(self.word)):
                            if(self.word[j]==s or self.word[j]==s+2):
                                break
                            if(self.word[j]==s+1):
                                pos.append(j)
                                break
                    if(len(pos)==2):
                        self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])

                if(s!=1):
                    pos=[]                 
                    for j in range(i-1,-1,-1):
                        if(self.word[j]==s or self.word[j]==s-2):
                            break
                        if(self.word[j]==s-1):
                            pos.append(j)
                            break
                    if(len(pos)==1):
                        for j in range(i+1,len(self.word)):
                            if(self.word[j]==s or self.word[j]==s-2):
                                break
                            if(self.word[j]==s-1):
                                pos.append(j)
                                break
                    if(len(pos)==2):
                        self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])
            else:
                pos=[]
                for j in range(i+1,len(self.word)-2):
                    if(self.word[j]==1):
                        if(self.word[j+1]==0 and self.word[j+2]==1):
                            pos=[i,j+1]
                            self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])
                            break
                        else:
                            break
                pos_1=[]
                if(i>2):
                    if(self.word[i-3]==1 and self.word[i-2]==0 and self.word[i-1]==1):
                        pos_1=[i-2,i]
                        self.r_braid_pos.append([self.r_ord[pos_1[0]],self.r_ord[pos_1[1]]])
                        

def words_generator(w,perm,length,max_length):
    if(length==max_length):
        new_w=copy.deepcopy(w)
        new_w.reverse()
        new_cls=Word(new_w)
        new_cls.compute_r_order()
        new_cls.compute_braid_pos()
        clss.append(new_cls)  
    else:
        if(length==0):
            for i in range(n):  
                if(i!=0):
                    if(perm[i]>perm[i+1]):                    
                        w[length]=i
                        perm[i],perm[i+1]=perm[i+1],perm[i]
                        words_generator(w, perm, length+1, max_length)
                        perm[i],perm[i+1]=perm[i+1],perm[i]
                else:
                    if(perm[1]<0):
                        w[length]=i
                        perm[1]=-perm[1]
                        words_generator(w, perm, length+1, max_length)
                        perm[1]=-perm[1]
                        
                    
                
        else:           
            last=w[length-1]
            for i in range(last-1,-1,-1):
                if(i!=0):
                    if(perm[i]>perm[i+1]):                   
                        w[length]=i                       
                        perm[i],perm[i+1]=perm[i+1],perm[i]
                        words_generator(w, perm, length+1, max_length)
                        perm[i],perm[i+1]=perm[i+1],perm[i]
                else:
                    if(perm[1]<0):
                        w[length]=i
                        perm[1]=-perm[1]
                        words_generator(w, perm, length+1, max_length)
                        perm[1]=-perm[1]                        
                   
                            
                        
            if(last+1<n and perm[last+1]>perm[last+2]):
                i=last+1
                w[length]=i                
                perm[i],perm[i+1]=perm[i+1],perm[i]
                words_generator(w, perm, length+1, max_length)
                perm[i],perm[i+1]=perm[i+1],perm[i]


def pattern_finder(w):
    #returns 0 if w is -1-2-3-4 avoiding; returns 1 otherwise
    if n<4:
        return 0
    
    for s in itertools.combinations([i for i in range(1,n+1)], 4):
        if 0>w[s[0]]>w[s[1]]>w[s[2]]>w[s[3]]:
            return 1
        
    return 0

def length(p,n,tp):
    #Compute the length of a permutation
    count=0
    for i in range(1,n):
        for j in range(i+1,n+1):
            if p[i]>p[j]:
                count+=1
            if -p[i]>p[j]:
                count+=1
    if tp=='B':
        for i in range(1,n+1):
            if p[i]<0:
                count+=1
    return count

n=5

clss=[]          

id_perm=[i for i in range(1,n+1)]
S_n=itertools.permutations(id_perm)

for pp in S_n:
    perm=list(pp)
    perm.insert(0, 0)
    binary=itertools.product([-1,1],repeat=n)
    for b in binary:
        count=0
        for i in range(n):
            if(b[i]==-1):
                count+=1
         
        binn=list(b)
        for i in range(1,n+1):
            perm[i]*=binn[i-1]
        
        if(pattern_finder(perm)==0 and perm[n]!=n):
            l=length(perm,n,'B')
            words_generator([None]*l, perm, 0,l)   
            
            for a in clss:
                find=0
                for b in clss:
                    if(a.word!=b.word):
                        flag=0
                        for p in b.r_braid_pos:
                            p1=p[0]
                            p2=p[1]
                            negp1=(-p1[1],-p1[0])
                            negp2=(-p2[1],-p2[0])
                            for r in a.r_ord:
                                if r==p1 or r==negp1:
                                    break
                                if r==p2 or r==negp2:
                                    flag=1
                                    break
                            if(flag==1):
                                break
                        if(flag==0):
                            find=1
                            print("Counter-example found: ", perm)
                            print(a.word,b.word)
                            break
                if(find==1):
                    break
            
        clss=[]
        for i in range(1,n+1):
            perm[i]*=binn[i-1]
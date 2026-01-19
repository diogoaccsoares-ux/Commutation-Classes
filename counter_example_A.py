import copy
import itertools


comm_classes=[]
class Word:
    def __init__(self,w):
        self.word=w
        self.r_ord=[]
        self.r_braid_pos=[]
    
    def compute_r_order(self):
        id_perm=[i for i in range(n+1)]
        for s in self.word:
            i=id_perm[s]
            j=id_perm[s+1]
            self.r_ord.append((i,j))
            id_perm[s],id_perm[s+1]=id_perm[s+1],id_perm[s]
            
    def compute_braid_pos(self):
        #compute the pairs of inversions associated to braid relations involving word
        for i in range(1,len(self.word)-1):
            s=self.word[i]
            if(s!=n-1):
                pos=[]      
                for j in range(i-1,-1,-1): #Seaching for a subword (s+1)s(s+1)
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
        
            if(s>1): #Seaching for a subword (s-1)s(s-1)
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
            
                
                    
def length(p):
    soma=0
    for i in range(1,n):
        for j in range(i+1,n+1):
            if(p[i]>p[j]):
                soma+=1
            
    
    return soma

def generate_comm(w,perm,pos,max_length):
    if(pos==0):
        for i in range(1,n):
            if(perm[i]>perm[i+1]):
                perm[i],perm[i+1]=perm[i+1],perm[i]
                w[pos]=i
                generate_comm(w,perm,pos+1,max_length)
                perm[i],perm[i+1]=perm[i+1],perm[i]
    else:
        if(pos==max_length):
            new_w=copy.deepcopy(w)
            new_w.reverse()
            new_word=Word(new_w)
            new_word.compute_r_order()
            new_word.compute_braid_pos()
            comm_classes.append(new_word)
        else:
            last=w[pos-1]
            if(last<n-1):
                for i in range(1,last+2):
                    if(perm[i]>perm[i+1]):
                        perm[i],perm[i+1]=perm[i+1],perm[i]
                        w[pos]=i
                        generate_comm(w,perm,pos+1,max_length)
                        perm[i],perm[i+1]=perm[i+1],perm[i]
            else:
                for i in range(last):
                    if(perm[i]>perm[i+1]):
                        perm[i],perm[i+1]=perm[i+1],perm[i]
                        w[pos]=i
                        generate_comm(w,perm,pos+1,max_length)
                        perm[i],perm[i+1]=perm[i+1],perm[i]

          

def pattern_654321_finder(w):
    #returns 0 if w is 654321 avoiding; returns 1 otherwise
    if n<6:
        return 0
    
    for s in itertools.combinations([i for i in range(1,n+1)], 6):
        if w[s[0]]>w[s[1]]>w[s[2]]>w[s[3]]>w[s[4]]>w[s[5]]:
            return 1
        
    return 0
                    
                
        
    
n=6

id_perm=[i for i in range(1,n+1)]
S_n=itertools.permutations(id_perm)
i=0
for p in S_n:
    perm=list(p)
    perm.insert(0, 0) 
    if(pattern_654321_finder(perm)==0):
        l=length(perm) 
        generate_comm([0]*l, perm, 0, l)    
        for a in comm_classes:
            find=0
            for b in comm_classes:
                if(a.word!=b.word):
                    flag=0
                    for p in b.r_braid_pos:
                        p1=p[0]
                        p2=p[1]
                        for r in a.r_ord:
                            if r==p1:
                                break
                            if r==p2:
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
    
    comm_classes=[]
    

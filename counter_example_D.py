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
            if(s==0):
                i=-id_perm[1]
                j=id_perm[2]
                self.r_ord.append((i,j))
                id_perm[1],id_perm[2]=-id_perm[2],-id_perm[1]
            else:
                i=id_perm[s]
                j=id_perm[s+1]
                self.r_ord.append((i,j))
                id_perm[s],id_perm[s+1]=id_perm[s+1],id_perm[s]
                
            
    def compute_braid_pos(self):
        for i in range(1,len(self.word)-1):
            s=self.word[i]
            if(s!=n-1 and s!=0):
                pos=[]      
                for j in range(i-1,-1,-1):
                    if(self.word[j]==s or self.word[j]==s+2):
                        break
                    if(self.word[j]==0 and s==1):
                        break
                    if(self.word[j]==s+1):
                        pos.append(j)
                        break
                if(len(pos)==1):
                    for j in range(i+1,len(self.word)):
                        if(self.word[j]==s or self.word[j]==s+2):
                            break
                        if(self.word[j]==0 and s==1):
                            break
                        if(self.word[j]==s+1):
                            pos.append(j)
                            break
                if(len(pos)==2):
                    self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])
            if(s==0):
                pos=[]      
                for j in range(i-1,-1,-1):
                    if(self.word[j]==0 or self.word[j]==1 or self.word[j]==3):
                        break
                    if(self.word[j]==2):
                        pos.append(j)
                        break
                if(len(pos)==1):
                    for j in range(i+1,len(self.word)):
                        if(self.word[j]==0 or self.word[j]==1 or self.word[j]==3):
                            break
                        if(self.word[j]==2):
                            pos.append(j)
                if(len(pos)==2):
                    self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])
                
                    
    
            if(s>2):
                pos=[]             
                for j in range(i-1,-1,-1):
                    if(self.word[j]==s or self.word[j]==s-2):
                        break
                    if(s==3 and self.word[j]==0):
                        break
                    if(self.word[j]==s-1):
                        pos.append(j)
                        break
                if(len(pos)==1):
                    for j in range(i+1,len(self.word)):
                        if(self.word[j]==s or self.word[j]==s-2):
                            break
                        if(s==3 and self.word[j]==0):
                            break
                        if(self.word[j]==s-1):
                            pos.append(j)
                            break
                if(len(pos)==2):
                    self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])
            if(s==2):
                pos=[]             
                for j in range(i-1,-1,-1):
                    if(self.word[j]==s):
                        break

                    if(self.word[j]==0):
                        pos.append(j)
                        break
                if(len(pos)==1):
                    for j in range(i+1,len(self.word)):
                        if(self.word[j]==s):
                            break

                        if(self.word[j]==0):
                            pos.append(j)
                            break
                if(len(pos)==2):
                    self.r_braid_pos.append([self.r_ord[pos[0]],self.r_ord[pos[1]]])
                pos=[]             
                for j in range(i-1,-1,-1):
                    if(self.word[j]==s):
                        break

                    if(self.word[j]==1):
                        pos.append(j)
                        break
                if(len(pos)==1):
                    for j in range(i+1,len(self.word)):
                        if(self.word[j]==s):
                            break

                        if(self.word[j]==1):
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
            if(-p[i]>p[j]):
                soma+=1
    
    return soma

def generate_comm(w,perm,pos,max_length):
    if(pos==0):
        for i in range(n):
            if(i==0 and -perm[1]>perm[2]):
                perm[1],perm[2]=-perm[2],-perm[1]
                w[pos]=i
                generate_comm(w,perm,pos+1,max_length)
                perm[1],perm[2]=-perm[2],-perm[1]
            
            if(i>0 and perm[i]>perm[i+1]):
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
            if(last>0):
                if(last<n-1):
                    for i in range(last+2):
                        if(i==0 and -perm[1]>perm[2]):
                            perm[1],perm[2]=-perm[2],-perm[1]
                            w[pos]=i
                            generate_comm(w,perm,pos+1,max_length)
                            perm[1],perm[2]=-perm[2],-perm[1]
                        
                        if(i>0 and perm[i]>perm[i+1]):
                            perm[i],perm[i+1]=perm[i+1],perm[i]
                            w[pos]=i
                            generate_comm(w,perm,pos+1,max_length)
                            perm[i],perm[i+1]=perm[i+1],perm[i]
                else:
                    for i in range(last):
                        if(i==0 and -perm[1]>perm[2]):
                            perm[1],perm[2]=-perm[2],-perm[1]
                            w[pos]=i
                            generate_comm(w,perm,pos+1,max_length)
                            perm[1],perm[2]=-perm[2],-perm[1]
                        
                        if(i>0 and perm[i]>perm[i+1]):
                            perm[i],perm[i+1]=perm[i+1],perm[i]
                            w[pos]=i
                            generate_comm(w,perm,pos+1,max_length)
                            perm[i],perm[i+1]=perm[i+1],perm[i]
            else:
                if(perm[2]>perm[3]):
                    perm[2],perm[3]=perm[3],perm[2]
                    w[pos]=2
                    generate_comm(w,perm,pos+1,max_length)
                    perm[2],perm[3]=perm[3],perm[2]

def pattern_finder(w):
    #returns 0 if w is -1-2-3-4 or 1-2-3-4 avoiding; returns 1 otherwise
    if n<4:
        return 0
    
    for s in itertools.combinations([i for i in range(1,n+1)], 4):
        if 0>w[s[0]]>w[s[1]]>w[s[2]]>w[s[3]] or (0>w[s[1]]>w[s[2]]>w[s[3]] and 0<w[s[0]]<-w[s[1]]):
            return 1
        
    return 0


n=5

          

id_perm=[i for i in range(1,n+1)]
S_n=itertools.permutations(id_perm)
kk=0
for pp in S_n:
    perm=list(pp)
    perm.insert(0, 0)
    binary=itertools.product([-1,1],repeat=n)
    for b in binary:
        count=0
        for i in range(n):
            if(b[i]==-1):
                count+=1
        
        if(count%2==0):  
            binn=list(b)
            for i in range(1,n+1):
                perm[i]*=binn[i-1]
            
            if(pattern_finder(perm)==0 and perm[n]!=n):
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
                
            comm_classes=[]
            for i in range(1,n+1):
                perm[i]*=binn[i-1]



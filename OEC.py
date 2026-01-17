import sys
import copy
OEC=[]

def main():
    args = sys.argv[1:]
    valid_types = ['A', 'B', 'D']
    try:
        perm=[int(args[i]) for i in range(len(args)-1)]
        n=len(perm)
        perm.insert(0, 0)  # This will put the permutation through positions 1 to n
        tp=args[-1]
        if tp not in valid_types :
            raise TypeError

    except ValueError:
        print('Only integers are allowed.')
        return
    except TypeError:
        print('Invalid Coxeter type.')
        return

    l=length(perm,n,tp) #Coxeter length of the inserted permutation
    w=[None]*l #list that will be used to record the one-element classes
    for i in des_set(perm,n,tp):
        w[0]=i
        if i==0 and tp=='B':
            perm[1]=-perm[1]
        if i==0 and tp=='D':
            perm[1],perm[2]=-perm[2],-perm[1]
        if i>0:
            perm[i],perm[i+1]=perm[i+1],perm[i]

        oec_generator(perm, w, 1, l,n,tp)

        if i==0 and tp=='B':
            perm[1]=-perm[1]
        if i==0 and tp=='D':
            perm[1],perm[2]=-perm[2],-perm[1]
        if i>0:
            perm[i],perm[i+1]=perm[i+1],perm[i]

    for w in OEC:
        print(w)
    print('Number of one-element commutation classes of',*perm[1:],":", len(OEC))


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

def des_set(p,n,tp):
    #Computes the descend set of a permutation
    des=[]
    for i in range(1,n):
        if p[i]>p[i+1]:
            des.append(i)
    if tp=='B' and p[1]<0:
        des.append(0)
    if tp=='D' and -p[1]>p[2]:
        des.append(0)

    return des


def oec_generator(p,w,pos,max_len,n,tp):
    if pos==max_len:
        new_w=copy.deepcopy(w)
        OEC.append(new_w)
    else:
        s = w[pos - 1]  # current last letter of w
        s_plus = s + 1
        s_minus = s - 1
        if tp=='A':
            if s_plus<n:
                if p[s_plus]>p[s_plus+1]: #checks if s+1 is a descend of p
                    w[pos]=s_plus
                    p[s_plus],p[s_plus+1]=p[s_plus+1],p[s_plus]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    p[s_plus],p[s_plus+1]=p[s_plus+1],p[s_plus]
            if s_minus>0:
                if p[s_minus]>p[s_minus+1]: #checks if s-1 is a descend of p
                    w[pos]=s_minus
                    p[s_minus],p[s_minus+1]=p[s_minus+1],p[s_minus]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    p[s_minus],p[s_minus+1]=p[s_minus+1],p[s_minus]

        if tp=='B':
            if s_plus<n:
                if p[s_plus]>p[s_plus+1]: #checks if s+1 is a descend of p
                    w[pos]=s_plus
                    p[s_plus],p[s_plus+1]=p[s_plus+1],p[s_plus]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    p[s_plus],p[s_plus+1]=p[s_plus+1],p[s_plus]
            if s_minus>-1:
                if p[s_minus]>p[s_minus+1]: #checks if s-1 is a descend of p
                    w[pos]=s_minus
                    if s_minus==0:
                        p[1]=-p[1]
                    else:
                        p[s_minus],p[s_minus+1]=p[s_minus+1],p[s_minus]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    if s_minus==0:
                        p[1]=-p[1]
                    else:
                        p[s_minus],p[s_minus+1]=p[s_minus+1],p[s_minus]
        if tp=='D':
            if s_plus<n and s!=0:
                if p[s_plus]>p[s_plus+1]: #checks if s+1 is a descend of p
                    w[pos]=s_plus
                    p[s_plus],p[s_plus+1]=p[s_plus+1],p[s_plus]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    p[s_plus],p[s_plus+1]=p[s_plus+1],p[s_plus]
            elif s==0:
                if p[2]>p[3]: #in case of s=0, check if 2 is a descend of p
                    w[pos]=2
                    p[2],p[3]=p[3],p[2]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    p[2], p[3] = p[3], p[2]

            if s!=0 and s!=1:
                if p[s_minus]>p[s_minus+1]: #checks if s-1 is a descend of p
                    w[pos]=s_minus
                    p[s_minus],p[s_minus+1]=p[s_minus+1],p[s_minus]
                    oec_generator(p, w, pos+1, max_len,n,tp)
                    p[s_minus],p[s_minus+1]=p[s_minus+1],p[s_minus]
            if s==2 and -p[1]>p[2]: #in case of s=2, check if 0 is a descend of p
                w[pos]=0
                p[1],p[2]=-p[2],-p[1]
                oec_generator(p, w, pos+1, max_len,n,tp)
                p[1], p[2] = -p[2], -p[1]
            

if __name__ == "__main__":
    main()
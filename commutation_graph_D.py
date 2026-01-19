from tkinter import *
import copy
import time


'''variaveis globais'''
n=4 #ordem do grafo

nos_selecionados=[]
classes=[]
ids=[]
iterador=0

def summation(n): #devolve o fatorial de um número
    if(n==0):
        return 0
    else:
        return n+summation(n-1)

def repeticaoClasse(conj_classes,pl): #verifica se uma dada palavra pertence a alguma classe
    for cl in conj_classes:
        if cl.representante==pl:
            return cl.id
    return -1


def is_element(cj,elem): #serve para verificar se algum elemento está num conjunto
    for item in cj:
        if item==elem:
            return 1
    return 0


def comutar(pl,pos): #efetuar uma comutacao numa palavra
    aux=pl[pos]
    pl[pos]=pl[pos-1]
    pl[pos-1]=aux

def rlongar(pl,pos,tipo): #efetuar uma relação longa numa palavra 
    if(tipo==0):
        aux=pl[pos]
        pl[pos-1]=aux
        pl[pos]=pl[pos+1]
        pl[pos+1]=aux
    else:
        aux=pl[pos]
        pl[pos-1]=aux
        pl[pos]=pl[pos+1]
        pl[pos+1]=aux
        pl[pos-2]=pl[pos]

def lexicoMenorGrau(pl): #calcular o lexico de menor de uma permutação 
    lmg=copy.deepcopy(pl)
    i=0
    while(i<dim_repr-1):
        if(lmg[i]==1 and lmg[i+1]==0):
            lmg[i],lmg[i+1]=lmg[i+1],lmg[i]
            i=0
            continue
        if(lmg[i]>2 and lmg[i+1]<lmg[i]-1):
            lmg[i],lmg[i+1]=lmg[i+1],lmg[i]
            i=0
            continue
        i+=1
            
    return lmg

def conteudo(pl):  #conteudo de uma palavra
    C={}
    for i in range(0,n):
        C[i]=0
    for item in pl:
        C[item]+=1
    
    cont=int("".join(str(x) for x in C.values()))

    return cont

def repr_num(pl):  #conteudo de uma palavra
    cont=0
    for i in range(1,dim_repr+1):
        cont+=10**(dim_repr-i)*pl[i-1]
    return cont

def cone_superior(grafo,no_inicial):
    cone_sup=[]
    nos_analise=grafo.arv[no_inicial]
    nivel=grafo.conj_classes[no_inicial].nivel
    while len(nos_analise):
        aux=[]
        for no in nos_analise:
            if grafo.conj_classes[no].nivel<nivel and is_element(cone_sup,no)==0:
                cone_sup.append(no)
                aux+=grafo.arv[no]
        nos_analise=aux
        nivel-=1
    return cone_sup

def cone_inferior(grafo,no_inicial):
    cone_inf=[]
    nos_analise=grafo.arv[no_inicial]
    nivel=grafo.conj_classes[no_inicial].nivel
    while len(nos_analise):
        aux=[]
        for no in nos_analise:
            if grafo.conj_classes[no].nivel>nivel and is_element(cone_inf,no)==0:
                cone_inf.append(no)
                aux+=grafo.arv[no]
        nos_analise=aux
        nivel+=1
    return cone_inf


def cone(grafo,no_inicial):
    cone=cone_superior(grafo,no_inicial)+cone_inferior(grafo,no_inicial)
    return cone



def classe_reversa(classe,conjClasses):
    rev=copy.deepcopy(classe.representante)
    for i in range(dim_repr//2):
        aux=rev[i]
        rev[i]=rev[len(rev)-1-i]
        rev[len(rev)-1-i]=aux
        
    lmg=lexicoMenorGrau(rev)
    for cl in conjClasses:
        if(cl.representante==lmg):
            return cl.id

def find(factor,cl):
    dim=len(factor)
    j=0
    for i in cl.representante:
        if(i==n):
            continue
        if(i==factor[j]):
            j+=1
        else:
            j=0
        if(j==dim):
            return 1
            
    return 0

def k_reversa(grafo,cl):
    aux=[]
    classes=[]
    classes_2=[]
    copia=copy.deepcopy(cl)
    while(True):
        for i in range(dim_repr):
            aux.append(cl.representante[(1+i)%dim_repr])
        aux=lexicoMenorGrau(aux)
        id_found=repeticaoClasse(grafo.conj_classes,aux)
        if(id_found!=-1 and is_element(classes,id_found)==0):
            classes.append(id_found)
        else:
            break
        cl=grafo.conj_classes[id_found]
        
        aux.clear()
    
    '''
    aux.clear() 
    cl=copia
    while(True):
        for i in range(dim_repr):
            aux.append(cl.representante[(dim_repr-1+i)%dim_repr])
        aux=lexicoMenorGrau(aux)
        id_found=repeticaoClasse(grafo.conj_classes,aux)
        if(id_found!=-1 and is_element(classes_2,id_found)==0):
            classes_2.append(id_found)
        else:
            break
        cl=grafo.conj_classes[id_found]       
        aux.clear()  
    
    for cl in classes_2:
        if(is_element(classes,cl)==0):
            classes.append(cl)
    '''        
    return classes

def k_reversa_2(grafo,cl):
    aux=[]
    classes=[]
    classes_2=[]
    copia=copy.deepcopy(cl)
    while(True):
        for i in range(dim_repr):
            aux.append(cl.representante[(1+i)%dim_repr])
        aux=lexicoMenorGrau(aux)
        id_found=repeticaoClasse(grafo.conj_classes,aux)
        if(id_found!=-1 and is_element(classes,id_found)==0):
            classes.append(id_found)
        else:
            break
        cl=grafo.conj_classes[id_found]
        
        aux.clear()
        
    aux.clear() 
    cl=copia
    while(True):
        for i in range(dim_repr):
            aux.append(cl.representante[(dim_repr-1+i)%dim_repr])
        aux=lexicoMenorGrau(aux)
        id_found=repeticaoClasse(grafo.conj_classes,aux)
        if(id_found!=-1 and is_element(classes_2,id_found)==0):
            classes_2.append(id_found)
        else:
            break
        cl=grafo.conj_classes[id_found]       
        aux.clear()  
            
    return len(classes), len(classes_2)
     
def gerar_subgrafo(grafo,cl,n_niveis):
    subgrafo=[]
    aux=[]
    filhos=grafo.arv[cl.id]
    for j in range(n_niveis):
        for no in filhos:
            if(is_element(subgrafo,no)==0):
                subgrafo.append(no)
                aux+=grafo.arv[no]
        filhos=aux
        aux=[]
    return subgrafo

def soma_2(rep):
    aux=[i for i in range(1,n+1)]
    soma=0
    negativos=0
    soma_pos=0
    positive=[]
    double_negativos=[]
    for i in rep:
        if(i==0):
            aux[0]=-aux[0]
            continue
        else:
            aux[i-1],aux[i]=aux[i],aux[i-1]
        
        if(aux[i-1]<0 or aux[i]<0):
            soma+=-i+1
            negativos+=1
            if(aux[i-1]<0 and aux[i]<0):
                double_negativos.append(i)
            
        else:
            soma+=i
            positive.append(i)
            soma_pos+=i
            
    
    
    return soma,negativos,positive,soma_pos,double_negativos

def ordem_neg(rep):
    aux=[i for i in range(1,n+1)]    
    contagem={}
    for i in range(1,n+1):
        contagem[i]=0
    
    for i in rep:
        if(i==0):
            aux[0]=-aux[0]
        else:
            aux[i-1],aux[i]=aux[i],aux[i-1]    
        for ii in range(1,n+1):
            if(aux[ii-1]==-ii):
                contagem[ii]+=1
    return contagem

class Node:
    def __init__(self,x,y,diam,cv,classe):       
        self.id=classe.id #classe associada ao nó
        self.classe=classe
        self.center=[x,y] #centro do nó
        self.diam=diam #diametro do nó
        self.cv=cv #canvas onde será desenhado o nó
        self.is_select=False #serve para ver quando o nó está selecionado
    def draw(self):
        #desenha o nó no canvas
        self.no=self.cv.create_oval(self.center[0]-self.diam,self.center[1]+self.diam,self.center[0]+self.diam,self.center[1]-self.diam,fill='blue',tag="no"+str(self.id), width=4)
        #desenha o id dentro do nó
        self.num=self.cv.create_text(self.center[0],self.center[1],fill='white',tag="no"+str(self.id)+'t',text=str(self.id),font='bold 10')
    def move(self,nv_ct): #define um novo centro para depois mover o nó
        self.cv.delete("no"+str(self.id))
        self.cv.delete("no"+str(self.id)+'t')
        self.center=nv_ct 

        
class Line:
    def __init__(self,x1,y1,x2,y2,cv,no1,no2,cor):
        self.P1=[x1,y1] #extremidade da linha
        self.P2=[x2,y2] #outra extremidade da linha
        self.no1=no1 #no de partida
        self.no2=no2 #no de chegada
        self.cv=cv #canvas onde vai ser desenhado a linha
        self.cor=cor #0 se for preto e 1 se for vermelho
    def draw(self):
        #desenhar a linha no canvas
        if(self.cor==0):
            self.linha=self.cv.create_line(self.P1[0],self.P1[1],self.P2[0],self.P2[1],width=2,fill="black")
            
        else:
            self.linha=self.cv.create_line(self.P1[0],self.P1[1],self.P2[0],self.P2[1],width=2,fill="red")
    def move(self,nv_ct,p):
        #mover a linha. Será necessário apenas mudar um ponto de momento
        self.cv.delete(self.linha)
        if p==1:
            self.P1=nv_ct
        if p==2:
            self.P2=nv_ct
        
        self.draw() #desenhar primeiro as linhas para não se sobreporem aos nós  
        
class Classe:
    def __init__(self,representante,id):
        self.id=id
        self.representante=lexicoMenorGrau(representante) #representante da classe que seráo lexico de menor grau
        self.rep_numerica="".join(str(x) for x in self.representante)
        self.conteudo=conteudo(representante)
        self.conj_palavras=[self.representante] #conjunto das palavras da classse
        self.filhos=[] #lista de tuplos que contem cada filho e a respetiva relação longa   
        self.dim=0 #dimensao da classe     
        self.grau=0
        self.excentrecidade=0
        self.distancia_excentrecidade=0       
        self.soma=sum(i for i in representante)
        self.soma_2,self.sinais_negativos,self.positive,self.soma_pos,self.double_negativos=soma_2(self.representante)
        self.cone=[] 
        self.reversa=0 #id da classe reversa
        self.nivel=0 #nivel que ocupa no grafo   
        self.fat=0 #numero de fatoriais
        
        
    def gerarClasse(self): #gera toda a classe
        k=0
        while(k<len(self.conj_palavras)):
            pl=self.conj_palavras[k]
            for j in range(1,dim_repr):
                if(abs(pl[j-1]-pl[j])>1):
                    if((pl[j-1]==0 and pl[j]==2) or (pl[j-1]==2 and pl[j]==0)):
                        continue
                    else:
                        nv_pl=copy.deepcopy(pl)
                        comutar(nv_pl,j)
                        if(is_element(self.conj_palavras,nv_pl)==0):
                            self.conj_palavras.append(nv_pl)       
                else:
                    if((pl[j-1]==0 and pl[j]==1) or (pl[j-1]==1 and pl[j]==0)):
                        nv_pl=copy.deepcopy(pl)
                        comutar(nv_pl,j)
                        if(is_element(self.conj_palavras,nv_pl)==0):
                            self.conj_palavras.append(nv_pl)   
                                               
            k=k+1
                    
        #preenchimento de algumas estatisticas
            #calcular dimensao da classe
        self.dim=len(self.conj_palavras)   
            
            
            #calcular o úmero de fatoriais no representante
        for i in range(n-1,dim_repr):
            if(self.representante[i]==0):
                prod=0
                for j in range(i-(n-1),i+1):
                    prod+=self.representante[j]
                if(prod==summation(n-1)):
                    self.fat+=1
                  
                
        
class Grafo:
    def __init__(self,c0):
        self.conj_classes=[c0]
        self.arv={}
        self.niveis={}
        self.raio=0
        self.diametro=0
        self.nos=[]
        self.linhas=[]
        self.num_nos_selecionados=0
        
    def gerarGrafo(self):
        k=0
        self.niveis[1]=[0]
        self.conj_classes[0].nivel=1
        id_atual=0
        cont=0
        while(k<len(self.conj_classes)):    
            cl=self.conj_classes[k]
            self.arv[k]=[]
            for pl in cl.conj_palavras:
                for i in range(2,dim_repr):
                    if(pl[i]==pl[i-2] and abs(pl[i]-pl[i-1])==1 and pl[i]!=0 and pl[i-1]!=0): #relações longas do tipo 0
                        nv_pl=copy.deepcopy(pl)
                        rlongar(nv_pl,i-1,0)
                        nv_pl=lexicoMenorGrau(nv_pl)
                        id_rep=repeticaoClasse(self.conj_classes,nv_pl) #devolve o id da classe a que a palavra pertence ou -1 caso não pertença a nenhuma
                        if(id_rep==-1):
                            id_atual+=1
                            nv_cl=Classe(nv_pl,id_atual)
                            nv_cl.gerarClasse()
                            nv_cl.nivel=cl.nivel+1
                            if(is_element(self.niveis.keys(),nv_cl.nivel)==0): #caso ainda não tenha sido criada memoria para o nivel do novo nó
                                self.niveis[nv_cl.nivel]=[id_atual]
                            else:
                                self.niveis[nv_cl.nivel].append(id_atual)
                            self.conj_classes.append(nv_cl)
                           
                                
                            cl.filhos.append((id_atual,0))
                            cont+=1
                            self.arv[k].append(id_atual)
                        else:
                            if(is_element(self.arv[k],id_rep)==0):
                                self.arv[k].append(id_rep)
                                if(is_element(cl.filhos,id_rep)==0 and id_rep>k):
                                    cl.filhos.append((id_rep,0))
                                    cont+=1
                             
                    
                    if(pl[i]==pl[i-2] and abs(pl[i]-pl[i-1])==2): #relações longas do tipo 1
                        if((pl[i-1]==0 and pl[i]==2) or (pl[i-1]==2 and pl[i]==0)):
                            nv_pl=copy.deepcopy(pl)
                            rlongar(nv_pl,i-1,0)  
                            nv_pl=lexicoMenorGrau(nv_pl)
                            id_rep=repeticaoClasse(self.conj_classes,nv_pl) #devolve o id da classe a que a palavra pertence ou -1 caso não pertença a nenhuma
                            if(id_rep==-1):
                                id_atual+=1   
                                nv_cl=Classe(nv_pl,id_atual)
                                nv_cl.gerarClasse()
                                nv_cl.nivel=cl.nivel+1
                                if(is_element(self.niveis.keys(),nv_cl.nivel)==0): #caso ainda não tenha sido criada memoria para o nivel do novo nó
                                    self.niveis[nv_cl.nivel]=[id_atual]                             
                                else:
                                    self.niveis[nv_cl.nivel].append(id_atual)
                                self.conj_classes.append(nv_cl)
                                
                                cl.filhos.append((id_atual,0))
                                cont+=1
                                self.arv[k].append(id_atual)
                            else:
                                if(is_element(self.arv[k],id_rep)==0):
                                    self.arv[k].append(id_rep)
                                    if(is_element(cl.filhos,id_rep)==0 and id_rep>k):
                                        cl.filhos.append((id_rep,0))
                                        cont+=1
            cl.grau=len(self.arv[k])                     
            k+=1
        

        for cl in self.conj_classes:
            i=cl.id
            self.conj_classes[i].ligacoes=self.arv[i]
            #self.conj_classes[i].excentrecidade,self.conj_classes[i].distancia_excentrecidade=excentrecidade_classe(self.arv,i)
            cl.reversa=classe_reversa(cl,self.conj_classes)
            cl.cone=cone(self,cl.id)
        
        
    def Raio(self):
        self.raio=self.conj_classes[0].distancia_excentrecidade
        for cl in self.conj_classes:
            if(cl.distancia_excentrecidade<self.raio):
                self.raio=cl.distancia_excentrecidade
    def Diametro(self):
        self.diametro=self.conj_classes[0].distancia_excentrecidade
        for cl in self.conj_classes:
            
            if(cl.distancia_excentrecidade>self.diametro):
                self.diametro=cl.distancia_excentrecidade

      



def inSet(cj,elem): #serve para verificar se algum elemento está num conjunto
    for item in cj:
        if item==elem:
            return 1
    return 0

def minDistancia(dis,spt): #usada na função Disjktra
    no=0
    minimo=10000
    for i in range(len(dis)):
        if(inSet(spt,i)==0 and dis[i]<minimo):
            no=i
            minimo=dis[i]
    return no

def Disjktra(Arv,no_inicial): #Calcula o caminho mais curto do no_inicial a todos os outros nós
    spt=[]
    dis={}
    n_no=len(Arv)
    percursos={}
    for i in range(n_no):
        if i==no_inicial:
            dis[i]=0
            percursos[i]=[i]
        else:
            dis[i]=100000
            percursos[i]=[]

    while(len(spt)<n_no):
        no=minDistancia(dis,spt)
        spt.append(no)
        for j in Arv[no]:
            if inSet(spt,j)==0:
                if(dis[j]==100000):
                    dis[j]=0
                if(dis[j]+1+dis[no]<dis[no]):
                    dis[j]+=1+dis[no]
                    percursos[j]+=percursos[no]
                    percursos[j].append(j)
                else:
                    dis[j]=1+dis[no]
                    percursos[j]=copy.deepcopy(percursos[no])
                    percursos[j].append(j)
    return percursos

def excentrecidade_classe(Arv,no):
    p=Disjktra(Arv,no)
    max_dis=len(p[0])
    no_mais_longe=0
    for i in range(len(p)):
        if len(p[i])>max_dis:
            max_dis=len(p[i])
            no_mais_longe=i
    return no_mais_longe,max_dis

def desenharGrafo(grafo,diam,x0,y0,dx,dy,cv):
    for i,lv in grafo.niveis.items():
        dim=len(lv)
        k=0
        if(dim%2):
            for j in range(-(dim-1)//2,(dim-1)//2+1):
                nv_no=Node(x0+j*dx,y0+i*dy,diam,cv,grafo.conj_classes[lv[k]])
                grafo.nos.append(nv_no)
                k+=1
                
        else:
            for j in range(-(dim)//2,(dim)//2+1):
                if(j==0):
                    continue
                nv_no=Node(x0+j*dx,y0+i*dy,diam,cv,grafo.conj_classes[lv[k]])
                grafo.nos.append(nv_no)
                k+=1
                
    for i in range(len(grafo.conj_classes)):
        cl=grafo.conj_classes[i]
        for tup in cl.filhos: 
            nv_ln=Line(grafo.nos[i].center[0],grafo.nos[i].center[1],grafo.nos[tup[0]].center[0],grafo.nos[tup[0]].center[1],cv,i,tup[0],tup[1])
            grafo.linhas.append(nv_ln)
    
    for linha in grafo.linhas:
        linha.draw()
        
    for no in grafo.nos:
        no.draw()
    

def minDistancia(dis,spt): #usada na função Disjktra
    no=0
    minimo=10000
    for i in range(len(dis)):
        if(is_element(spt,i)==0 and dis[i]<minimo):
            no=i
            minimo=dis[i]
    return no

def Disjktra(Arv,no_inicial): #Calcula o caminho mais curto do no_inicial a todos os outros nós
    spt=[]
    dis={}
    n_no=len(Arv)
    percursos={}
    for i in range(n_no):
        if i==no_inicial:
            dis[i]=0
            percursos[i]=[i]
        else:
            dis[i]=100000
            percursos[i]=[]

    while(len(spt)<n_no):
        no=minDistancia(dis,spt)
        spt.append(no)
        for j in Arv[no]:
            if is_element(spt,j)==0:
                if(dis[j]==100000):
                    dis[j]=0
                if(dis[j]+1+dis[no]<dis[no]):
                    dis[j]+=1+dis[no]
                    percursos[j]+=percursos[no]
                    percursos[j].append(j)
                else:
                    dis[j]=1+dis[no]
                    percursos[j]=copy.deepcopy(percursos[no])
                    percursos[j].append(j)
    return percursos
'''******Funções para verificar repetições*******'''       

def limpar(grafo,cv,root):
    for node in grafo.nos:
        cv.itemconfig(node.no, fill='blue')
    clear_screen(cv,grafo,root)


def clear_screen(grafo,cv,root):
    for node in grafo.nos:
        cv.itemconfig(node.no ,outline="black",width=4)
        
    lista = root.pack_slaves()
    for i in range(1,len(lista)):
        
        lista[i].destroy() #corresponde aos labels de ajuda
    cv.delete("legenda")
    for i in range(1,5):
        cv.delete("legenda"+str(i))
    cv.delete("info")

def transparente(grafo,cv):
    for node in grafo.nos:
        cv.itemconfig(node.no, fill='light blue')


       
'''******Funções para os menus*******'''  
def Ativar_mostrarInfo(grafo,cv,root):
    clear_screen(grafo,cv,root) 
    transparente(grafo,cv)
    #criação das legendas e labels
    off_set=33
    cv.create_oval(35,35-off_set,45,45-off_set,fill='red',width=2, tag="legenda")
    cv.create_text(115,40-off_set,text="Classe selecionada", tag="legenda")
    cv.create_oval(35,55-off_set,45,65-off_set,fill='blue',width=2,tag="legenda")
    cv.create_text(85,60-off_set,text="Vizinhos", tag="legenda")
    cv.create_oval(35,75-off_set,45,85-off_set,fill='green',width=2,tag="legenda")
    cv.create_text(105,80-off_set,text="Classe reversa", tag="legenda")
    cv.create_oval(35,95-off_set,45,105-off_set,fill='orange',width=2,tag="legenda")
    cv.create_text(110,100-off_set,text="Vizinhos reversa", tag="legenda")
    status=Label(root,text="Selecione uma classe para obter a sua informação",bd=3,relief=SUNKEN,anchor=W,font=8)
    status.pack(side=TOP)
    #criação dos eventos para cada nó
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,1))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,1))
    


def mostrarInfo(event,cv,grafo,node,is_transparent):
    #limpar o ecrã
    cv.delete("info")
    if(is_transparent):
        transparente(grafo,cv)
        for no in grafo.nos:
            cv.itemconfig(no.no ,outline="black")
        
    else:
        for no in grafo.nos:
            cv.itemconfig(no.no ,outline="black")
            
    
    #criar o texto 
    cl=node.classe
    perm=[]
    for i in cl.representante:
        if(i!=0):
            perm.append(i)
    classess=k_reversa(grafo,cl)
    perm=[i for i in range(1,n+1)]
    ordem=[]
    for s in cl.representante:
        if(s!=0):
            perm[s-1], perm[s] = perm[s], perm[s-1]
        else:
            perm[0],perm[1]=-perm[1],-perm[0]
            ordem.append(perm[0])
        
    prod=1
    for i in cl.representante:
        prod*=i
        
    txt="Representante: "+str(cl.rep_numerica)+"\n"+"Dimensao da classe: "+str(cl.dim)+"\n"+"Nível: "+str(cl.soma_2)+"\n"+"Conteudo: "+str(cl.conteudo)+"\nGrau: "+str(cl.grau)+"\nDimensão do cone: "+str(len(cl.cone))+"\nProduto: "+str(prod)+"\nGeradores positivos: "+str(cl.positive)
    cv.create_text(1560,80,text=txt,tag="info",font='bold 11')
    
    #criar a modificação da permutação identidade dada uma palavra
    x=1740
    y=15
    center=[x,y]
    diam=6
    perm=[i for i in range(1,n+1)]

    for i in range(1,n+1):
        no=cv.create_oval(center[0]-diam,center[1]+diam,center[0]+diam,center[1]-diam,fill='black',tag="info", width=4)
        num=cv.create_text(center[0],center[1],fill='white',tag="info",text=str(perm[i-1]),font='bold 10')
        center[0]=x+20*i
    
    dy=1
    
    for s in cl.representante:
        if(s!=0):
            perm[s-1], perm[s] = perm[s], perm[s-1]
        else:
            perm[0],perm[1]=-perm[1],-perm[0]
        
        center[0]=x
        center[1]=y+20*dy
        '''
        cor="red"
        for i in range(n):
            if(abs(perm[i])!=n-i):
                cor="black"
                break
        '''    
        pal={-1: "yellow", -2: "orange", -3: "red", -4: "purple",-5:"blue", -6: "green"}
        for i in range(1,n+1):
            if(perm[i-1]<0):
                cor=pal[perm[i-1]]
            else:
                cor="black"
            no=cv.create_oval(center[0]-diam,center[1]+diam,center[0]+diam,center[1]-diam,fill=cor,tag="info", width=4)
            num=cv.create_text(center[0],center[1],fill='white',tag="info",text=str(perm[i-1]),font='bold 10')
            center[0]=x+20*i
        
        dy+=1
    
    if(is_transparent==1):
        #for i in classess:
        #    cv.itemconfig("no"+str(i), fill='red',outline="white")
            
        cv.itemconfig("no"+str(node.id), fill='red')
        for i in grafo.arv[cl.id]:
            cv.itemconfig("no"+str(i), fill='blue')
        
        id_rv=cl.reversa
        cv.itemconfig("no"+str(id_rv),fill='green')
        for i in grafo.arv[id_rv]:
            cv.itemconfig("no"+str(i), fill='orange')
    else:
        cv.itemconfig("no"+str(node.id), outline="white")
    
        
def Ativar_Cone(grafo,cv,root):
    clear_screen(grafo,cv,root)
    transparente(grafo,cv)
    #legendas
    cv.create_oval(35,35,45,45,fill='green',width=2, tag="legenda")
    cv.create_text(170,40,text="Classe selecionada", tag="legenda")
    cv.create_oval(35,55,45,65,fill='blue',width=2,tag="legenda")
    cv.create_text(170,60,text="Elemento do cone da classe", tag="legenda")
    cv.create_oval(35,75,45,85,fill='orange',width=2,tag="legenda")
    cv.create_text(170,80,text="Classe  reversa", tag="legenda")
    cv.create_oval(35,95,45,105,fill='red',width=2,tag="legenda")
    cv.create_text(170,100,text="Elemento do cone da reversa", tag="legenda")
    cv.create_oval(35,115,45,125,fill='purple',width=2,tag="legenda")
    cv.create_text(170,120,text="Elemento em comum nos dois cones", tag="legenda")

    status=Label(root,text="Selecione um nó para obter o seu cone",bd=3,relief=SUNKEN,anchor=W,font=8)
    status.pack(side=TOP)
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,node=no: Cone(event,cv,grafo,node))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,node=no: Cone(event,cv,grafo,node))
    
def Cone(event,cv,grafo,node):
    transparente(grafo,cv)
            
    cv.itemconfig("no"+str(node.id),fill='green')
    
    for i in node.classe.cone:
        cv.itemconfig("no"+str(i), fill='blue')
    
    id_rv=node.classe.reversa
    cv.itemconfig("no"+str(id_rv),fill='orange')
    
    for i in grafo.conj_classes[id_rv].cone:
        cv.itemconfig("no"+str(i), fill='red')
    
    for j in node.classe.cone:
        if(is_element(grafo.conj_classes[id_rv].cone,j)):
            cv.itemconfig("no"+str(j), fill='purple')

def Ativar_mostarCaminhoMaisCurto(grafo,cv,root):
    clear_screen(grafo,cv,root)
    transparente(grafo,cv)
    #legendas
    cv.create_oval(35,35,45,45,fill='blue',width=2, tag="legenda")
    cv.create_text(115,40,text="Classe selecionada", tag="legenda")

    status=Label(root,text="Selecione duas classes para obter um caminho mais curto",bd=3,relief=SUNKEN,anchor=W,font=8)
    status.pack(side=TOP)
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,node=no: mostrarCaminhoMaisCurto(event,cv,grafo,node))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,node=no: mostrarCaminhoMaisCurto(event,cv,grafo,node))
    
def mostrarCaminhoMaisCurto(event,cv,grafo,node):
    nos_selecionados.append(node.id)
    dim=len(nos_selecionados)
    if dim==3:
        nos_selecionados.clear()
        nos_selecionados.append(node.id)
        transparente(grafo,cv)

    cv.itemconfig("no"+str(node.id),fill='blue')

    if dim==2: 
        percursos=Disjktra(grafo.arv,nos_selecionados[0])
        i=0
        for no in percursos[nos_selecionados[1]]:
            if i!=0 and i!=len(percursos[nos_selecionados[1]])-1:
                cv.itemconfig("no"+str(no),fill='red')
            i+=1
            
def Ativar_procurar_palavra(grafo,root,cv):
    clear_screen(grafo,cv,root)
    transparente(grafo,cv)
    L1 = Label(root, text="Insira uma palavra",bd=1)
    L1.pack( side = LEFT)
    txt=IntVar()
    ent=Entry(root,textvariable=txt,bd=5,validate="key")
    ent.pack(side=LEFT)
    but=Button(root,text="Procurar",command=lambda:procurar_palavra(ent,grafo,cv))
    but.pack(side=LEFT)

def procurar_palavra(e,grafo,cv):
    transparente(grafo,cv)
    w=e.get()
    p=[]
    for i in w:
        i=int(i)
        p.append(i)
    for no in grafo.nos:
        if lexicoMenorGrau(p)==grafo.conj_classes[no.id].representante:
            cv.itemconfig("no"+str(no.id), fill='red')
            break

def colorir_soma(grafo,cv,root):
    palete={24:"red",23:"orange",22:"green",21:"blue",20:"purple"}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(70,25,text="Somas",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=20
        y2+=20
    

    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id),fill=palete[grafo.conj_classes[no.id].soma])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
 
def colorir_soma_2(grafo,cv,root):
    palete={-12:'#%02x%02x%02x' % (255,51,51),
            -11:'#%02x%02x%02x' % (255,153,51),
            -10:'#%02x%02x%02x' % (255,255,51),
            -9:'#%02x%02x%02x' % (153,255,51),
            -8:'#%02x%02x%02x' % (51,255,51),
            -7:'#%02x%02x%02x' % (51,255,153),
            -6:'#%02x%02x%02x' % (51,255,255),
            -5:'#%02x%02x%02x' % (51,153,255),
            -4:'#%02x%02x%02x' % (51,51,255),
            -3:'#%02x%02x%02x' % (153,51,255),
            -2:'#%02x%02x%02x' % (255,51,255),
            -1:'#%02x%02x%02x' % (255,51,153),
             0:'#%02x%02x%02x' % (255,0,127),
             1:'#%02x%02x%02x' % (255,0,255),
             2:'#%02x%02x%02x' % (127,0,255),
             3:'#%02x%02x%02x' % (0,0,255),
             4:'#%02x%02x%02x' % (0,128,255),
             5:'#%02x%02x%02x' % (0,255,255),
             6:'#%02x%02x%02x' % (0,128,255),
             7:'#%02x%02x%02x' % (0,255,0),
             8:'#%02x%02x%02x' % (0,0,255),
             9:'#%02x%02x%02x' % (128,255,0),
            10:'#%02x%02x%02x' % (255,225,0),
            }
    
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(75,25,text="Nível",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=15
        y2+=15
    
    for no in grafo.nos:
       cv.itemconfig("no"+str(no.id),fill=palete[grafo.conj_classes[no.id].soma_2])
       cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
       cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))

def colorir_dimensao(grafo,cv,root):
    palete={1:'#%02x%02x%02x' % (0,0,255),2:'#%02x%02x%02x' % (0,0,255), 4:'#%02x%02x%02x' % (0,128,255), 8:'#%02x%02x%02x' % (0,255,255), 16:'#%02x%02x%02x' % (0,255,128), 32:'#%02x%02x%02x' % (0,255,0),64:'#%02x%02x%02x' % (128,255,0),128:'#%02x%02x%02x' % (255,255,0),264:'#%02x%02x%02x' % (255,128,0),512:'#%02x%02x%02x' % (255,0,0),1024:'#%02x%02x%02x' % (0,0,0),2048:'#%02x%02x%02x' % (0,0,0)}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(75,25,text="Dimensões das classes",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        if(k==1 or k==2048):
            continue
        if(k==2):
            cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
            cv.create_text(x1+45,y2-5,text="<"+str(k), tag="legenda")
        elif(k<1024):
            cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
            cv.create_text(x1+45,y2-5,text="["+str(ant)+","+str(k)+"[", tag="legenda")
        else:
            cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
            cv.create_text(x1+45,y2-5,text=str(ant)+"<=", tag="legenda")
        y1+=20
        y2+=20
        ant=k
    
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        for i in range(1,len(key_list)):
            if(grafo.conj_classes[no.id].dim>=key_list[i-1] and grafo.conj_classes[no.id].dim<key_list[i]):
                cv.itemconfig("no"+str(no.id),fill=palete[key_list[i]])
        

def colorir_relacoes_longas(grafo,cv,root):
    palete={1:"orange",2:"green",3:"blue",4:"purple", 5: "red", 6: "black"}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(100,25,text="Números de relações longas",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=20
        y2+=20
    

    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id),fill=palete[grafo.conj_classes[no.id].grau])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))

def colorir_conteudo(grafo,cv,root):
    palete={4444: "red", 4453:"orange", 4543:"green", 4462:"dark green", 4552:"blue", 4633:"dark blue", 4642:"purple"}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(60,15,text="Conteúdos",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=20
        y2+=20
    

    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id),fill=palete[grafo.conj_classes[no.id].conteudo])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))


def colorir_fat(grafo,cv,root):
    palete={1:"orange",2:"green",3:"blue",4:"purple"}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(70,25,text="Número de fatorias",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=20
        y2+=20
    

    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id),fill=palete[grafo.conj_classes[no.id].fat])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))

def colorir_tipoA(grafo,cv,root):
    clear_screen(grafo,cv,root)
    transparente(grafo,cv)
    classes=[]
    aux2=[i for i in range(n,0,-1)]
    for cl in grafo.conj_classes:
        for pl in cl.conj_palavras:
            aux1=[i for i in range(1,n+1)]
            perm=[]
            cont=0
            for i in pl:
                if i!=0:
                    perm.append(i)
                    cont+=1
                if(cont==6):
                    break
            for i in perm:
                aux1[i-1],aux1[i]=aux1[i],aux1[i-1]
            if(aux1==aux2):
                classes.append(cl)
                break
            
    for cl in classes:
        cv.itemconfig("no"+str(cl.id),fill="green")
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))



def colorir_B3(grafo,cv,root):
    clear_screen(grafo,cv,root)
    transparente(grafo,cv)
    classes=[]
    ft=[3,2,1,0,1,2,3]
    g3=[[0, 1, 0, 2, 1, 0, 2, 1, 2],[0, 1, 0, 2, 1, 0, 1, 2, 1],[0, 1, 0, 1, 2, 1, 0, 1, 2],
        [0, 1, 2, 1, 0, 1, 0, 2, 1],[1, 0, 1, 0, 2, 1, 0, 1, 2],[0, 2, 1, 0, 2, 1, 0, 2, 1],
        [1, 0, 1, 2, 1, 0, 1, 0, 2],[0, 2, 1, 0, 1, 2, 1, 0, 1],[1, 0, 2, 1, 0, 2, 1, 0, 2],
        [2, 1, 0, 1, 0, 2, 1, 0, 1],[1, 0, 2, 1, 0, 1, 2, 1, 0],[2, 1, 0, 1, 2, 1, 0, 1, 0],
        [1, 2, 1, 0, 1, 0, 2, 1, 0],[2, 1, 0, 2, 1, 0, 2, 1, 0]]
    for pl in g3:
        for i in range(9):
            aux=[]
            for j in range(i):
                aux.append(pl[j])
            for k in ft:
                aux.append(k)
            for j in range(i,9):
                aux.append(pl[j])
            aux=lexicoMenorGrau(aux)
            cl_id=repeticaoClasse(grafo.conj_classes,aux)
            if(cl_id>=0):
                if(is_element(classes,grafo.conj_classes[cl_id])==0):
                    classes.append(grafo.conj_classes[cl_id])
    print(len(classes))
    for cl in classes:
        cv.itemconfig("no"+str(cl.id),fill="red")
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))    

def colorir_neg(grafo,cv,root):
    palete={0:"red",1:"orange",2:"yellow",3:"green",4:"blue", 5:"purple",6:"black"}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(120,25,text="Número de geradores positivos",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=20
        y2+=20
    
   
    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id),fill=palete[len(no.classe.positive)])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
    

def colorir_soma_pos(grafo,cv,root):
    palete={0:'#%02x%02x%02x' % (255,51,51),
            1:'#%02x%02x%02x' % (255,153,51),
            2:'#%02x%02x%02x' % (255,255,51),
            3:'#%02x%02x%02x' % (153,255,51),
            4:'#%02x%02x%02x' % (51,255,51),
            5:'#%02x%02x%02x' % (51,255,153),
            6:'#%02x%02x%02x' % (51,255,255),
            7:'#%02x%02x%02x' % (51,153,255),
            8:'#%02x%02x%02x' % (51,51,255),
            9:'#%02x%02x%02x' % (153,51,255),
            10:'#%02x%02x%02x' % (255,51,255),
            11:'#%02x%02x%02x' % (255,51,153),
             12:'#%02x%02x%02x' % (255,0,127),
             13:'#%02x%02x%02x' % (255,0,255),
             14:'#%02x%02x%02x' % (127,0,255)}
    clear_screen(grafo,cv,root)
    #legenda
    cv.create_text(70,25,text="Número de geradores positivos",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda")
        cv.create_text(x1+30,y2-5,text=str(k), tag="legenda")
        y1+=20
        y2+=20
    
    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id),fill=palete[grafo.conj_classes[no.id].soma_pos])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
    
def Ativar_cls(grafo,root,cv):
    global iterador,ids
    iterador=0
    ids=[]
    clear_screen(grafo,cv,root)
    transparente(grafo,cv)
    for no in grafo.nos:       
        #cv.itemconfig("no"+str(no.id),fill=palete[len(no.classe.positive)])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
    
    cv.create_text(45,25,text="Iteração: ",tag="legenda")
    cv.create_text(85,25,text="0",tag="it")
    but=Button(root,text="Próxima",command=lambda:iterar(grafo,cv))
    but.pack(side=LEFT)
    but2=Button(root,text="Anterior",command=lambda:atrasar(grafo,cv))
    but2.pack(side=LEFT)
    txt=IntVar()
    ent=Entry(root,textvariable=txt,bd=5,validate="key")
    ent.pack(side=LEFT)
    but3=Button(root,text="Ir para a iteração",command=lambda:avancar(ent,grafo,cv))
    but3.pack(side=LEFT)

def avancar(e,grafo,cv):
    global iterador, ids
    ids=[]
    transparente(grafo,cv)
    w=e.get()
    iterador=int(w)
    for i in range(iterador):
        aux=lexicoMenorGrau(classes[i])
        cl_id=repeticaoClasse(grafo.conj_classes,aux)
        if(cl_id>=0):
            if(is_element(ids,cl_id)==0):
                  ids.append(cl_id)
                  
                  #contador+=1
                  cv.itemconfig("no"+str(cl_id),fill="red")
                   
            else:
                cv.itemconfig("no"+str(cl_id),fill="orange")
                #print(cl_id,"rep")
                #rep+=1
                
                
                
        else:
            print(cl)

    cv.delete("it")
    cv.create_text(85,25,text=str(iterador),tag="it")
    

def iterar(grafo,cv):
    global iterador,ids
    aux=lexicoMenorGrau(classes[iterador])
    cl_id=repeticaoClasse(grafo.conj_classes,aux)
    if(cl_id>=0):
        if(is_element(ids,cl_id)==0):
              ids.append(cl_id)

              #contador+=1
              cv.itemconfig("no"+str(cl_id),fill="red")
               
        else:
            cv.itemconfig("no"+str(cl_id),fill="orange")
            #print(cl_id,"rep")
            #rep+=1
            
            
            
    else:
        print(cl)
    iterador+=1
    cv.delete("it")
    cv.create_text(85,25,text=str(iterador),tag="it")
    

def atrasar(grafo,cv):
    global iterador,ids
    iterador=iterador-1
    aux=lexicoMenorGrau(classes[iterador])
    cl_id=repeticaoClasse(grafo.conj_classes,aux)
    cv.itemconfig("no"+str(cl_id),fill="light blue")
    for i in range(len(ids)):
        if(ids[i]==cl_id):
            ids.pop(i)
            
    cv.delete("it")
    cv.create_text(85,25,text=str(iterador),tag="it")


def colorir_cl(grafo,cv,root):
    palete={0:"red",1:"orange",2:"yellow",3:"green",4:"blue", 5:"purple",6:"black"}
    clear_screen(grafo,cv,root)
    classes=[]
    #legenda
    cv.create_text(120,25,text="Classes",tag="legenda")
    key_list=list(palete.keys())
    file1 = open('Classes.txt', 'r')
    Lines = file1.readlines()
    count=0
    cl=[]
    classes=[]
    ids=[]
    rep=0
    
    
    for line in Lines:
        if(count<16):
            line=int(line)
            cl.append(line)
            count+=1
            
        else:
            classes.append(cl)
            cl=[]
            line=int(line)
            cl.append(line)
            count=1
            
    classes.append(cl)       
    contador=0
    
    print(len(classes))
    for cl in classes:
        aux=lexicoMenorGrau(cl)
        cl_id=repeticaoClasse(grafo.conj_classes,aux)
        if(cl_id>=0):
            if(is_element(ids,cl_id)==0):
               ids.append(cl_id)
               contador+=1

               cv.itemconfig("no"+str(cl_id),fill="red")
               
            else:
                cv.itemconfig("no"+str(cl_id),fill="orange")
                #print(cl_id,"rep")
                rep+=1
            
            
            
        else:
            print(cl)
    print(contador,rep)

        
        
    for no in grafo.nos:       
        #cv.itemconfig("no"+str(no.id),fill=palete[len(no.classe.positive)])
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,no_aux=no: mostrarInfo(event,cv,grafo,no_aux,0))           
    
    file1.close()

def Ativar_Marcar(grafo,cv,root):
    clear_screen(grafo,cv,root)
    palete={1:"white",2:"black",3:"yellow",4:"dark green"}
    #legenda
    cv.create_text(70,25,text="Palete",tag="legenda")
    x1=35
    y1=35
    x2=45
    y2=45
    key_list=list(palete.keys())
    for k in key_list:
        cv.create_oval(x1,y1,x2,y2,fill=palete[k],width=2, tag="legenda"+str(k))
        y1+=20
        y2+=20
    
    for k in key_list:
        cv.tag_bind("legenda"+str(k),'<Button-1>', lambda event,i=k: mudanca_cor(event,grafo,cv,palete[i]))
        
    for no in grafo.nos:
        cv.itemconfig("no"+str(no.id), width=0)
        
        
    
def marcar(event,cv,grafo,node,cor):
    cv.itemconfig("no"+str(node.id), width=4, outline=cor)
    

def mudanca_cor(event,grafo,cv,cor):
    for no in grafo.nos:
        cv.tag_bind("no"+str(no.id)+"t",'<Button-1>', lambda event,node=no: marcar(event,cv,grafo,node,cor))
        cv.tag_bind("no"+str(no.id),'<Button-1>', lambda event,node=no: marcar(event,cv,grafo,node,cor))
    
def main():
    
    global dim_repr
    a=[0,2,1,3,2,0,3,2,1] #Insert a reduced word for some element of type D
    dim_repr=len(a)
 
    
    c0=Classe(a,0) 
    c0.gerarClasse()
    G=Grafo(c0)
    G.gerarGrafo()
    G.Diametro()
    
 
    
    root=Tk()
    c=Canvas(root, height=950, width=2000) #1400 2000
    desenharGrafo(G,13,925,-25,75,40,c)
    menu=Menu(root)
    root.config(menu=menu)
 
    nos_menu=Menu(menu)
    menu.add_cascade(label="Classes", menu=nos_menu)
    nos_menu.add_command(label="Informação sobre uma classe", command=lambda:Ativar_mostrarInfo(G,c,root))
    nos_menu.add_command(label="Cone", command=lambda:Ativar_Cone(G,c,root))
    nos_menu.add_command(label="Caminho mais curto", command=lambda:Ativar_mostarCaminhoMaisCurto(G,c,root))    
    nos_menu.add_command(label="Procurar palavra",command=lambda:Ativar_procurar_palavra(G,root,c))
    nos_menu.add_command(label="Limpar", command=lambda: limpar(G,c,root))
    
    coresmenu=Menu(menu)
    menu.add_cascade(label="Cores",menu=coresmenu)
    coresmenu.add_command(label="Colorir por dimensao", command=lambda:colorir_dimensao(G,c,root))

    coresmenu.add_command(label="Colorir por número de relações longas", command=lambda:colorir_relacoes_longas(G,c,root))
 
 
    
    c.pack(side=BOTTOM)
    root.mainloop()

main()
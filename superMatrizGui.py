import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import tix
from tkinter.filedialog import askopenfilename, asksaveasfile
import numpy as np

from tkinter.constants import *

from testSuperMatrix3 import obtenNodos, eigenVector, laMatrizDeValores, obtenClustersNodos, sonDistintas

losEntries = []
superMatriz = []
superMatrizTxt = []
superMatrizOriginal = []
nodos = []
losHeaders = []
lasSumas = []

p = tix.Tk()
p.minsize(1600, 800)
# p.geometry('1850x800+100+300')
frame = Frame(p)
frame.place(x=0, y=200)
frameAlternatives = Frame(p)
frameAlternatives.place(x=400, y=60)


    


fileName = ""

def matrizLimite():
    global superMatriz
    
    laAnterior = np.matrix(superMatriz)
    laSiguiente = laAnterior * laAnterior

    while sonDistintas(laAnterior, laSiguiente):
        print ("son distintas")
        laAnterior = laSiguiente.copy()
        laSiguiente = laAnterior * laAnterior
        
    return np.array(laSiguiente)

def headerCallback(j):
    global superMatriz, superMatrizTxt, losEntries, estosClusterNodos, laMatrizOriginal
    print("me pico el "+str(j-2))
    laColumna=j-2
    i = -1
    for cluster in estosClusterNodos:
        laSuma = 0.000
        laSumaOriginal = 0.000
        ii = i
        for nodo in cluster['nodos']:
            i = i + 1
            laSumaOriginal = laSumaOriginal + superMatrizOriginal[i][laColumna]
            laSuma = laSuma + superMatriz[i][laColumna]
            print (nodo + " : " + str(superMatriz[i][laColumna]))

        print(laSumaOriginal, laSuma)
        
        for nodo in cluster['nodos']:
            ii = ii + 1
            if laSuma > 0: 
                
                
                valor = superMatriz[ii][laColumna]* laSumaOriginal / laSuma
                
                losEntries[ii][laColumna].delete(0,END)
                losEntries[ii][laColumna].insert(END, "{0:.6f}".format(valor))
                #superMatriz[ii][laColumna] = superMatriz[ii][laColumna] * laSumaOriginal / laSuma
                print (nodo + " normalizado : " + str(superMatriz[ii][laColumna]))           
#     suma = 0.0000000000
#     for row in superMatriz:
#         print(row[i-2])
#         suma=suma+row[i-2]
#     
#     resta = 1.0000 - suma
#     if (resta<0):
#         resta = 0 - resta 
#         
#     if (resta > 0.0002):
#         
#         factor = float(1.0/suma)
#         print("normalizare con " +str(factor))
#         
#         renglon=-1
#         for row in losEntries:
#             renglon=renglon+1
#             valor = superMatriz[renglon][i-2]*factor
#             print(valor)
#             row[i-2].delete(0,END)
#             row[i-2].insert(END, "{0:.5f}".format(valor))

    
def ponMatriz(eataMatriz):
    global superMatriz
    print("aqui se pondra una matriz en grid")
    
    
def callback(var, i, j):
    global superMatriz
    print("aaa"+str(i),str(j))
    if (var.get()==""):
        print("no hay nada")
        superMatriz[i-1][j-2]=0
    else:
        try:
            superMatriz[i-1][j-2]= float(var.get())
        except:
            var.set(str(superMatriz[i-1][j-2]))
    suma=0
    for row in superMatriz:
        suma = suma + row[j-2]
    lasSumas[j-2].config(text="{0:.2f}".format(suma))
    
    resta = 1.0000 - suma
    if (resta<0):
        resta = 0 - resta 
        
    if (resta > 0.0002):
        print("falla")
        losHeaders[j-2].config(bg="yellow")
        lasSumas[j-2].config(bg="yellow")
    else:
        losHeaders[j-2].config(bg="gray90")
        lasSumas[j-2].config(bg="gray90")
        

def arrayDeStrings():
    global superMatrizTxt, superMatriz
    print("bla")



    
def abreCSV(): 
    global fileName
    
    fileName = askopenfilename(defaultextension="csv", title="escoje archivo csv")
    if fileName:
        abreEsteCSV(fileName)
    
def abreEsteCSV(fileName):
    global hastaAqui, frame, eigenLabel, superMatriz, nodos, superMatrizOriginal, losHeaders, lasSumas, losEntries, estosClusterNodos
    frame.destroy()
    frame = Frame(p)
    frame.place(x=0, y=200)
    # eigenFrame = Frame(p)
    # eigenFrame.place(x=0, y=200)
    b = tix.Balloon(p)
    eigenLabel = tix.Label(frame, text="", width=9, bg="gray90")
    eigenLabel.grid(row=0,column=0)
    #aqui hay que borrar todo el frame
    estosNodos = obtenNodos(fileName)
    print(estosNodos)
    
    
    superMatriz = laMatrizDeValores(fileName)

    superMatrizOriginal = np.array(np.matrix(superMatriz).copy())
    
    nodos=[]
    for nodofeo in estosNodos:
        cachos1 = nodofeo.split("_")
        cachos2 = nodofeo.split(" ")
        if (len(cachos1) >= len(cachos2)):
            cachos = cachos1
        else:
            cachos = cachos2
        
        if (len(cachos) > 1):
            segundoCacho = cachos[len(cachos) - 1][:4]
            nodoguapo = cachos[0][:4] + segundoCacho[:1].upper() + segundoCacho[1:]
            
        else:
            nodoguapo = cachos[0][:5] 
        nodos.append(nodoguapo)
    
    print(nodos)
    losHeaders = []
    columna = 1
    lasSumas =[]
    for nodo in nodos:
        columna = columna + 1
        
        losHeaders.append(Button(frame, text=nodo, width=7, bg="gray90", command= lambda columna=columna: headerCallback(columna)))
        
        losHeaders[columna-2].grid(row=0, column=columna) 
        b.bind_widget(losHeaders[columna-2], balloonmsg=estosNodos[columna-2])
        lasSumas.append(Label(frame, text="nada", width=8, bg="gray90"))
        lasSumas[columna-2].grid(row=len(nodos)+2,column=columna)
        
    renglon = 0
    for nodo in nodos:
        renglon = renglon + 1
        l = Label(frame, text=nodo, width=7)
        l.grid(row=renglon, column=1)
        b.bind_widget(l, balloonmsg=estosNodos[renglon-1]) 
         
    estosClusterNodos = obtenClustersNodos(fileName)
    print (estosClusterNodos[0]['cluster'])
    print (estosClusterNodos[0]['nodos'])
    
    hastaAqui = len(estosClusterNodos[0]['nodos'])
        
    
    superMatrizTxt = []
    losEntries = []
    for i in range(1, len(nodos) + 1):
        
        superMatrizTxt.append([])
        losEntries.append([])
        for j in range(2, len(nodos) + 2):
            superMatrizTxt[i - 1].append(StringVar())
            
            superMatrizTxt[i - 1][j - 2].trace("w", lambda name, index, mode, var=superMatrizTxt[i - 1][j - 2], i=i,j=j: callback(var, i, j))
            losEntries[i - 1].append(Entry(frame, width=7, bd=0, justify=CENTER, textvariable=superMatrizTxt[i - 1][j - 2]))
            
            #superMatrizTxt[i - 1][j - 2].set("{0:.3f}".format(superMatriz[i - 1][j - 2])) 
            #sv = StringVar()
            #superMatrizTxt[i - 1][j - 2]
            
            if ((i <= hastaAqui) and (j <= hastaAqui)) or ((i > hastaAqui) and (j > hastaAqui)):
                losEntries[i - 1][j - 2].config(bg="RosyBrown1")
            else:
                losEntries[i - 1][j - 2].config(bg="RosyBrown3")
            losEntries[i - 1][j - 2].grid(row=i, column=j, sticky=NSEW)
            losEntries[i - 1][j - 2].insert(END, "{0:.6f}".format(superMatriz[i - 1][j - 2]))
            
    #laColumna=5
    columna = -1 
    sombreoCol = True
    for clusterCol in estosClusterNodos:
        sombreoCol = not sombreoCol
        print(clusterCol['cluster'])
        for nodo in clusterCol['nodos']:
            columna = columna + 1
            
            i = -1
            sombreo = True
            for clusterRow in estosClusterNodos:
                sombreo = not sombreo
                for nodo in clusterRow['nodos']:
                    i = i + 1
                    print(sombreo, sombreoCol)
                    if (sombreo != sombreoCol):
                        losEntries[i][columna].config(bg="RosyBrown1",relief=RIDGE)
                    else:
                        losEntries[i][columna].config(bg="RosyBrown3",relief=FLAT)
                
        
          

def ponMatrizLimite():
    global hastaAqui, frame, eigenLabel, fileName, nodos, superMatrizTxt, losHeaders, lasSumas, entries
        
    frame.destroy()
    frame = Frame(p)
    frame.place(x=0, y=200)
    # eigenFrame = Frame(p)
    # eigenFrame.place(x=0, y=200)
    b = tix.Balloon(p)
    eigenLabel = tix.Label(frame, text="", width=9, bg="gray90")
    eigenLabel.grid(row=0,column=0)
    #aqui hay que borrar todo el frame
    estosNodos = obtenNodos(fileName)
    print(estosNodos)
    
    
    estaMatrizLimite = matrizLimite()

    
    
    nodos=[]
    for nodofeo in estosNodos:
        cachos1 = nodofeo.split("_")
        cachos2 = nodofeo.split(" ")
        if (len(cachos1) >= len(cachos2)):
            cachos = cachos1
        else:
            cachos = cachos2
        
        if (len(cachos) > 1):
            segundoCacho = cachos[len(cachos) - 1][:4]
            nodoguapo = cachos[0][:4] + segundoCacho[:1].upper() + segundoCacho[1:]
            
        else:
            nodoguapo = cachos[0][:5] 
        nodos.append(nodoguapo)
    
    print(nodos)
    losHeaders = []
    columna = 1
    lasSumas =[]
    for nodo in nodos:
        columna = columna + 1
        
        losHeaders.append(Button(frame, text=nodo, width=7, bg="gray90", command= lambda columna=columna: headerCallback(columna)))
        
        losHeaders[columna-2].grid(row=0, column=columna) 
        b.bind_widget(losHeaders[columna-2], balloonmsg=estosNodos[columna-2])
        lasSumas.append(Label(frame, text="nada", width=8, bg="gray90"))
        lasSumas[columna-2].grid(row=len(nodos)+2,column=columna)
        
    renglon = 0
    for nodo in nodos:
        renglon = renglon + 1
        l = Label(frame, text=nodo, width=7)
        l.grid(row=renglon, column=1)
        b.bind_widget(l, balloonmsg=estosNodos[renglon-1]) 
         
    estosClusterNodos = obtenClustersNodos(fileName)
    print (estosClusterNodos[0]['cluster'])
    print (estosClusterNodos[0]['nodos'])
    
    hastaAqui = len(estosClusterNodos[0]['nodos'])
        
    
    
    superMatrizTxt = []
    losEntries = []
    for i in range(1, len(nodos) + 1):
        
        superMatrizTxt.append([])
        losEntries.append([])
        for j in range(2, len(nodos) + 2):
            superMatrizTxt[i - 1].append(StringVar())
            
            superMatrizTxt[i - 1][j - 2].trace("w", lambda name, index, mode, var=superMatrizTxt[i - 1][j - 2], i=i,j=j: callback(var, i, j))
            losEntries[i - 1].append(Entry(frame, width=7, bd=0, justify=CENTER, textvariable=superMatrizTxt[i - 1][j - 2]))
            
            #superMatrizTxt[i - 1][j - 2].set("{0:.3f}".format(superMatriz[i - 1][j - 2])) 
            #sv = StringVar()
            #superMatrizTxt[i - 1][j - 2]
            
            if ((i <= hastaAqui) and (j <= hastaAqui)) or ((i > hastaAqui) and (j > hastaAqui)):
                losEntries[i - 1][j - 2].config(bg="RosyBrown1")
            else:
                losEntries[i - 1][j - 2].config(bg="RosyBrown3")
            losEntries[i - 1][j - 2].grid(row=i, column=j, sticky=NSEW)
            losEntries[i - 1][j - 2].insert(END, "{0:.6f}".format(estaMatrizLimite[i - 1][j - 2]))
            
          
def eigenVectorMM():
    global superMatriz
 
    laSuperMatriz = np.matrix(superMatriz)
    laAnterior = laSuperMatriz.copy()
    laSiguiente = laSuperMatriz * laSuperMatriz

    while sonDistintas(laAnterior, laSiguiente):
        print ("son distintas")
        laAnterior = laSiguiente.copy()
        laSiguiente = laAnterior * laAnterior
         
    
    columna = laSiguiente[:, [0]]
    print(columna)
    return columna   
    
    
    
   
        
def eigenVectorCallBack():
    global fileName, hastaAqui, eigenLabel, superMatriz, estosClusterNodos, frameAlternatives
    
    print(superMatriz)
    print(laMatrizDeValores(fileName))
    
    
    #eigenLista = eigenVector(fileName).tolist()
    eigenLista = eigenVectorMM().tolist()
    eigenLabel.config(text="eigenVector")
    #eigenLabel.grid(row=0, column=0)
    renglon = 0
    for row in eigenLista:
        renglon = renglon + 1
        
        e = Entry(frame, width=7, bd=0, justify=CENTER)
        if(renglon > hastaAqui):
            e.config(bg="RosyBrown3")
        else:
            e.config(bg="RosyBrown1")
        e.grid(row=renglon, column=0, sticky=NSEW)
        e.insert(END, "{0:.6f}".format(row[0]))
        
    frameAlternatives.destroy()
    frameAlternatives = Frame(p,width=300,height=300)
    frameAlternatives.place(x=800, y=60)
    renglon=-1
    eigenSuma = 0.00
    for nodo in estosClusterNodos[0]['nodos']:
        renglon = renglon +1
        eigenSuma = eigenSuma + eigenLista[renglon][0] 
    renglon=-1   
    for nodo in estosClusterNodos[0]['nodos']:
        renglon = renglon +1
        print(nodo, renglon)
        
        valorNormalizado = 100*eigenLista[renglon][0]/eigenSuma
        Label(frameAlternatives, text= nodo, width=20).grid(row=renglon,column=0, sticky=NSEW)
        Label(frameAlternatives, text="{0:.1f}".format(valorNormalizado) , width=5).grid(row=renglon,column=1, sticky=NSEW)
        
def ponOriginal():
    global superMatrizOriginal, superMatriz, fileName
    
    abreEsteCSV(fileName)

B = tkinter.Button(p, text="EigenVector", command=eigenVectorCallBack)
B.place(x=500, y=50)


Button(text='Matriz Limite', command=ponMatrizLimite).grid()    
        
Button(text='Abrir csv', command=abreCSV).grid()     
Button(text='SuperMatriz Original', command=ponOriginal).grid()     



mainloop()

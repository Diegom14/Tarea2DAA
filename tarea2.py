from skimage import io
from skimage.color import rgb2gray
from skimage.filters.rank import entropy, gradient
from skimage.morphology import disk
import numpy as np
import matplotlib.pyplot as plt




def get(y, x, t):
    m = len(t) #rows
    n = len(t[0]) #cols
    if x < 0 or x >= n: return sys.maxsize
    if y < 0 or y >= m: return sys.maxsize
    return t[y][x]
    
## Transform the image to gray
## Calculate the entropy or gradient
## Get the path with less energy
## Return the energy as an integer, and the 
## path with less energy as a list of (x,y)

def camino(m,n,e):#m=4 n=5
    #inicializa la matriz con ceros
    T = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append(0)
        T.append(row)  

    #Rellena la matriz
    
    for i in range(n):
        for j in range(m):
            #Guarda el mínimo cuando no se puede preguntar hacia la izquierda
            if j == 0 :
                T[i][j] = e[i][j] + min(T[i-1][j],T[i-1][j+1])
               
            #Guarda el mínimo cuando no se puede preguntar hacia la derecha
            elif j == m-1:
                T[i][j] = e[i][j] + min(T[i-1][j-1],T[i-1][j])
                
            #Guarda el minimo en todos los demas casos
            else:
                T[i][j] = e[i][j] + min(T[i-1][j+1],T[i-1][j],T[i-1][j-1])
                
    energia=min(T[n-1])
    pos=0
    for i in range(m):
        if T[n-1][i] == energia:
            pos=i

    pad=[]
    pad.append((n-1,pos))
    
    for i in range(n-1,0,-1):
    
        if pos == 0:
            minimo = min(T[i-1][pos],T[i-1][pos+1])
            
            if minimo==T[i-1][pos]:
                pad.append((i-1,pos))
            elif minimo==T[i-1][pos+1]:
                pad.append((i-1,pos+1))
                pos=pos+1
                
        elif pos == m-1:
            minimo = min(T[i-1][pos-1],T[i-1][pos])
            
            if minimo==T[i-1][pos-1]:
                pad.append((i-1,pos-1))
                pos=pos-1
                
            elif minimo==T[i-1][pos]:
                pad.append((i-1,pos))

        else:
            minimo= min(T[i-1][pos+1],T[i-1][pos],T[i-1][pos-1])

            if minimo==T[i-1][pos+1]:
                pad.append((i-1,pos+1))
                pos=pos+1
                
            elif minimo==T[i-1][pos]:
                pad.append((i-1,pos))
            elif minimo == T[i-1][pos-1]:
                pad.append((i-1,pos-1))
                pos=pos-1
                
    pad.reverse()
                
    return energia, pad

def energy(img):
    # filas = m, columnas = n
    m,n = img.shape
    e,ans=camino(n,m,img)
    
    return e, ans


def togray(image):
    image_bw = rgb2gray(image)
    # using the entropy
    #image_e = entropy(image_bw,disk(1))
    #energy(image_e)
    #print(image_e)
    
    # using gradient
    image_g = gradient(image_bw,disk(1))
    #print(image_g)
    return image_g

## Remove one pixel per row... the one
## in the path min energy
def remove(image, pixels):
    ## Debe remover el camino con menor energia
    
    ans=image
    m,n,_ = ans.shape
    aux = []
    for i in range(m):
        row = []
        for j in range(n):
            row.append(ans[i][j])
        aux.append(row)

    for i in range(m):
        del aux[pixels[i][0]][pixels[i][1]] 

    r=np.asarray(aux)

    return r
   
if __name__=='__main__':
    
    import sys
    from timeit import Timer
    
    image = io.imread('imagen1000.jpg')
    """
    img_gray = togray(image)
    plt.figure()
    plt.imshow(image)
    plt.figure()
    plt.imshow(img_gray)
    plt.show()
    """
    
    percent = 0.75
    
    m,n,_ = image.shape
    new_n = int(n * percent)
    
    img = image
    ims = []

    #t = Timer("togray(img)", "from __main__ import togray, img")
    #t1 = Timer("energy(img_gray)", "from __main__ import energy, img_gray")
    #t2 = Timer("remove(img,p)", "from __main__ import remove, img, p")
    

    for i in range(n-new_n):
        print("Iteracion numero {}/{}".format(i+1, n-new_n))
        
        img_gray = togray(img)
        e, p = energy(img_gray)
        img_new = remove(img, p)
        
        img = img_new

    
    plt.figure()
    plt.imshow(image) # imagen original
    plt.figure()
    plt.imshow(img) # imagen escalada
    plt.show()
    
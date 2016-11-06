from skimage import io
from skimage.color import rgb2gray
from skimage.filters.rank import entropy, gradient
from skimage.morphology import disk
import numpy as np
import matplotlib.pyplot as plt
import sys

def table(m,n):
    # filas = m, columnas = n
    #Inicializa la matriz en ceros
    T = []
    for i in range(len(n)):
        row = []
        for j in range(len(m)):
            row.append(0)
        T.append(row)
    

    #Rellena la matriz

    for i in range(len(n)):
        for j in range(len(m)):
            if i >= 1 or i!=len(m):
                T[i,j] = min(T[i,j]+T[i-1,j+1],T[i,j]+T[i,j+1],T[i,j]+T[i+1,j+1])

            
            elif i == 0:
                T[i,j] = min(T[i,j]+T[i,j+1],T[i,j]+T[i+1,j+1])
                

            elif i == len(m):
                T[i,j] = min(T[i,j]+T[i-1,j+1],T[i,j]+T[i,j+1])
    solucion = find(T)

#Crea un arreglo con los pixeles a eliminar
def find(table):
    points = []
    for i in range(n):
        for i in range(m):
            if T[i][j] != 0:
                points.append(T[i][j])
    return points

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
def energy(img):
    # filas = m, columnas = n
    m, n = img.shape
    

    
    e = 0
    ans = table(m,n)
    
    return e, ans


def togray(image):
    image_bw = rgb2gray(image)
    # using the entropy
    #image_e = entropy(image_bw,disk(1))
    #return energy(image_e)
    
    # using gradient
    image_g = gradient(image_bw,disk(1))
    return image_g

## Remove one pixel per row... the one
## in the path min energy
def remove(image, pixels):
    ## Debe remover el camino con menor energia
    ans = image
    
    return ans
   
if __name__=='__main__':
    import sys
    
    image = io.imread('image.png')
    img_gray = togray(image)
    plt.figure()
    plt.imshow(image)
    plt.figure()
    plt.imshow(img_gray)
    plt.show()
    
    percent = 0.75
    
    m,n,_ = image.shape
    new_n = int(n * percent)
    
    img = image
    ims = []
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

def table(m,n,e):
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
    print(T)





n = 5
m = 4
e = [[100,23,3,1],[1,2,3,1],[1,5,8,1],[3,1,2,1],[2,2,1000,200]]

table(m,n,e)
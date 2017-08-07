#!/usr/bin/python
# -*- coding: utf-8 -*-

class LetraSecuencia:
    letra = None
    secuencia = 0

class ADNException(Exception):
    pass

def esMutante(adn):
    letras_validas = "atcg"

    #Inicialización de la estructura para el cálculo
    N = len(adn)
    if N < 4:
        raise ADNException("Secuencia de ADN demasiado chica (N = " + str(N) + ")")

    secuencias = 0
    
    #V[j].letra es la última letra de la columna j
    #V[j].letra es la cantidad de letras iguales en la columna j
    verticales = [LetraSecuencia() for i in range(0, N)]
    
    #diag_izq_der son las diagonales de izquierda a derecha, a saber:
    # diag_izq_der[i - j] contiene el LetraSecuencia correspondiente a la diagonal que empieza en (i, j)
    # aprovechando que en Python se puede indexar con números negativos
    diag_izq_der = [LetraSecuencia() for i in range(0, (1 + 2*(N-4)))]

    #diag_der_izq son las diagonales de derecha a izquierda, a saber:
    # diag_der_izq[i + j - N] contiene el LetraSecuencia correspondiente a la diagonal que empieza en (i, j)
    # aprovechando que en Python se puede indexar con números negativos
    diag_der_izq = [LetraSecuencia() for i in range(0, (1 + 2*(N-4)))]

    for i in range(0, N):
        if len(adn[i]) != N:
            raise ADNException("Secuencia de dimensiones inválidas (esperaba " + str(N) + " y la " + str(i) + "-ésima fila mide " + str(len(adn[i])) + ")")

        adn[i] = adn[i].lower()

        sec_horizontal = 1
        for j in range(0, N):
            if adn[i][j] not in letras_validas:
                raise ADNException("Letra inválida: «" + str(adn[i][j]) + "»")

            #Fila
            if j > 0:
                if adn[i][j] == adn[i][j-1]:
                    sec_horizontal += 1
                else:
                    sec_horizontal = 1

                if sec_horizontal == 4:
                    secuencias += 1

            #Columna
            if verticales[j].letra == None:
                verticales[j].letra = adn[i][j]
                verticales[j].secuencia = 1
            else:
                if adn[i][j] == verticales[j].letra:
                    verticales[j].secuencia += 1
                else:
                    verticales[j].letra = adn[i][j]
                    verticales[j].secuencia = 1

            if verticales[j].secuencia == 4:
                secuencias += 1

            #Diagonal izquierda a derecha
            indice_izq_der = i - j

            # Diagonales de más de 4 elementos
            if abs(indice_izq_der) < (N - 4):
                if diag_izq_der[indice_izq_der].letra == None:
                    diag_izq_der[indice_izq_der].letra = adn[i][j]
                    diag_izq_der[indice_izq_der].secuencia = 1
                else:
                    if adn[i][j] == diag_izq_der[indice_izq_der].letra:
                        diag_izq_der[indice_izq_der].secuencia += 1
                    else:
                        diag_izq_der[indice_izq_der].letra = adn[i][j]
                        diag_izq_der[indice_izq_der].secuencia = 1

                if diag_izq_der[indice_izq_der].secuencia == 4:
                    secuencias += 1

            #Diagonal derecha a izquierda
            indice_der_izq = i + j - N
            
            # Diagonales de más de 4 elementos
            # Esta cuenta es más complicada porque los índices de estas diagonales son más raros:
            #  * La principal (que empieza en adn[N-1][N-1]) está en diag_der_izq[-1]
            #  * La de abajo de esta (que empieza en adn[N-2][N-1]) está en diag_der_izq[0]
            #  * La de arriba de la principal (que empieza en adn[N-1][N-2]) está en diag_der_izq[-2]
            # La secuencia da este rango
            if indice_der_izq in range(3 - N, N - 5):

                if diag_der_izq[indice_der_izq].letra == None:
                    diag_der_izq[indice_der_izq].letra = adn[i][j]
                    diag_der_izq[indice_der_izq].secuencia = 1
                else:
                    if adn[i][j] == diag_der_izq[indice_der_izq].letra:
                        diag_der_izq[indice_der_izq].secuencia += 1
                    else:
                        diag_der_izq[indice_der_izq].letra = adn[i][j]
                        diag_der_izq[indice_der_izq].secuencia = 1

                if diag_der_izq[indice_der_izq].secuencia == 4:
                    secuencias += 1


        if secuencias >= 2:
            return True
    
    return False

if __name__ == '__main__':
    adn_test = ["atgcga", "cagtgc", "ttatgt", "agaagg", "ccccta", "tcactg"]

    print esMutante(adn_test)


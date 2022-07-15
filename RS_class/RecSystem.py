import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

class RecSystem():

    def distancia_de_vetores(a, b):
        return np.linalg.norm(a - b)

    def notas_do_usuario(usuario):

        # fltra o dataframe pelo usuarioId
        notas_do_usuario = df[df['usuarioId'] == usuario]
        
        # setta o index como a coluna de filmeId
        notas_do_usuario = notas_do_usuario[['filmeId', 'nota']].set_index(['filmeId'])
        return notas_do_usuario

    def distancia_de_usuarios(usuario_id1, usuario_id2):

        # trás notas dos usuários 1 e 2
        notas1 = notas_do_usuario(usuario_id1)
        notas2 = notas_do_usuario(usuario_id2)

        # trazer somente os filmes que os dois usuários assistiram
        diferencas = notas1.join(notas2, lsuffix = '_esquerda', rsuffix = '_direita').dropna()

        # calcula a distância entre os dois usuários
        distancia = distancia_de_vetores(diferencas['nota_esquerda'], diferencas['nota_direita'])
        return distancia

    def distancia_de_todos(voce_id):
        todos_os_usuarios = notas['usuarioId'].unique()
        distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
        distancias = pd.DataFrame(distancias, columns = ['voce', 'outra_pessoa', 'distancia'])
        return distancias
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

class KnnMv():

    # função que pega os dados e renomeia colunas

    def get_data(filmes, notas):
        # lendo os dados
        filmes = pd.read_csv(filmes)
        notas = pd.read_csv(filmes)

        # alterando os nomes das colunas
        filmes.columns = ['filmeId', 'titulo', 'generos']
        notas.columns = ['usuarioId', 'filmeId', 'nota', 'momento']
        return filmes, notas

    # função que calcula a distância euclidiana entre dois vetores
    def distancia_de_vetores(a, b):
        dist = np.linalg.norm(a - b)
        return dist

    # função que retorna dataframe com os coluna de notas e index como o id do filme
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
        return [usuario_id1, usuario_id2, distancia]


    def distancia_de_todos(voce_id):

        todos_os_usuarios = notas['usuarioId'].unique()
        distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
        distancias = pd.DataFrame(distancias, columns = ['voce', 'outra_pessoa', 'distancia'])
        return distancias

    def distancia_de_usuarios(usuario_id1, usuario_id2, minimo = 5):

        # trás notas dos usuários 1 e 2
        notas1 = notas_do_usuario(usuario_id1)
        notas2 = notas_do_usuario(usuario_id2)

        # trazer somente os filmes que os dois usuários assistiram
        diferencas = notas1.join(notas2, lsuffix = '_esquerda', rsuffix = '_direita').dropna()

        if(len(diferencas) < minimo):
        return None

        # calcula a distância entre os dois usuários
        distancia = distancia_de_vetores(diferencas['nota_esquerda'], diferencas['nota_direita'])
        return [usuario_id1, usuario_id2, distancia]

    def mais_proximos_de(voce_id, n_mais_proximos = 5, numero_de_usuarios_a_analisar = None):
        distancias = distancia_de_todos(voce_id, numero_de_usuarios_a_analisar = numero_de_usuarios_a_analisar)
        mp = distancias.sort_values(by = 'distancia')
        mp = distancias.set_index('outra_pessoa').drop(voce_id, errors = 'ignore')
        
        return mp

    def distancia_de_todos(voce_id, numero_de_usuarios_a_analisar = None):
        todos_os_usuarios = notas['usuarioId'].unique()
        if numero_de_usuarios_a_analisar:
            todos_os_usuarios = todos_os_usuarios[:numero_de_usuarios_a_analisar]
        distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
        distancias = list(filter(None, distancias))
        distancias = pd.DataFrame(distancias, columns = ['voce', 'outra_pessoa', 'distancia'])
        return distancias

    def sugere_para(voce, n_mais_proximos = 10, numero_de_usuarios_a_analisar = None):
        # suas notas
        notas_de_voce = notas_do_usuario(voce)

        # indice do filme visto por ti
        filmes_vistos = notas_de_voce.index

        # pessoas similares
        similares = mais_proximos_de(voce, n_mais_proximos, numero_de_usuarios_a_analisar)
        similares = similares.sort_values(by = 'distancia')
        similares = similares.head(n_mais_proximos)
        usuarios_similares = similares.index
        notas_dos_similares = notas.set_index(['usuarioId']).loc[usuarios_similares]
        recomendacoes = notas_dos_similares.groupby(by = 'filmeId').mean()[['nota']]
        recomendacoes = recomendacoes.sort_values(by = 'nota', ascending = False)
        recomendacoes = recomendacoes.join(filmes)
        return recomendacoes

    

    
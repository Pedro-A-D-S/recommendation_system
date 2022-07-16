# imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

class KnnMv():

    def __init__(self, filmes_path, notas_path):
        self.filmes_path = filmes_path
        self.notas_path = notas_path


    # função que pega os dados e renomeia colunas
    def get_data(self):
        # lendo os dados
        filmes = pd.read_csv(self.filmes_path)
        notas = pd.read_csv(self.notas_path)

        # alterando os nomes das colunas
        filmes.columns = ['filmeId', 'titulo', 'generos']
        notas.columns = ['usuarioId', 'filmeId', 'nota', 'momento']
        return filmes, notas

    def aux_df(self, notas, filmes):
        # criando tabela única para melhor análise
        df = pd.merge(notas, filmes, how = 'left', right_on = 'filmeId', left_on = 'filmeId')
        # criando coluna com a quantidade de notas atribuídas aos filmes
        df_aux = df.groupby(by = 'filmeId').agg({'nota':'count'}).reset_index()
        # juntando o dataframe inicial com a coluna de quantidade de notas
        df = pd.merge(df, df_aux, how = 'left', right_on = 'filmeId', left_on = 'filmeId')
        # renomeando colunas
        df.rename(columns = {'nota_x':'nota', 'nota_y':'total_de_votos'}, inplace = True)
        # obtendo os filmes mais votados pelas pessoas e suas notas médias
        df_aux2 = df.groupby(by = ['titulo', 'filmeId']).agg({'total_de_votos':'count', 
        'nota':'mean'}).reset_index().sort_values(by = 'total_de_votos', ascending = False)
        df_aux2.rename(columns = {'nota':'nota_media'}, inplace = True)
        # filtrando colunas
        df_aux3 = df_aux2[['filmeId', 'nota_media']]
        # dataframe na forma final
        df = pd.merge(df, df_aux3, how = 'left', right_on = 'filmeId', left_on = 'filmeId')

        return df

    # função que calcula a distância euclidiana entre dois vetores
    def distancia_de_vetores(a, b):
        dist = np.linalg.norm(a - b)
        return dist

    # função que retorna dataframe com os coluna de notas e index como o id do filme
    def notas_do_usuario(self, data_frame, usuario):
        # fltra o dataframe pelo usuarioId
        notas_do_usuario = data_frame[data_frame['usuarioId'] == usuario]
        
        # setta o index como a coluna de filmeId
        notas_do_usuario = notas_do_usuario[['filmeId', 'nota']].set_index(['filmeId'])
        return notas_do_usuario

    def distancia_de_usuarios(self, usuario_id1, usuario_id2):
        self.notas_do_usuario()
        self.distancia_de_vetores()
        # trás notas dos usuários 1 e 2
        notas1 = notas_do_usuario(usuario_id1)
        notas2 = notas_do_usuario(usuario_id2)

        # trazer somente os filmes que os dois usuários assistiram
        diferencas = notas1.join(notas2, lsuffix = '_esquerda', rsuffix = '_direita').dropna()

        # calcula a distância entre os dois usuários
        distancia = distancia_de_vetores(diferencas['nota_esquerda'], diferencas['nota_direita'])
        return [usuario_id1, usuario_id2, distancia]


    def distancia_de_todos(self, voce_id):
        self.notas
        self.distancia_de_usuarios()
        todos_os_usuarios = notas['usuarioId'].unique()
        distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
        distancias = pd.DataFrame(distancias, columns = ['voce', 'outra_pessoa', 'distancia'])
        return distancias

    def distancia_de_usuarios(self, usuario_id1, usuario_id2, minimo = 5):
        self.notas_do_usuario()
        self.distancia_de_vetores()
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

    def mais_proximos_de(self, voce_id, n_mais_proximos = 5, numero_de_usuarios_a_analisar = None):
        self.distancia_de_todos()
        distancias = distancia_de_todos(voce_id, numero_de_usuarios_a_analisar = numero_de_usuarios_a_analisar)
        mp = distancias.sort_values(by = 'distancia')
        mp = distancias.set_index('outra_pessoa').drop(voce_id, errors = 'ignore')
        
        return mp

    def distancia_de_todos(self, voce_id, numero_de_usuarios_a_analisar = None):
        self.notas
        self.distancia_de_usuarios()
        todos_os_usuarios = notas['usuarioId'].unique()
        if numero_de_usuarios_a_analisar:
            todos_os_usuarios = todos_os_usuarios[:numero_de_usuarios_a_analisar]
        distancias = [distancia_de_usuarios(voce_id, usuario_id) for usuario_id in todos_os_usuarios]
        distancias = list(filter(None, distancias))
        distancias = pd.DataFrame(distancias, columns = ['voce', 'outra_pessoa', 'distancia'])
        return distancias

    def sugere_para(self, voce, n_mais_proximos = 10, numero_de_usuarios_a_analisar = None):
        self.notas_do_usuario()
        self.mais_proximos_de()
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

    

    
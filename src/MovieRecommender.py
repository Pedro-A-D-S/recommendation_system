import pandas as pd
import numpy as np
from typing import Optional
from typing import Tuple

class MovieRecommender:
    def __init__(self, filmes_path: str, rating_path: str):
        self.filmes,
        self.rating = self._get_data(filmes_path, rating_path)
        self.df = self._aux_df(self.rating, self.filmes)
    
    def _get_data(self, filmes_path: str, rating_path: str) -> Tuple(pd.DataFrame, pd.DataFrame):
        """
        Carrega os dados dos arquivos CSV e retorna DataFrames de filmes e rating.
        
        Args:
            filmes_path (str): Filepath para arquivo contendo filme
            rating_path (str): Filepath para arquivo contendo rating
        
        Returns:
            filmes, rating (Tuple): Dataframes de filmes e rating
        """
        filmes = pd.read_csv(filmes_path)
        rating = pd.read_csv(rating_path)
        
        filmes.columns = ['filmeId', 'titulo', 'generos']
        rating.columns = ['usuarioId', 'filmeId', 'nota', 'momento']
        rating.drop(columns = ['momento'], inplace = True)
        
        return filmes, rating
    
    def _aux_df(self, df_rating: pd.DataFrame, df_filmes: pd.DataFrame) -> pd.DataFrame:
        """
        Cria um DataFrame combinado com informações adicionais para análise.
        
        Args:
            df_rating (pd.DataFrame): DataFrame contendo as rating.
            df_filmes (pd.DataFrame): DataFrame contendo os filmes.
            
        Returns:
            df (pd.DataFrame): DataFrame.
        """
        df = pd.merge(df_rating, df_filmes, how='left', right_on='filmeId', left_on='filmeId')
        df_aux = df.groupby(by='filmeId').agg({'nota': 'count'}).reset_index()
        df = pd.merge(df, df_aux, how='left', right_on='filmeId', left_on='filmeId')
        df.rename(columns={'nota_x': 'nota', 'nota_y': 'total_de_votos'}, inplace=True)

        return df


    def distancia_de_vetores(self, vetor_a: np.ndarray, vetor_b: np.ndarray) -> float:
        """
        Calcula a distância euclidiana entre dois vetores.
        
        Args:
            vetor_a (np.ndarray): vetor a.
            vetor_b (np.ndarray): vetor b.
            
        Returns
            distance (float): distancia entre vetores a e b
        """
        distance = np.linalg.norm(vetor_a - vetor_b)
        
        return distance

    def user_ratings(self, id_user: int) -> pd.DataFrame:
        """
        Retorna um DataFrame com as rating do usuário especificado.
        
        Args:
            id_user (int): ID do usuário.
        
        Returns:
            user_ratings (pd.DataFrame): Pandas DataFrame contendo ratings de usuários.
        """
        user_ratings = self.rating[self.rating['usuarioId'] == id_user]
        user_ratings = user_ratings[['filmeId', 'nota']].set_index(['filmeId'])\
            
        return user_ratings
    
    def distancia_de_usuarios(self, id_user1: int, id_user2: int, minimo: int = 5) -> Optional[list]:
        """
        Calcula a distância entre dois usuários com base em suas rating.
        
        Args:
            id_user1 (int): id do primeiro usuário
            id_user2 (int): id do segundo usuário
            minimo (int): Número de usuários
        
        Returns:
            distancia (Optional[list]): Lista contendo ids dos usuários e a distância entre eles.
        """
        rating1 = self.user_ratings(id_user1)
        rating2 = self.user_ratings(id_user2)
        diferencas = rating1.join(rating2, lsuffix='_esquerda', rsuffix='_direita').dropna()
        
        if len(diferencas) < minimo:
            return None
        
        distancia = self.distancia_de_vetores(diferencas['nota_esquerda'], diferencas['nota_direita'])
        return distancia
    
    def mais_proximos_de(self, id_user: int, nearest: int = 5, range: Optional[int] = None) -> pd.DataFrame:
        """
        Encontra os usuários mais próximos com base nas distâncias.
        
        Args:
    
            id_user (int): ID do usuário.
            nearest (int): Número de usuários mais próximos.
            range (Optional[int]): Número de usuários mais próximos.
        
        Returns:
            nearest (pd.DataFrame): DataFrame contendo usuários mais próximos.
        """
        distancias = self.distancia_de_todos(id_user, range)
        nearest = distancias.sort_values(by = 'distancia')
        nearest = nearest.set_index('outra_pessoa').drop(id_user, errors = 'ignore')
        return nearest

    def distancia_de_todos(self, id_user: int, range: Optional[int] = None) -> pd.DataFrame:
        """
        Calcula a distância entre o usuário e todos os outros usuários.
        
        Args: 
        
            id_user (int): ID do usuário.
            range (Optional[int]): Quantidade de usuários recomendados
        
        Returns:

            distancia_a_todos (pd.DataFrame): DataFrame contendo distância entre todos os usuários.
        """
        todos_os_usuarios = self.rating['usuarioId'].unique()
        if range:
            todos_os_usuarios = todos_os_usuarios[:range]
        distancia_a_todos = [self.distancia_de_usuarios(id_user, uid) for uid in todos_os_usuarios]
        distancia_a_todos = list(filter(None, distancia_a_todos))
        distancia_a_todos = pd.DataFrame(distancia_a_todos, columns=['usuario', 'outro_usuario', 'distancia'])
        return distancia_a_todos

    def sugere_para(self, id_user: int, nearest: int = 10, range: Optional[int] = None,
                    qtd_filmes: int = 5) -> pd.DataFrame:
        """
        Sugere filmes para um usuário com base nas rating de usuários similares.
        
        Args: 
    
            id_user (int): ID do usuário.
            nearest (int): Número de usuários mais próximos.
            range (Optional[int]): Número de usuários mais próximos.
            qtd_filmes (int): Quantidade de filmes recomendados.
        
        Returns:
            recomendacoes (pd.DataFrame): DataFrame contendo filmes recomendados.
        """
        filmes = filmes.set_index(['filmeId'])
        rating_de_usuario = self.user_ratings(id_user)
        filmes_vistos = rating_de_usuario.index
        similares = self.mais_proximos_de(id_user, nearest, range)
        similar = similares.sort_values(by = 'distancia').iloc[0].name
        rating_do_similar = self.user_ratings(similar)
        rating_do_similar = rating_do_similar.drop(filmes_vistos, erros = 'ignore')
        recomendacoes = rating_do_similar.sort_values(by = 'nota', ascendimg = False).head(qtd_filmes)
        recomendacoes = recomendacoes.join(filmes)
        
        return recomendacoes
        

<!DOCTYPE html>
<html>

<head>
</head>

<body>

<h1>Sistema de Recomendação de Filmes</h1>

<p>Este repositório contém códigos para a criação de um sistema de recomendação de filmes utilizando análise de dados e machine learning. O sistema é projetado para sugerir filmes aos usuários com base em suas preferências de avaliação e nos padrões de avaliação de outros usuários.</p>

<h2>Estrutura do Repositório</h2>

<p>O repositório está organizado da seguinte maneira:</p>

<ul>
    <li><strong>config:</strong> Este diretório contém um arquivo YAML que armazena os caminhos para os arquivos e pastas relevantes para o projeto.</li>
    <li><strong>data:</strong> Neste diretório, você encontrará os dados utilizados no sistema de recomendação. Os dados estão armazenados em arquivos CSV e podem ser baixados do site <a href="https://grouplens.org/datasets/movielens/latest/">https://grouplens.org/datasets/movielens/latest/</a>.</li>
    <li><strong>notebooks:</strong> Este diretório contém um notebook Jupyter onde a análise de dados, a criação do sistema de recomendação e a geração de resultados são realizadas. Ele serve como o ponto central para a exploração e desenvolvimento do sistema.</li>
    <li><strong>source:</strong> Aqui você encontrará a classe que encapsula as funções do sistema de recomendação. Essa classe é construída a partir do notebook e pode ser reutilizada para recomendações em outros contextos.</li>
</ul>

<h2>Uso</h2>

<p>Para executar o sistema de recomendação, siga estas etapas:</p>

<ol>
    <li>Certifique-se de ter instalado as bibliotecas necessárias. Você pode usar o arquivo <code>requirements.txt</code> para instalar as dependências usando o comando:</li>
</ol>

<pre><code>pip install -r src/requirements.txt</code></pre>

<ol start="2">
    <li>Execute o notebook <code>notebooks/recomendacao_filmes.ipynb</code>. Este notebook guiará você por todo o processo de análise de dados, construção do sistema de recomendação e geração de resultados.</li>
    <li>Se você deseja incorporar as funcionalidades do sistema de recomendação em outros projetos, importe a classe do módulo <code>source</code> e utilize as funções encapsuladas para gerar recomendações com base nos dados fornecidos.</li>
</ol>

<h2>Contribuições</h2>

<p>Contribuições para este repositório são bem-vindas! Se você encontrar bugs, tiver sugestões ou melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.</p>

<h2>Créditos</h2>

<p>Este projeto é desenvolvido por Pedro Alves.</p>

<h2>Licença</h2>

<p>Este projeto é licenciado sob a <a href="https://exemplo.com/licenca">licença MIT</a>. Veja o arquivo LICENSE para mais detalhes.</p>

</body>

</html>

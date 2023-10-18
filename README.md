# Projeto - Fome_Zero

# 1. Problema de negócio

A empresa Fome Zero é uma marketplace de restaurantes. Ou seja, seu core
business é facilitar o encontro e negociações de clientes e restaurantes. Os
restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza
informações como endereço, tipo de culinária servida, se possui reservas, se faz
entregas e também uma nota de avaliação dos serviços e produtos do restaurante,
dentre outras informações.

O Desafio

O CEO Guerra também foi recém contratado e precisa entender melhor o negócio
para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a
Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da
empresa e que sejam gerados dashboards, a partir dessas análises, para responder
às seguintes perguntas:

### Perguntas Gerais:

1. Quantos restaurantes únicos estão registrados?
2. Quantos países únicos estão registrados?
3. Quantas cidades únicas estão registradas?
4. Qual o total de avaliações feitas?
5. Qual o total de tipos de culinária registrados?

### Visão por País:

1. Qual o nome do país que possui mais cidades registradas?
2. Qual o nome do país que possui mais restaurantes registrados?
3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
registrados?
4. Qual o nome do país que possui a maior quantidade de tipos de culinária
distintos?
5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
entrega?
7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
reservas?
8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
registrada?
9. Qual o nome do país que possui, na média, a maior nota média registrada?
10. Qual o nome do país que possui, na média, a menor nota média registrada?
11. Qual a média de preço de um prato para dois por país?

### Visão por Cidades:

1. Qual o nome da cidade que possui mais restaurantes registrados?
2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
4?
3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
2.5?
4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
distintas?
6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
reservas?
7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
entregas?
8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
aceitam pedidos online?

### Visão por Restaurantes:

1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
2. Qual o nome do restaurante com a maior nota média?
3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
pessoas?
4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
média de avaliação?
5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
possui a maior média de avaliação?
6. Os restaurantes que aceitam pedido online são também, na média, os
restaurantes que mais possuem avaliações registradas?
7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
possuem o maior valor médio de um prato para duas pessoas?
8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
possuem um valor médio de prato para duas pessoas maior que as churrascarias
americanas (BBQ)?

### Visão por Tipos de Culinárias:

1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a maior média de avaliação?
2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
restaurante com a menor média de avaliação?
3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a maior média de avaliação?
4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
restaurante com a menor média de avaliação?
5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a maior média de avaliação?
6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
restaurante com a menor média de avaliação?
7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a maior média de avaliação?
8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
restaurante com a menor média de avaliação?
9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a maior média de avaliação?
10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
restaurante com a menor média de avaliação?
11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
pessoas?
12. Qual o tipo de culinária que possui a maior nota média?
13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
online e fazem entregas?

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
que exibam essas métricas da melhor forma possível para o CEO, a fim auxiliá-lo para entender a empresa e conseguir tomar as decisões mais assertivas

# 2. Premissas assumidas para a análise

1. Marketplace foi o modelo de negócio assumido.
2. As principais visões do negócio foram: Visão por  País, Visão por Cidades, Visão Restaurantes e Visão por Tipo de Culinárias.

# 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as principais visões do modelo de negócio da empresa:

1. Visão por País;
2. Visão por Cidades
3. Visão por Restaurantes e Culinárias

Dispomos na página inicial as informações gerais com opção de seleção de Filtro por país com as informações gerais do Marketplace, além de uma mapa interativo, em que é possível identificar a localização de cada restaurante com rank de cores e suas principais características (Valor prato para dois, Tipo de Culinária e Nota Média de avaliação)

Cada visão é representada pelo seguinte conjunto de métricas.

### 3.1. Pagina Inicial (Informações Gerais):
    a. Quantidade de Restaurantes Cadastrados;
    b. Quantidade de Países;
    c. Quantidade de cidades cadastradas;
    d. Número de Avaliações realizadas;
    e. Quantidade de tipos de culinárias cadastradas.

### 3.2. Visão Países
    a. Quantidade de Restaurantes Registrados por País;
    b. Quantidade de Cidades Registradas por País;
    c. Avaliações Médias realizadas por País;
    d. Média do Preço de um prato para dois por País;

### 3.3. Visão Cidades
    a. Top 10 cidades com mais Restaurantes Cadastrados; 
    b. Top 7 Cidades com mais Restaurantes com média de avaliação acima de 4;
    c. Top 7 Cidades com mais Restaurantes com média de avaliação abaixo de 2,5;
    d. a. Top 10 cidades com mais Restaurantes com Tipos de Culinárias Cadastrados; 

### 3.4. Visão Cozinhas
    1. Nome do Melhor Tipo de Culinária (conforme nota média de avaliações);
    2. Melhor nota média do Melhor Tipo Culinária;
    3. Nome do Pior tipo de Culinária (conforme nota média de avaliações);
    4. Pior nota média  do Pior Tipo de Culinária;
    5. Dataframe com os 10 melhores Restaurantes e suas informações;
    6. Top 10 Melhores Tipos de Culinárias (conforme média de avaliações);
    7. Top 10 Piores Tipos de Culinárias (conforme média de avaliações);

# 4. Top 3 Insights de dados

1. Como esperado a maior concentração de Restaurantes está no continente asiático, com destaque para os Estados Unidos assumindo o segundo lugar com mais restaurantes registrados na plataforma
2. Não há diferença na média de valores dos pratos para duas pessoas em restaurantes que aceitem ou não reservas.
3. Os restaurantes com pedidos online recebem mais acessos de avaliações na plataforma.

# 5. O produto final do projeto

Painel online, hospedado em um Cloud e disponível para acesso em
qualquer dispositivo conectado à internet.
O painel pode ser acessado através desse link: [https://somali-fomezero.streamlit.app/]

# 6. Conclusão

O objetivo desse projeto é criar um conjunto de gráficos e/ou tabelas
que exibam essas métricas da melhor forma possível para o CEO.

# 7. Próximo passos

1. Reduzir o número de métricas.
2. Dispor de features com as informações dos clientes (Sexo, Idade).
3. Dispor de features com período/datas de conversão das compras;
4. Adicionar uma feature com a conversão dos valores dos pratos para uma moeda única (utilização por exemplo do Dólar como padrão);
5. Criar modelo para prever satisfação dos clientes
6. Adicionar novas visões de negócio.

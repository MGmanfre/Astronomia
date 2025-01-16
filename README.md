# Astronomia
# Extração e Processamento de Dados de Exoplanetas

Este repositório contém um script em Python que coleta, processa e insere dados de exoplanetas no banco de dados MySQL. Os dados são extraídos da API do NASA Exoplanet Archive, limpos e, em seguida, armazenados para posterior análise.

## Funcionalidades

### Coleta de Dados de Exoplanetas

A função get_exoplanets consulta a API do NASA Exoplanet Archive para obter informações detalhadas sobre exoplanetas, como:

- *Nome do exoplaneta*

- *Massa* (em massas terrestres)

- *Raio* (em raios terrestres)

- *Período orbital* (em dias)

- *Distância da estrela hospedeira* (em parsecs)

Os dados só são recuperados se os valores necessários não forem nulos.

### Armazenamento no Banco de Dados

Os dados processados são inseridos na tabela Exoplanetas do banco de dados MySQL. Cada registro inclui as seguintes colunas:

- *Nome*

- *Massa*

- *Raio*

- *Período Orbital*

- *Distância*

O banco de dados é configurado através das credenciais armazenadas em um arquivo .env, garantindo segurança.

#### Tecnologias e Bibliotecas Utilizadas

**Python** (linguagem principal)

**Bibliotecas**

- *Requests:* Para acessar a API do NASA Exoplanet Archive.

- *Pandas:* Para manipulação de dados tabulares.

- *MySQL Connector:* Para conexão e inserção de dados no banco de dados.

- *BeautifulSoup:* Para processar tabelas HTML.

- *dotenv:* Para gerenciar variáveis de ambiente de forma segura.

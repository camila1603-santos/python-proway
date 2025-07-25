# Explicação Detalhada do Código Python

Olá! Como seu professor particular de Python, vou te guiar por cada parte deste código, explicando o que acontece em cada linha e por que ela é importante. Prepare-se para desvendar os segredos deste script!

Este programa tem como objetivo principal:

1.  **Conectar-se a um banco de dados SQLite**: Um banco de dados leve e fácil de usar, perfeito para projetos pequenos e médios.
2.  **Ler dados de cursos de um arquivo CSV**: CSV (Comma Separated Values) é um formato comum para armazenar dados tabulares.
3.  **Armazenar esses dados em uma tabela no banco de dados**.
4.  **Calcular estatísticas importantes sobre os cursos** (como o curso com maior carga horária ou maior valor).
5.  **Salvar essas estatísticas em outra tabela no banco de dados**.
6.  **Exibir as estatísticas na tela**.

Vamos começar!

## 1. Importação das Bibliotecas

Todo programa Python que usa funcionalidades extras precisa "importar" bibliotecas. Pense nelas como ferramentas que você pega da sua caixa de ferramentas para usar no seu projeto.

```python
import sqlite3  # Biblioteca para trabalhar com banco de dados SQLite
import csv      # Biblioteca para ler e escrever arquivos CSV
import os       # Biblioteca para trabalhar com caminhos de arquivos e sistema operacional
```

*   `import sqlite3`: Traz para o seu código tudo o que você precisa para interagir com bancos de dados SQLite. É como se você estivesse pegando a chave para abrir e manipular seu banco de dados.
*   `import csv`: Essencial para lidar com arquivos CSV. Com ela, você pode ler os dados organizados em colunas e linhas, como uma planilha simples.
*   `import os`: Esta biblioteca é super útil para interagir com o sistema operacional. No nosso caso, vamos usá-la para construir caminhos de arquivos de forma inteligente, garantindo que o código funcione tanto no Windows quanto no Linux ou macOS.

## 2. Definição dos Caminhos dos Arquivos

Para que o programa saiba onde encontrar o banco de dados e o arquivo CSV, precisamos dizer a ele o "endereço" desses arquivos. Fazemos isso de uma forma que o código seja flexível e funcione em diferentes computadores.

```python
# __file__ é uma variável especial que contém o caminho do arquivo atual
# os.path.dirname(__file__) pega o diretório onde este script está localizado
# '..' significa "subir um nível" na estrutura de pastas
# os.path.join() junta os caminhos de forma segura (funciona em Windows, Linux, Mac)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'cursos.csv')
```

*   `DB_PATH` e `CSV_PATH`: São variáveis que armazenam os caminhos completos para o seu arquivo de banco de dados (`db.sqlite3`) e seu arquivo de dados (`cursos.csv`).
*   `os.path.dirname(__file__)`: Isso é um truque inteligente! `__file__` é uma variável interna do Python que guarda o caminho completo do arquivo Python que está sendo executado. `os.path.dirname()` pega apenas o diretório (a pasta) onde esse arquivo está.
*   `'..'`: Isso significa "voltar uma pasta". Se o seu script está em `projeto/scripts/meu_script.py`, e o `db.sqlite3` está em `projeto/db.sqlite3`, você precisa "subir" da pasta `scripts` para a pasta `projeto`.
*   `os.path.join(...)`: Esta função é a melhor amiga de quem trabalha com caminhos de arquivo. Ela junta pedaços de caminhos de forma correta para o sistema operacional que você está usando (colocando barras `\` no Windows e `/` no Linux/macOS). Isso evita muitos erros!

## 3. Conectando ao Banco de Dados

Antes de fazer qualquer coisa com o banco de dados, precisamos nos conectar a ele. É como abrir um livro antes de começar a ler ou escrever nele.

```python
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
```

*   `conn = sqlite3.connect(DB_PATH)`: Esta linha estabelece a conexão com o banco de dados. Se o arquivo `db.sqlite3` não existir no caminho especificado, o SQLite o criará automaticamente para você. A variável `conn` (de "connection") agora representa essa conexão.
*   `cursor = conn.cursor()`: Um `cursor` é um objeto muito importante. Pense nele como um "ponteiro" ou um "agente" que você usa para enviar comandos SQL para o banco de dados e receber os resultados. Você não interage diretamente com a conexão para executar comandos, mas sim através do cursor.

## 4. Criando a Tabela `tb_cursos`

Um banco de dados é feito de tabelas, que são como planilhas. Precisamos definir a estrutura da nossa primeira tabela, `tb_cursos`, que vai guardar as informações sobre cada curso.

```python
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Chave primária que incrementa automaticamente
    curso TEXT NOT NULL,                   -- Nome do curso (texto obrigatório)
    carga_horaria INTEGER NOT NULL,        -- Carga horária em horas (número inteiro obrigatório)
    preco REAL NOT NULL                    -- Preço do curso (número decimal obrigatório)
)
''')
```

*   `cursor.execute(...)`: É aqui que enviamos comandos SQL para o banco de dados. O texto entre as três aspas simples (`'''`) é o comando SQL.
*   `CREATE TABLE IF NOT EXISTS tb_cursos`: Este comando SQL tenta criar uma tabela chamada `tb_cursos`. O `IF NOT EXISTS` é uma salvaguarda: se a tabela já existir, o comando simplesmente não faz nada, evitando um erro. Isso é ótimo para quando você executa o script várias vezes.
*   Dentro dos parênteses, definimos as colunas da tabela:
    *   `id INTEGER PRIMARY KEY AUTOINCREMENT`: Esta é a coluna de identificação única para cada curso. `INTEGER` significa que armazenará números inteiros. `PRIMARY KEY` indica que é a chave principal da tabela (cada `id` deve ser único). `AUTOINCREMENT` faz com que o SQLite preencha automaticamente este campo com um número sequencial a cada novo curso inserido.
    *   `curso TEXT NOT NULL`: Uma coluna para o nome do curso. `TEXT` armazena texto. `NOT NULL` significa que esta coluna não pode ficar vazia; todo curso deve ter um nome.
    *   `carga_horaria INTEGER NOT NULL`: Para a carga horária, armazenamos números inteiros (`INTEGER`). Também é `NOT NULL`.
    *   `preco REAL NOT NULL`: Para o preço, usamos `REAL`, que é o tipo de dado para números de ponto flutuante (números com casas decimais). Também é `NOT NULL`.

## 5. Lendo o Arquivo CSV e Inserindo os Dados

Agora que temos a tabela pronta, vamos pegar os dados do nosso arquivo `cursos.csv` e colocá-los lá dentro.

```python
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    cursos = [(row['curso'], int(row['carga_horaria']), float(row['preco'])) for row in reader]

# Limpar tabela antes de inserir (para evitar duplicidade em execuções repetidas)
cursor.execute('DELETE FROM tb_cursos')
cursor.executemany('INSERT INTO tb_cursos (curso, carga_horaria, preco) VALUES (?, ?, ?)', cursos)
conn.commit()
```

*   `with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:`:
    *   `with open(...)`: Esta é a maneira recomendada de abrir arquivos em Python. Ela garante que o arquivo será fechado automaticamente, mesmo que ocorra um erro.
    *   `CSV_PATH`: O caminho para o seu arquivo CSV que definimos lá em cima.
    *   `newline=''`: Isso é importante para o `csv` módulo. Ele evita que linhas em branco extras apareçam quando você lê o arquivo.
    *   `encoding='utf-8'`: Define a codificação de caracteres. `utf-8` é a mais comum e garante que caracteres especiais (como acentos e cedilhas) sejam lidos corretamente.
    *   `as csvfile`: O arquivo aberto é atribuído à variável `csvfile`.
*   `reader = csv.DictReader(csvfile)`: `csv.DictReader` é uma ferramenta fantástica. Ela lê o arquivo CSV e, para cada linha, cria um dicionário onde as chaves são os nomes das colunas (lidos da primeira linha do CSV) e os valores são os dados daquela linha. Isso torna o acesso aos dados muito mais fácil (ex: `row['curso']`).
*   `cursos = [(row['curso'], int(row['carga_horaria']), float(row['preco'])) for row in reader]`: Esta é uma **list comprehension**, uma forma muito Pythonica e eficiente de criar listas. Ela faz o seguinte:
    *   Para cada `row` (linha/dicionário) que o `reader` lê do CSV...
    *   Ela cria uma tupla `(row['curso'], int(row['carga_horaria']), float(row['preco']))`.
    *   `int(row['carga_horaria'])` e `float(row['preco'])`: Os dados lidos de um CSV são sempre strings (texto). Precisamos convertê-los para os tipos corretos (`int` para carga horária e `float` para preço) antes de inseri-los no banco de dados.
    *   O resultado é uma lista de tuplas, onde cada tupla contém os dados de um curso prontos para serem inseridos.
*   `cursor.execute('DELETE FROM tb_cursos')`: Antes de inserir os novos dados, esta linha apaga *todos* os registros existentes na tabela `tb_cursos`. Por que fazemos isso? Para evitar que, se você executar o script várias vezes, os dados sejam duplicados no banco. É uma forma de "limpar a lousa" antes de escrever de novo.
*   `cursor.executemany('INSERT INTO tb_cursos (curso, carga_horaria, preco) VALUES (?, ?, ?)', cursos)`:
    *   `executemany()`: Esta função é otimizada para inserir *muitas* linhas de uma vez. É muito mais eficiente do que usar `execute()` em um loop para cada linha.
    *   `'INSERT INTO tb_cursos (...) VALUES (?, ?, ?)'`: Este é o comando SQL para inserir dados. Os `?` são **placeholders** (marcadores de posição). Eles são substituídos pelos valores da lista `cursos` na ordem correta. Usar placeholders é uma prática de segurança fundamental, pois previne ataques de **SQL Injection**.
    *   `cursos`: É a lista de tuplas que criamos, contendo todos os dados dos cursos.
*   `conn.commit()`: **MUITO IMPORTANTE!** Quando você faz alterações no banco de dados (como inserir, atualizar ou deletar), essas mudanças ficam primeiro em uma área temporária. `conn.commit()` é o comando que salva essas mudanças permanentemente no arquivo do banco de dados. Se você esquecer o `commit()`, suas alterações não serão salvas!

## 6. Calculando Estatísticas

Com os dados no banco, podemos fazer perguntas a ele para extrair informações úteis. Isso é o que chamamos de "consultas" SQL.

```python
cursor.execute('SELECT COUNT(*) FROM tb_cursos')
qtd_cursos = cursor.fetchone()[0]

cursor.execute('SELECT curso, carga_horaria FROM tb_cursos ORDER BY carga_horaria DESC, id ASC LIMIT 1')
curso_maior_carga = cursor.fetchone()

cursor.execute('SELECT curso, preco FROM tb_cursos ORDER BY preco DESC, id ASC LIMIT 1')
curso_maior_valor = cursor.fetchone()
```

*   `cursor.execute('SELECT COUNT(*) FROM tb_cursos')`:
    *   `SELECT COUNT(*)`: Este comando SQL conta o número total de linhas (registros) na tabela `tb_cursos`.
*   `qtd_cursos = cursor.fetchone()[0]`:
    *   `cursor.fetchone()`: Após executar um `SELECT`, este método recupera a *próxima* linha de resultados. No caso de `COUNT(*)`, ele retorna uma tupla com um único valor (ex: `(10,)`).
    *   `[0]`: Acessamos o primeiro (e único) elemento dessa tupla para obter o número puro da quantidade de cursos.
*   `cursor.execute('SELECT curso, carga_horaria FROM tb_cursos ORDER BY carga_horaria DESC, id ASC LIMIT 1')`:
    *   `SELECT curso, carga_horaria`: Seleciona apenas as colunas `curso` e `carga_horaria`.
    *   `ORDER BY carga_horaria DESC`: Ordena os resultados pela `carga_horaria` em ordem **descendente** (do maior para o menor). Isso coloca o curso com maior carga horária no topo.
    *   `, id ASC`: Se houver dois cursos com a mesma carga horária máxima, este é um critério de desempate: ele ordena pelo `id` em ordem **ascendente** (do menor para o maior). Isso garante um resultado consistente.
    *   `LIMIT 1`: Retorna apenas a primeira linha do resultado (que será o curso com a maior carga horária).
*   `curso_maior_carga = cursor.fetchone()`: Armazena a tupla resultante (ex: `('Python Avançado', 80)`) na variável `curso_maior_carga`.
*   As linhas para `curso_maior_valor` seguem a mesma lógica, mas ordenam pelo `preco` para encontrar o curso mais caro.

## 7. Criando a Tabela `tb_estatisticas_cursos`

Para guardar as estatísticas que acabamos de calcular, criamos uma nova tabela.

```python
cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_estatisticas_cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    qtd_cursos INTEGER,                    -- Quantidade total de cursos
    curso_maior_carga_horaria TEXT,        -- Nome e carga do curso com mais horas
    curso_com_maior_valor TEXT             -- Nome e preço do curso mais caro
)
''')
# Limpar tabela antes de inserir
cursor.execute('DELETE FROM tb_estatisticas_cursos')
```

*   A estrutura é similar à da `tb_cursos`, mas com colunas para armazenar as estatísticas calculadas: `qtd_cursos`, `curso_maior_carga_horaria` e `curso_com_maior_valor`.
*   `TEXT` é usado para as colunas de curso com maior carga/valor porque vamos formatar essas informações como strings (ex: "Python (80 horas)").
*   `cursor.execute('DELETE FROM tb_estatisticas_cursos')`: Novamente, limpamos a tabela antes de inserir para evitar duplicidade se o script for executado múltiplas vezes.

## 8. Inserindo as Estatísticas

Agora, pegamos os valores das estatísticas que calculamos e os inserimos na nova tabela.

```python
cursor.execute(
    'INSERT INTO tb_estatisticas_cursos (qtd_cursos, curso_maior_carga_horaria, curso_com_maior_valor) VALUES (?, ?, ?)',
    (
        qtd_cursos,  # Quantidade de cursos
        # f-string: forma moderna de formatar strings em Python
        # curso_maior_carga[0] é o nome do curso, [1] é a carga horária
        f"{curso_maior_carga[0]} ({curso_maior_carga[1]} horas)",
        # :.2f formata o número com 2 casas decimais
        f"{curso_maior_valor[0]} (R$ {curso_maior_valor[1]:.2f})"
    )
)
conn.commit()
```

*   `INSERT INTO tb_estatisticas_cursos (...) VALUES (?, ?, ?)`: Comando SQL para inserir uma nova linha na tabela de estatísticas.
*   Os valores são passados como uma tupla:
    *   `qtd_cursos`: O número inteiro que já calculamos.
    *   `f"{curso_maior_carga[0]} ({curso_maior_carga[1]} horas)"`: Aqui usamos uma **f-string** (formatted string literal), uma forma super prática de formatar strings em Python. Ela permite que você incorpore variáveis e expressões diretamente dentro de uma string, usando chaves `{}`. Estamos pegando o nome do curso (`curso_maior_carga[0]`) e sua carga horária (`curso_maior_carga[1]`) e formatando-os em uma única string legível.
    *   `f"{curso_maior_valor[0]} (R$ {curso_maior_valor[1]:.2f})"`: Similarmente, formatamos o nome do curso mais caro e seu preço. O `: .2f` dentro das chaves é um formatador que diz: "formate este número de ponto flutuante com duas casas decimais". Isso é ótimo para exibir valores monetários.
*   `conn.commit()`: Novamente, confirmamos as alterações no banco de dados para que as estatísticas sejam salvas permanentemente.

## 9. Exibindo Estatísticas na Tela

Finalmente, vamos mostrar os resultados para o usuário no console.

```python
print(f"Quantidade de cursos: {qtd_cursos}")
print(f"Curso com a maior carga horária: {curso_maior_carga[0]} ({curso_maior_carga[1]} horas)")
print(f"Curso com o maior valor: {curso_maior_valor[0]} (R$ {curso_maior_valor[1]:.2f})")
```

*   `print(...)`: A função `print()` é usada para exibir texto na tela (no seu terminal ou console).
*   Aqui, novamente usamos **f-strings** para criar mensagens claras e informativas, incorporando os valores das variáveis que calculamos.

## 10. Fechando a Conexão com o Banco

É uma boa prática sempre fechar a conexão com o banco de dados quando você termina de usá-lo. Isso libera recursos e garante que todas as operações pendentes sejam finalizadas.

```python
conn.close()
```

*   `conn.close()`: Fecha a conexão com o banco de dados. Simples e eficaz!

--- 

Espero que esta explicação detalhada tenha sido útil para você! Se tiver mais alguma dúvida, é só perguntar. Continue praticando e explorando o mundo da programação!



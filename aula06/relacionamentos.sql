/*

Relacionamento entre tabelas em um banco de dados.

Um banco de dados relacional possui esse nome pois permite criar relaciomentos
entre as suas entidades, que podemos chamar de tabelas. Dentro de um banco de
dados relacional, podemos ter 3 níveis de relacionamento entre tabelas:

1:1 -> Um para um
1:N -> Um para muitos
N:N -> Muitos para muitos.

Entender como as tabelas se relacionam é um passo fundamental na fase de
modelagem de dados da nossa aplicação. Relacionamentos mal definidos podem levar
a perda de consistência e confiabilidade dos dados.

Para ilustrar os níveis de relacionamento, vamos montar a estrutura de banco de
dados de uma aplicação de blog, onde o usuário pode criar postagens, comentários,
etc.

Nesse caso, nosso sistema terá 5 entidades (tabelas):
* Tabela para os Usuarios
* Tabela para os Perfis
* Tabela para as Postagens
* Tabela para as Categorias
* Tabela para os Comentários

* No caso dos dados do usuário, separamos em 2 tabelas: Uma para os dados de
acesso (email, senha, etc) e outra para os dados pessoais (nome, genero, etc)
*/

CREATE DATABASE IF NOT EXISTS relacionamentos;

CREATE TABLE IF NOT EXISTS usuarios(
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(100) NOT NULL,
	senha VARCHAR(100) NOT NULL,
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP()
);
SELECT * FROM usuarios;

CREATE TABLE IF NOT EXISTS perfis(
	id INT PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	data_de_nascimento DATE NULL,
	genero VARCHAR(50) NULL
-- 	FOREIGN KEY(id) REFERENCES usuarios(id)
);

-- Caso você queira adicionar a chave estrangeira depois
ALTER TABLE perfis ADD FOREIGN KEY(id) REFERENCES usuarios(id);

/*
Acima, criamos um relacionamento entre as tabelas usuarios e perfis. Utilizamos
a instrução FOREIGN KEY... REFERENCES para criar essa ligação. Como criamos
essa ligação na coluna id de perfis, que também é chave primária, os valores
dessa coluna ao mesmo tempo que não devem se repetir, devem existir na tabela
usuarios (tabela referenciada). Abaixo veremos alguns exemplos.
*/

INSERT INTO usuarios(email, senha) VALUES (
	'joao.silva@email.com', 'joao123'
);
INSERT INTO usuarios(email, senha) VALUES ( 
	'maria.batista@email.com', 'maria123'
);
INSERT INTO usuarios(email, senha) VALUES (
	'barbara.barreto@email.com', 'barbara123'
);
SELECT * FROM usuarios;

INSERT INTO perfis(id, nome, data_de_nascimento, genero) VALUES (
	1, 'João da Silva', '1980-11-17', 'Masculino'
);
INSERT INTO perfis(id, nome, data_de_nascimento, genero) VALUES (
	2, 'Maria Batista', NULL, 'Feminino'
);
SELECT * FROM perfis;

/*
Acima garantimos a aplicação do relacionamento 1:1, garantindo que não haverá
valores repetidos para as colunas id das tabelas usuarios e perfis, e garantindo
que os valores da coluna id da tabela perfis existem na tabela usuarios
*/

/*
No caso dos dados da postagem, temos que armazenar as seguintes informações:

* id da postagem
* id do usuario que fez a postagem
* titulo da postagem
* texto da postagem
* data e hora de criacão da postagem
*/

CREATE TABLE IF NOT EXISTS postagens(
	id INT PRIMARY KEY AUTO_INCREMENT,
	usuario_id INT NOT NULL,
	titulo VARCHAR(100) NOT NULL,
	texto VARCHAR(1000) NOT NULL,
	criado_em DATETIME DEFAULT CURRENT_TIMESTAMP(),
	FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
);

INSERT INTO postagens(usuario_id, titulo, texto) VALUES
	(1, 'A linguagem Python', 'Python é especialmente usada em dados.'),
	(1, 'A linguagem Assembly', 'Assembly é utilizado em baixo nível.'),
	(2, 'A linguagem Java', 'Java é largamento utilizado.');
SELECT * FROM postagens;

SELECT a.id, a.email, b.titulo FROM usuarios a
INNER JOIN postagens b
ON a.id = b.usuario_id;

/*
Com isso garantimos o relacionamento 1:N entre as entidades usuarios e
postagens. Um usuário pode realizar diversas postagens, enquanto uma postagem
pode ter apenas 1 autor (usuario). Para isso criamos a coluna usuario_id na
tabela de postagens e a definimos como uma chave estrangeira que referencia
a coluna id da tabela usuarios.
*/

/*
Para a criação da tabela de categorias, vamos precisar apenas da coluna nome.
Uma categoria pode ser atribuída a diversas postagens, enquanto uma postagem
pode ter diversas categorias atribuídas a ela.
*/

CREATE TABLE IF NOT EXISTS categorias(
	id INT PRIMARY KEY AUTO_INCREMENT,
	nome VARCHAR(100) NOT NULL
);
DESC categorias;

INSERT INTO categorias (nome) VALUES
	('python'),
	('programacao'),
	('sql'),
	('proway'),
	('linux');

/*
Como temos uma relação de N:N entre as tabelas postagens e categorias, precisamos
criar uma outra tabela, que chamamos de tabela associativa. Como o próprio nome
diz, é a tabela que irá associar os dados relacionados entre postagens e
categorias
*/

CREATE TABLE IF NOT EXISTS postagens_categorias(
	postagem_id INT NOT NULL,
	categoria_id INT NOT NULL,
	PRIMARY KEY(postagem_id, categoria_id),
	FOREIGN KEY(postagem_id) REFERENCES postagens(id),
	FOREIGN KEY(categoria_id) REFERENCES categorias(id)
);

-- Associando a postagem "A Linguagem Python" com as categorias
-- "python" e "programacao"
INSERT INTO postagens_categorias(postagem_id, categoria_id)
VALUES
	(1, 1),
	(1, 2);

SELECT p.id, p.titulo, c.nome FROM postagens p 
INNER JOIN postagens_categorias pc
ON p.id = pc.postagem_id
INNER JOIN categorias c 
ON pc.categoria_id = c.id
WHERE p.id = 1;

/*
Acima garantimos o relacionamento N:N entre as tabelas postagens e categorias.
Foi criada a tabela associativa postagens_categorias que terá as colunas
associadas a cada coluna id das tabelas postagens e categorias, permitindo
a associação entre essas 2 tabelas.
*/
<h1 align="center"> Projeto-Redes1</h1>
<p align="center">Implementação de socket utilizando a linguagem Python para a disciplina de Redes de Computadores1</p>

**Alunos:** [Emily Brito de Oliveira](https://github.com/Emilybtoliveira) e [Felipe Ferreira Vasconcelos](https://github.com/felipeVsc)

<h3> Pré-requisitos: </h3>

  * Python 3 

<h3>Como rodar?</h3> 

Após baixar o código source, navegue via terminal/cmd até a pasta *src* `/Projeto-Redes1/src` e inicialize primeiramente o arquivo "***servidor.py***".

```bash
python servidor.py
```
ou
```bash
python3 servidor.py
```

É necessário manter este terminal sendo único, além de estar ativo e rodando o arquivo, para que o servidor que irá lidar com o socket TCP possa estar online.

**Em uma segunda janela de terminal,** inicialize o arquivo "***cliente.py***", da mesma forma que foi inicializado o servidor.

```bash
python cliente.py
```
ou
```bash
python3 cliente.py
```

Não existe limitação para a criação de instâncias de ***cliente.py***, ou seja, poderá ser feita a inicialização de vários arquivos em janelas de terminal diferentes, cada um correspondente a um cliente.

 Após a inicialização dos arquivos, é necessário prover um nome de usuário, que irá ficar salvo no arquivo "***usuarios.txt***". Em seguida, o programa seguirá para a tela de chat.

Para uma melhor exemplificação do software, recomendamos abrir, pelo menos, duas instâncias de ***cliente.py*** e utilizar nomes diferentes, de modo que você reproduzir uma conversa.

<h3>Resumo do passo a passo da execução</h3> 

1. Inicializar ***servidor.py***
2. Inicializar, pelo menos, duas instâncias de ***cliente.py***
3. Entrar com usuários diferentes nas instâncias de ***cliente.py***
4. Conversar

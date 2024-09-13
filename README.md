# Teste prático para cargo de Desenvolvedor RPA Pleno na empresa A&C

## DESCRIÇÃO
- Este projeto é um aplicativo web desenvolvido em Python utilizando Flask e SQLAlchemy, com automação de tarefas usando Selenium. O objetivo é criar um sistema que permita login de usuários, realizar automação de navegação e exportação de dados para um banco de dados e arquivos CSV/Excel.

## TECNOLOGIAS UTILIZADAS
-  Linguagens: Python
-  Bibliotecas: Selenium e Beautiful Soup 4

## ESTRUTURA DO PROJETO

- `app.py`: Arquivo principal do aplicativo Flask.
- `libraries.py`: Arquivo contendo as importações de bibliotecas.
- `automation.log`: Arquivo de log para registrar eventos e erros.
- `templates/`: Diretório contendo os templates HTML.

## Descrição das Funcionalidades

### 1. Configuração Inicial

- **Importação de Bibliotecas**: Importa as bibliotecas necessárias como Flask, SQLAlchemy, Selenium, entre outras.
- **Configuração do Logging**: Configura o logging para registrar eventos e erros no arquivo `automation.log`.
- **Configuração do Banco de Dados**: Configura a conexão com o banco de dados SQL Server usando SQLAlchemy e cria a tabela `books`.

### 2. Funções Auxiliares

- **log_event**: Registra eventos e erros no arquivo de log.
- **connect_with_retry**: Tenta conectar ao banco de dados com múltiplas tentativas em caso de falha.

### 3. Rotas do Flask

- **Rota `/`**: Renderiza a página inicial.
- **Rota `/login`**: Processa o login do usuário e inicia a automação se as credenciais estiverem corretas.

### 4. Automação com Selenium

- **run_automation_task**: Executa uma função de automação e registra eventos e erros.
- **automate_section**: Automação genérica para seções do site demoqa.com.
- **bookstore**: Automação específica para a seção "Book Store Application", que coleta dados de livros e os salva no banco de dados e em arquivos CSV/Excel.

### 5. Execução do Aplicativo

- **automation**: Função que coordena a execução de todas as automações configuradas.
- **if __name__ == '__main__'**: Inicia o servidor Flask em modo debug.

## Relatório de Entrega

Durante a execução e desenvolvimento me deparei com alguns erros de sintaxe de busca das tags e seletores utilizando a biblioteca Selenium. Não houve dificuldade, mas sim um teste de adaptação entre utilizar o `By.CSS_SELECTOR` e o `By.XPATH`. Utilizando o `By.CSS_SELECTOR` verifiquei um resultado mais satisfatório, pois o processamento ocorreu em menos tempo do que se estivesse utilizando `By.XPATH`.

Ocorreram alguns erros na conexão com o banco de dados, pois a versão do driver não era compatível e o nome do servidor estava incorreto. Após a correção, funcionou normalmente.

No início do desenvolvimento, decidi fazer uma função para cada seção da página a ser automatizada para entender se haveria algum comportamento diferente entre as seções. Após entender que os processos eram similares, resolvi simplificar o código para otimizar o tempo de execução e diminuir a quantidade de linhas tanto no script principal quanto no arquivo de log.

Ocorreram alguns erros de digitação, mas coisas simples que não demandaram muito tempo para ser solucionadas.

Na parte de exportação dos dados não houve nenhuma dificuldade.

No desenvolvimento da aplicação desktop não houve dificuldades relevantes, apenas foi necessário determinar a sequência correta das etapas emuladas pelas tarefas feitas por um humano para criar um alarme com as características apresentadas.

Após a perfeita compreensão dos passos para se fazer uma determinada ação repetitiva como a criação de um alarme, ficou claro como deveria elaborar a codificação e automação do processo.

Para utilizar os testes foi utilizado as bibliotecas `unittest` para o aplicativo desktop e `flask-testing` e `pytest` para a aplicação web. Os nomes dos arquivos de teste seguem o mesmo nome dos arquivos originais, adicionando o termo `test_` no início do nome do arquivo.

## Tecnologias Utilizadas

- Linguagem Python e bibliotecas internas
- Biblioteca Selenium
- Biblioteca Pandas
- SQL Server Developer 2022
- Visual Studio Code
- Navegador Google Chrome


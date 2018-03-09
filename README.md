# PRTGbot
Um bot para automatizar ações da ferramenta de monitoramento PRTG.

## Como usar
Linha 42: Edite **PRTG_USER** e **PRTG_PASSWORD** passando as credenciais de acesso da ferramenta.<br>
Linha 57: Inserir endereço de e-mail remetente, que irá enviar o relatório (alias ou conta SMTP).<br>
Linha 58: Inserir destinatário. Conta que irá receber o relatório.<br>
Linha 67: Inserir servidor e porta SMTP.<br>
Linha 68: Atenticação SMTP.<br>
Linha 135 a 150: Edite passando IP - ou DNS - e porta de acesso ao NOC do PRTG. Adeque a quantidade de acordo com o que for necessário.

## Funções
Na versão 1.0 o bot apenas tem a função de gerar um relatório HTML com todos os acionadores que estiverem com status diferente de OK.

## Autores
[Danilo Moschem](https://github.com@github.com/moscaca)<br>
[Rodrigo Lopes](https://github.com@github.com/rodrigo-apoc)
# Decisões do Projeto - Monitoramento de IA no Piauí

## 1. Objetivo
Monitorar notícias sobre **Inteligência Artificial no Piauí** e analisar o sentimento do conteúdo, permitindo identificar percepções positivas, negativas ou neutras.

## 2. Abordagem de Sentimento
Escolhi uma **análise baseada em regras com palavras-chave** em vez de um modelo de Machine Learning por alguns motivos:
- O projeto tem escopo pequeno e limitado a notícias de um contexto específico (Piauí), tornando a abordagem de regras mais simples e eficiente.
- Evita a necessidade de treinar modelos complexos ou depender de grandes volumes de dados rotulados.
- Permite fácil manutenção e compreensão do critério de classificação.

## 3. Tecnologias
- **Python** como linguagem principal
- **Streamlit** para criar o dashboard interativo
- **Pandas** para manipulação de dados
- **Requests** para acessar RSS do Google Notícias
- **BeautifulSoup** e **lxml** para limpeza de HTML
- **Plotly** e **Matplotlib / WordCloud** para visualizações
- **XlsxWriter** para exportar Excel
- Suporte a CSV, Excel e JSON como formatos de exportação

## 4. Funcionalidades
- Coleta de notícias via RSS usando palavras-chave
- Limpeza e normalização do texto das notícias
- Análise de sentimento baseada em palavras-chave
- Visualizações interativas:
  - Gráfico de pizza com a distribuição de sentimentos
  - Nuvem de palavras com termos mais frequentes
  - Tabela com títulos, links, sentimentos e datas
- Download de dados nos formatos **CSV**, **Excel** e **JSON**
- Filtro opcional por data de publicação

## 5. Tratamento de Erros
- Caso o feed RSS não retorne notícias ou ocorra algum erro na requisição:
  - O dashboard exibe mensagens de alerta ao usuário.
  - A aplicação continua rodando sem travar.
- Permite que o usuário ajuste palavras-chave e quantidade de notícias para melhorar a coleta.

## 6. Observações
- A análise de sentimento é **simplificada** e não considera contexto avançado ou sarcasmo.
- O projeto foi estruturado para ser facilmente expandido com novas funcionalidades futuramente.

# Monitoramento de Percepção sobre Inteligência Artificial no Piauí

Este projeto tem como objetivo **monitorar notícias sobre Inteligência Artificial no Piauí**, realizando uma **análise de sentimento simples** e gerando um **dashboard interativo** usando Streamlit. O painel permite visualizar a percepção pública em termos de sentimentos positivos, negativos ou neutros, além de mostrar os termos mais frequentes nas notícias.

---

#Funcionalidades

* Coleta de notícias via **RSS do Google Notícias** usando palavras-chave como "Inteligência Artificial Piauí".
* Limpeza de texto e remoção de HTML.
* Classificação de sentimento baseada em **palavras-chave**:
  - Positivo: avanços, benefícios, inovação, progresso, etc.
  - Negativo: riscos, problemas, falhas, ameaças, etc.
* Dashboard interativo com Streamlit, incluindo:
  - Gráfico de pizza da distribuição de sentimentos.
  - Nuvem de palavras com termos mais frequentes.
  - Tabela interativa com títulos, links, sentimentos e datas.
- **Download de dados** em:
  - CSV
  - Excel
  - JSON
* Filtro opcional por **data de publicação**.
* Aviso sobre limitações da análise de sentimento.



# Instalação e execução

1. Clone o repositório:

	git clone https://github.com/Carlosm544/monitoramento-ia-piaui.git

2. Acesse a pasta do projeto:

	cd monitoramento-ia-piaui

3. Instale as dependências:

	pip install -r requirements.txt

4. Execute o dashboard:
	streamlit run main.py


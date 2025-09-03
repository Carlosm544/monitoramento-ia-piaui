import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
from bs4 import BeautifulSoup
import html
import io
from datetime import datetime

# Configuração da página 
st.set_page_config(page_title="Monitoramento IA Piauí", layout="wide")

# Inicialização do Session_state 
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame()

# Funções auxiliares 
def build_rss_url(query: str) -> str:
    from urllib.parse import quote_plus
    return f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=pt-BR&gl=BR&ceid=BR:pt-419"

def fetch_rss_items(query: str, limit: int = 15):
    """Busca notícias no RSS do Google com tratamento de erros"""
    url = build_rss_url(query)
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Erro ao buscar notícias: {e}")
        return []

    root = ET.fromstring(resp.content)
    noticias = []
    for item in root.findall(".//item")[:limit]:
        titulo = html.unescape((item.findtext("title") or "").strip())
        link = (item.findtext("link") or "").strip()
        desc = html.unescape((item.findtext("description") or "").strip())
        pubdate = item.findtext("pubDate")
        try:
            data_pub = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z") if pubdate else None
        except:
            data_pub = None
        noticias.append({
            "titulo": titulo,
            "link": link,
            "descricao": desc,
            "data": data_pub
        })
    return noticias

def clean_html(texto: str) -> str:
    if not texto:
        return ""
    soup = BeautifulSoup(texto, "html.parser")
    clean = soup.get_text(separator=" ")
    return re.sub(r"\s+", " ", clean).strip().lower()

def classificar_sentimento(texto: str) -> str:
    positivas = ["avanço", "benefício", "positivo", "inovação", "melhoria", "progresso"]
    negativas = ["problema", "risco", "falha", "crítico", "ameaça", "preocupação"]

    score = sum(bool(re.search(rf"\b{p}\b", texto)) for p in positivas) - \
            sum(bool(re.search(rf"\b{n}\b", texto)) for n in negativas)

    if score > 0:
        return "Positivo"
    elif score < 0:
        return "Negativo"
    return "Neutro"

# Interface 
st.title("📊 Monitoramento de Percepção sobre IA no Piauí")
st.caption("⚠️ Análise simples baseada em palavras-chave, sem considerar contexto ou sarcasmo.")

# SIDEBAR!
st.sidebar.header("Parâmetros")
query = st.sidebar.text_input("Buscar por:", "Inteligência Artificial Piauí")
limite = st.sidebar.slider("Quantidade de notícias", 5, 30, 15)
atualizar = st.sidebar.button("🔄 Atualizar notícias")
filtro_data = st.sidebar.date_input("Filtrar a partir de:", value=None)

# Pipeline 
if atualizar:
    with st.spinner("Buscando notícias..."):
        noticias = fetch_rss_items(query, limit=limite)
        df = pd.DataFrame(noticias)
        if not df.empty:
            df["descricao_limpa"] = df["descricao"].apply(clean_html)
            df["sentimento"] = df["descricao_limpa"].apply(classificar_sentimento)
            st.session_state.df = df
        else:
            st.warning("Nenhuma notícia encontrada.")

# Se existe dataframe 
if not st.session_state.df.empty:
    df = st.session_state.df.copy()
    if filtro_data:
        df = df[df["data"] >= pd.to_datetime(filtro_data)]

    # Visualização
    st.subheader("Distribuição de sentimentos")
    if not df.empty:
        fig_pizza = px.pie(df, names="sentimento", title="Positivo x Negativo x Neutro")
        st.plotly_chart(fig_pizza, use_container_width=True)
    else:
        st.warning("Nenhuma notícia disponível para gerar o gráfico de sentimentos.")

    st.subheader("Nuvem de palavras")
    texto = " ".join(df["descricao_limpa"])
    if texto.strip():
        wc = WordCloud(width=800, height=400, background_color="white").generate(texto)
        fig, ax = plt.subplots()
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("Não há texto suficiente para gerar a nuvem de palavras.")

    # Tabela com índice correto
    tabela_final = df[["titulo", "sentimento", "link", "data"]].reset_index(drop=True)
    tabela_final.index = tabela_final.index + 1
    st.subheader("Tabela de notícias coletadas")
    st.dataframe(tabela_final, use_container_width=True)

    # Exportar CSV
    csv = tabela_final.to_csv(index=False, sep=";", encoding="utf-8-sig")
    st.download_button("⬇️ Baixar CSV", data=csv, file_name="noticias.csv", mime="text/csv")

    # Exportar Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        tabela_final.to_excel(writer, index=False, sheet_name="Notícias")
    st.download_button("⬇️ Baixar Excel", data=output.getvalue(), file_name="noticias.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Exportar JSON
    json_data = tabela_final.to_json(orient="records", force_ascii=False, indent=4)
    st.download_button("⬇️ Baixar JSON", data=json_data, file_name="noticias.json", mime="application/json")

else:
    st.info("Clique em **🔄 Atualizar notícias** para começar a coleta.")

# Rodapé fixo
rodape = """
<style>
footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background-color: #E0F2FE;
    color: #000;
    text-align: center;
    padding: 10px 0;
    font-size: 14px;
    box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
}
</style>

<footer>
⚠️ Esta análise é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos.
</footer>
"""
st.markdown(rodape, unsafe_allow_html=True)

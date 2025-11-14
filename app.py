import streamlit as st
from google import genai
import time 

# ----------------------------------------------------
# 1. Configuração e Inicialização do Gemini
# ----------------------------------------------------

try:
    # Tenta carregar a chave de API de forma segura
    API_KEY = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=API_KEY)
except (KeyError, FileNotFoundError):
    st.error("ERRO: Chave 'GEMINI_API_KEY' não encontrada. Verifique o arquivo .streamlit/secrets.toml.")
    st.stop()

# ----------------------------------------------------
# 2. Funções Essenciais
# ----------------------------------------------------

# **SIMULAÇÃO DE WEB SCRAPING**
# Em um projeto real, você usaria 'requests' e 'BeautifulSoup' aqui.
def simular_extracao_produto(url):
    """Simula a extração de dados básicos do link."""
    st.info(f"Simulando análise do link: {url}...")
    time.sleep(1) # Simula o tempo de carregamento
    
    # Dados fictícios que seriam extraídos
    return {
        "nome": "Smartwatch Pro Max 3",
        "caracteristicas_principais": [
            "Monitoramento de Oxigênio (SpO2)", 
            "GPS Integrado", 
            "Bateria de 7 dias",
            "Design ultra-fino"
        ],
        "imagens_urls": ["url_imagem_1", "url_imagem_2"], # URLs para a aba de vídeo
        "videos_urls": ["url_video_demo"]
    }

def gerar_texto_viral(nome_produto, caracteristicas):
    """Gera o texto de venda viral usando o modelo Gemini 2.5 Flash."""
    
    caracteristicas_str = ", ".join(caracteristicas)
    
    prompt = f"""
    Crie um texto de venda altamente viral e chamativo para o produto: {nome_produto}. 
    O texto deve ser curto (máximo 4 parágrafos), emocionante e focado em mídias sociais.
    Destaque as seguintes características de forma criativa: {caracteristicas_str}.
    Inclua uma Chamada para Ação (CTA) forte no final.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Erro na Geração de Texto: {e}"

# ----------------------------------------------------
# 3. Funções de Criação de Vídeo (SIMULAÇÃO)
# ----------------------------------------------------

def simular_montagem_video(nome_produto, texto_final):
    """Simula a etapa de Text-to-Speech e Edição de Vídeo (MoviePy/TTS API)."""
    
    st.caption("*(Simulando conversão do texto para áudio e montagem das imagens...)*")
    
    # Simula a duração da narração
    duracao_audio = len(texto_final) * 0.05
    st.info(f"Gerando Narração TTS de {duracao_audio:.1f} segundos...")
    time.sleep(2)
    
    # Simula a renderização
    st.info("Montando vídeo com MoviePy e sincronizando com a narração...")
    time.sleep(3) 
    
    st.success(f"✅ Vídeo 'Promoção {nome_produto}' renderizado com sucesso!")
    st.balloons()
    st.markdown(f"**Saída:** Vídeo MP4 criado com áudio gerado a partir do texto.")

# ----------------------------------------------------
# 4. Interface Streamlit
# ----------------------------------------------------

st.set_page_config(layout="wide", page_title="Gerador Viral")
st.title("✨ Gerador de Conteúdo de Venda Viral")
st.markdown("Insira o link, gere o texto e crie um vídeo promocional rapidamente.")

# Campo para a URL do produto
url_produto = st.text_input(
    "🔗 **1. Link do Produto:**", 
    "https://loja.exemplo.com/smartwatch-pro-max"
)

# Criação das duas abas (funcionalidade solicitada)
tab1, tab2 = st.tabs(["✍️ Gerar e Editar Texto", "🎬 Criar Vídeo Promocional"])

# --- TAB 1: Geração de Texto ---
with tab1:
    
    if st.button("🚀 Gerar Texto de Venda com IA"):
        
        # Etapa A: Simular Extração de Dados
        st.session_state['produto_data'] = simular_extracao_produto(url_produto)
        data = st.session_state['produto_data']
        
        st.subheader(f"Produto: {data['nome']}")
        
        # Etapa B: Geração do Texto pela IA
        with st.spinner("🧠 A IA está escrevendo seu texto viral..."):
            texto_gerado = gerar_texto_viral(data['nome'], data['caracteristicas_principais'])
            st.session_state['texto_viral'] = texto_gerado
        
        st.success("Texto Gerado! Agora você pode editá-lo.")

    # Área de Texto Editável
    if 'texto_viral' in st.session_state:
        st.text_area(
            "**2. Texto Viral Editável (Base para a Narração):**",
            value=st.session_state['texto_viral'],
            height=300,
            key='texto_final_para_video' # O texto final é salvo aqui
        )
        st.markdown("---")
        st.info("💡 Vá para a aba 'Criar Vídeo Promocional' para finalizar.")


# --- TAB 2: Criação de Vídeo ---
with tab2:
    if 'produto_data' not in st.session_state:
        st.warning("🚨 Por favor, primeiro preencha o link e clique em 'Gerar Texto de Venda com IA' na aba anterior.")
    else:
        # Puxa o produto e o texto final editado
        data = st.session_state['produto_data']
        texto_para_narra = st.session_state['texto_final_para_video']
        
        st.markdown(f"**Produto:** {data['nome']}")
        st.markdown(f"**Mídia (Simulada):** {len(data['imagens_urls'])} Imagens, {len(data['videos_urls'])} Vídeos.")

        st.markdown("---")

        if st.button("▶️ INICIAR Criação do Vídeo (Narração + Montagem)"):
            simular_montagem_video(data['nome'], texto_para_narra)

# FIM DO CÓDIGO
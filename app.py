import streamlit as st
import pandas as pd
from datetime import datetime
import google.generativeai as genai

# Configuração da página
st.set_page_config(
    page_title="Gerador de Textos Virais",
    page_icon="🚀",
    layout="wide"
)

# Configurar a API do Gemini
API_KEY = "AIzaSyD5Wx6YyhFBt__GVd2HYht3LmpTJd66erA"  # Substitua pela sua chave API
genai.configure(api_key=API_KEY)

# Título principal
st.title("🚀 Gerador de Textos Virais para Marketing")
st.markdown("---")

# Sidebar para upload de arquivo
with st.sidebar:
    st.header("📁 Upload de Dados")
    uploaded_file = st.file_uploader("Carregue seu arquivo CSV com dados dos produtos", type=['csv'])
    
    st.markdown("---")
    st.header("⚙️ Configurações")
    tom = st.selectbox(
        "Tom do texto:",
        ["Entusiasta", "Profissional", "Casual", "Humorístico", "Inspirador"]
    )
    
    tamanho = st.selectbox(
        "Tamanho do texto:",
        ["Curto (até 50 palavras)", "Médio (50-100 palavras)", "Longo (100+ palavras)"]
    )

# Área principal
if uploaded_file is not None:
    # Carregar dados
    df = pd.read_csv(uploaded_file)
    
    # Mostrar preview dos dados
    st.header("📊 Preview dos Dados")
    st.dataframe(df.head())
    
    # Seleção do produto
    st.header("🎯 Selecione o Produto")
    produto_selecionado = st.selectbox(
        "Escolha um produto:",
        df.index.tolist(),
        format_func=lambda x: f"{df.iloc[x]['nome_produto'] if 'nome_produto' in df.columns else df.iloc[x][0]}"
    )
    
    # Mostrar detalhes do produto selecionado
    st.subheader("Detalhes do Produto Selecionado:")
    produto_info = df.iloc[produto_selecionado]
    st.json(produto_info.to_dict())
    
    # Botão para gerar texto
    if st.button("✨ Gerar Texto Viral", type="primary"):
        with st.spinner("Gerando texto viral..."):
            # Preparar o prompt
            prompt = f"""
            Crie um texto de marketing viral para o seguinte produto:
            
            Detalhes do produto:
            {produto_info.to_dict()}
            
            Tom desejado: {tom}
            Tamanho: {tamanho}
            
            O texto deve ser:
            - Cativante e viral
            - Focado nos benefícios do produto
            - Adequado para redes sociais
            - Incluir call-to-action
            """
            
            try:
                # Gerar conteúdo usando Gemini
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                texto_gerado = response.text
                
                # Mostrar resultado
                st.success("✅ Texto gerado com sucesso!")
                st.header("📝 Texto Gerado:")
                st.markdown(f"**{texto_gerado}**")
                
                # Opções de ação
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Baixar Texto",
                        data=texto_gerado,
                        file_name=f"texto_viral_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
                with col2:
                    if st.button("📋 Copiar para Área de Transferência"):
                        st.code(texto_gerado)
                
                # Salvar histórico
                if 'historico' not in st.session_state:
                    st.session_state.historico = []
                
                st.session_state.historico.append({
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'produto': produto_info.to_dict(),
                    'texto': texto_gerado
                })
                
            except Exception as e:
                st.error(f"❌ Erro ao gerar texto: {str(e)}")
    
    # Mostrar histórico
    if 'historico' in st.session_state and len(st.session_state.historico) > 0:
        st.markdown("---")
        st.header("📚 Histórico de Textos Gerados")
        for i, item in enumerate(reversed(st.session_state.historico)):
            with st.expander(f"Texto {len(st.session_state.historico) - i} - {item['data']}"):
                st.write("**Produto:**", item['produto'])
                st.write("**Texto Gerado:**")
                st.markdown(item['texto'])

else:
    st.info("👆 Por favor, faça upload de um arquivo CSV na barra lateral para começar.")
    
    # Instruções
    st.markdown("""
    ### 📋 Como usar:
    
    1. **Upload**: Carregue um arquivo CSV com os dados dos seus produtos
    2. **Configure**: Escolha o tom e tamanho do texto desejado
    3. **Selecione**: Escolha o produto para gerar o texto
    4. **Gere**: Clique no botão para criar o texto viral
    5. **Use**: Baixe ou copie o texto gerado
    
    ### 📊 Formato do CSV:
    
    Seu arquivo CSV deve conter colunas como:
    - `nome_produto`: Nome do produto
    - `descricao`: Descrição do produto
    - `preco`: Preço do produto
    - `categoria`: Categoria do produto
    - Outras informações relevantes
    """)

# Footer
st.markdown("---")
st.markdown("🚀 Gerador de Textos Virais - Powered by Google Gemini")

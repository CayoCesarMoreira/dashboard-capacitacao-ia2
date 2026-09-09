import os
import io
import re
# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
import plotly.express as px
# pyrefly: ignore [missing-import]
import plotly.graph_objects as go

# ==============================================================================
# CONFIGURAÇÃO GERAL DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Dashboard | Capacitação em IA, ML & Ciência de Dados",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ESTILIZAÇÃO CSS — PALETA OFICIAL CIIA
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0D1B2A;
        color: #F2F2F2;
    }

    /* Fundo principal da app */
    .stApp {
        background-color: #0D1B2A;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A2B3C !important;
        border-right: 1px solid rgba(45, 109, 166, 0.3);
    }
    [data-testid="stSidebar"] * {
        color: #F2F2F2 !important;
    }

    /* ── Hero Container ── */
    .hero-container {
        background: linear-gradient(135deg, #003F71 0%, #1A2B3C 55%, #0D1B2A 100%);
        border: 1px solid rgba(45, 109, 166, 0.45);
        border-radius: 16px;
        padding: 24px 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        background: linear-gradient(90deg, #A0BED9, #2D6DA6, #3B6D8C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 6px;
        line-height: 1.2;
    }

    .hero-subtitle {
        color: rgba(160, 190, 217, 0.9);
        font-size: 1.05rem;
        font-weight: 400;
        line-height: 1.5;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: linear-gradient(145deg, #1A2B3C 0%, #0D1B2A 100%);
        border: 1px solid rgba(45, 109, 166, 0.35);
        border-radius: 14px;
        padding: 18px 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #003F71, #2D6DA6, #A0BED9);
        border-radius: 14px 14px 0 0;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
        border-color: rgba(45, 109, 166, 0.6);
        box-shadow: 0 10px 25px rgba(0, 63, 113, 0.35);
    }

    .kpi-icon {
        font-size: 1.6rem;
        margin-bottom: 8px;
        display: inline-block;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #F2F2F2;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }

    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #A0BED9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }

    .kpi-sub {
        font-size: 0.78rem;
        color: #3B6D8C;
        margin-top: 4px;
    }

    /* ── Content Cards ── */
    .detail-card {
        background: #1A2B3C;
        border: 1px solid rgba(45, 109, 166, 0.25);
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 14px;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }

    .detail-card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #F2F2F2;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .detail-card-content {
        font-size: 0.9rem;
        color: #A0BED9;
        line-height: 1.55;
    }

    .card-target   { border-left: 4px solid #2D6DA6; }
    .card-positive { border-left: 4px solid #3B6D8C; }
    .card-warning  { border-left: 4px solid #8C1414; }
    .card-feedback { border-left: 4px solid #A0BED9; }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .badge-primary { background: rgba(0, 63, 113, 0.4);  color: #A0BED9; border: 1px solid rgba(45, 109, 166, 0.5); }
    .badge-purple  { background: rgba(59, 109, 140, 0.3); color: #A0BED9; border: 1px solid rgba(59, 109, 140, 0.4); }
    .badge-teal    { background: rgba(45, 109, 166, 0.25);color: #A0BED9; border: 1px solid rgba(45, 109, 166, 0.4); }
    .badge-amber   { background: rgba(140, 20, 20, 0.25); color: #F2F2F2; border: 1px solid rgba(140, 20, 20, 0.4); }

    /* ── Action Button ── */
    .btn-access {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #003F71 0%, #2D6DA6 100%);
        color: #F2F2F2 !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 10px 22px;
        border-radius: 10px;
        text-decoration: none !important;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(0, 63, 113, 0.45);
        margin-top: 12px;
    }

    .btn-access:hover {
        background: linear-gradient(135deg, #2D6DA6 0%, #3B6D8C 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(45, 109, 166, 0.55);
    }

    /* ── Streamlit widget overrides ── */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #003F71 !important;
        color: #F2F2F2 !important;
        border: 1px solid rgba(45,109,166,0.5) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #003F71, #2D6DA6);
        color: #F2F2F2;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2D6DA6, #3B6D8C);
        transform: translateY(-1px);
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1A2B3C;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 7px;
        color: #A0BED9;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003F71 !important;
        color: #F2F2F2 !important;
    }
    /* Alert / info box */
    .stAlert {
        background-color: rgba(0, 63, 113, 0.2);
        border-left: 4px solid #2D6DA6;
        color: #F2F2F2;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# CARREGAMENTO E PROCESSAMENTO DOS DADOS
# ==============================================================================
@st.cache_data
def carregar_dados():
    # Prioridade: base consolidada final (gerada pelo script consolidar.py),
    # depois o arquivo original como fallback.
    possiveis_caminhos_base = [
        "base_consolidada_final.xlsx",
        "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx",
        r"C:\Users\visitante\Desktop\Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx",
        r"C:\Users\visitante\Desktop\campanha\Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx"
    ]

    arquivo_encontrado = None
    for caminho in possiveis_caminhos_base:
        if os.path.exists(caminho):
            arquivo_encontrado = caminho
            break

    if not arquivo_encontrado:
        raise FileNotFoundError(
            "Arquivo de dados não encontrado. Execute 'consolidar.py' para gerar 'base_consolidada_final.xlsx'."
        )

    # Leitura da aba Consolidado
    df_consolidado = pd.read_excel(arquivo_encontrado, sheet_name="Consolidado")

    # Garantir que a coluna 'Ano de Lançamento' exista (criada pelo consolidar.py).
    # Se a base vier do arquivo original (sem o campo), cria a partir de 'Data de lançamento'.
    if 'Ano de Lançamento' not in df_consolidado.columns and 'Ano de Lancamento' not in df_consolidado.columns:
        if 'Data de lançamento' in df_consolidado.columns:
            def _extrair_ano(valor):
                if pd.isna(valor) or str(valor).strip() == '':
                    return 'Não informado'
                match = re.search(r'\b(202\d)\b', str(valor))
                return match.group(1) if match else 'Não informado'
            df_consolidado['Ano de Lançamento'] = df_consolidado['Data de lançamento'].apply(_extrair_ano)
        else:
            df_consolidado['Ano de Lançamento'] = 'Não informado'
            df_consolidado['Data de lançamento'] = 'Não informado'
    else:
        # Normalizar nome da coluna caso venha sem acento do consolidar.py antigo
        if 'Ano de Lancamento' in df_consolidado.columns and 'Ano de Lançamento' not in df_consolidado.columns:
            df_consolidado.rename(columns={'Ano de Lancamento': 'Ano de Lançamento'}, inplace=True)
        if 'Data de lançamento' not in df_consolidado.columns:
            df_consolidado['Data de lançamento'] = 'Não informado'

    # Tratamento de strings e valores nulos
    colunas_texto = df_consolidado.select_dtypes(include=['object']).columns
    df_consolidado[colunas_texto] = df_consolidado[colunas_texto].fillna("Não informado")

    # Normalizar 'Não informado' na coluna Ano de Lançamento (pode vir como 'Nao informado' do script)
    df_consolidado['Ano de Lançamento'] = df_consolidado['Ano de Lançamento'].replace(
        {'Nao informado': 'Não informado', 'nan': 'Não informado', '': 'Não informado'}
    )

    # Limpeza de URLs (removendo tags < e > se presentes)
    if 'Link ou referência de acesso' in df_consolidado.columns:
        df_consolidado['Link_Limpo'] = df_consolidado['Link ou referência de acesso'].astype(str).apply(
            lambda x: re.sub(r'[<>]', '', x).strip()
        )
    else:
        df_consolidado['Link_Limpo'] = "Não informado"

    # Categoria Macrotipo simplificada para filtros rápidos
    def agrupar_tipo(tipo_str):
        tipo_lower = str(tipo_str).lower()
        if "mba" in tipo_lower:
            return "MBA Executivo / Lato Sensu"
        elif "pós" in tipo_lower or "especialização" in tipo_lower or "lato sensu" in tipo_lower:
            return "Pós-Graduação & Especialização"
        elif "bacharelado" in tipo_lower or "graduação" in tipo_lower or "tecnólogo" in tipo_lower:
            return "Graduação & Tecnólogo"
        elif "short" in tipo_lower or "curto" in tipo_lower or "curso aberto" in tipo_lower or "gratuita" in tipo_lower:
            return "Cursos Curtos, Livres & Gratuitos"
        elif "certificate" in tipo_lower or "certificação" in tipo_lower or "micromasters" in tipo_lower:
            return "Certificações & MicroMasters"
        elif "mestrado" in tipo_lower or "stricto" in tipo_lower:
            return "Mestrado & Stricto Sensu"
        else:
            return "Outros Programas"

    df_consolidado['Macro_Tipo'] = df_consolidado['Tipo'].apply(agrupar_tipo)

    # Identificação de tecnologias e tópicos-chave para tags e busca
    topicos_keywords = {
        "GenAI / LLMs": ["llm", "genai", "generative ai", "ia generativa", "gpt", "chatgpt", "prompt", "openai", "claude", "gemini"],
        "RAG & Agentes": ["rag", "agente", "agents", "langchain", "crewai", "autogen", "retrieval", "vector"],
        "Visão Computacional": ["visão computacional", "computer vision", "opencv", "yolo", "detecção de objetos"],
        "NLP & Processamento de Linguagem": ["nlp", "pln", "processamento de linguagem", "transformers", "bert", "huggingface"],
        "MLOps & Engenharia de Dados": ["mlops", "engenharia de dados", "deploy", "pipeline", "ci/cd", "kubernetes", "docker", "airflow"],
        "Deep Learning & PyTorch/TF": ["deep learning", "redes neurais", "pytorch", "tensorflow", "keras"],
        "Estatística & Big Data": ["estatística", "big data", "spark", "hadoop", "sql", "regressão", "probabilidade"],
        "Governança, Ética & Direito em IA": ["ética", "governança", "lgpd", "responsável", "regulamentação", "compliance", "segurança"]
    }

    def extrair_tags(row):
        texto_completo = f"{row.get('Nome do curso, guia ou programa', '')} {row.get('Principais conteúdos', '')} {row.get('Estrutura de módulos', '')}".lower()
        tags_encontradas = []
        for tag, kw_list in topicos_keywords.items():
            if any(kw in texto_completo for kw in kw_list):
                tags_encontradas.append(tag)
        return tags_encontradas if tags_encontradas else ["IA / ML Geral"]

    df_consolidado['Tags_Tematicas'] = df_consolidado.apply(extrair_tags, axis=1)

    # Carregar também o Resumo por Lote se disponível
    try:
        df_resumo = pd.read_excel(arquivo_encontrado, sheet_name="Resumo por Lote")
    except Exception:
        df_resumo = pd.DataFrame()

    return df_consolidado, df_resumo

# Tentativa de carregamento
try:
    df, df_resumo = carregar_dados()
except Exception as e:
    st.error(f"⚠️ Erro ao carregar a base de dados: {e}")
    st.info("Por favor, verifique se o arquivo 'Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx' está acessível.")
    st.stop()


# ==============================================================================
# SIDEBAR (FILTROS DE ALTA PERFORMANCE)
# ==============================================================================
# Logo CIIA no topo da sidebar
import os as _os
_logo_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "assets", "img", "logo_ciia.png")
if _os.path.exists(_logo_path):
    st.sidebar.image(_logo_path, width=160)
st.sidebar.markdown("---")
st.sidebar.markdown("## 🔍 Filtros & Busca Avançada")
st.sidebar.caption("Refine o mapeamento por temas, lotes, tipos e instituições.")

# Busca textual geral
busca_texto = st.sidebar.text_input(
    "🔎 Busca por palavra-chave ou termo:",
    placeholder="Ex: RAG, LangChain, USP, DeepLearning, Stanford, Pós...",
    help="Pesquisa no título do curso, instituição, público-alvo, ementa e conteúdos."
)

# Filtro Rápido por Macro Categoria
macro_tipos = sorted(df['Macro_Tipo'].unique())
macro_selecionados = st.sidebar.multiselect(
    "📚 Categoria Geral",
    options=macro_tipos,
    default=macro_tipos,
    help="Categorização agrupada de formações"
)

# Filtro por Tópicos Tecnológicos
todos_topicos = sorted(list({tag for tags in df['Tags_Tematicas'] for tag in tags}))
topicos_selecionados = st.sidebar.multiselect(
    "🏷️ Tópicos & Tecnologias-Chave",
    options=todos_topicos,
    default=[],
    help="Filtre por tecnologias específicas como LLMs, RAG, MLOps, Visão Computacional, etc."
)

# Filtro por Ano de Lançamento
anos_disponiveis = sorted(
    [a for a in df['Ano de Lançamento'].astype(str).unique() if a not in ('nan', '')],
    key=lambda x: (x == 'Não informado', x)
)
anos_selecionados = st.sidebar.multiselect(
    "📅 Ano de Lançamento",
    options=anos_disponiveis,
    default=anos_disponiveis,
    help="Filtre por ano de lançamento/publicação do curso (2022–2026 ou Não informado)"
)

# Filtro por Lote
lotes_disponiveis = sorted(df['Lote'].astype(str).unique(), key=lambda x: (x.startswith("Lote"), x))
lotes_selecionados = st.sidebar.multiselect(
    "📦 Lote de Mapeamento",
    options=lotes_disponiveis,
    default=lotes_disponiveis,
    help="Filtre pelos lotes de pesquisa originais e expansões"
)

# Filtro por Tipo Original
tipos_disponiveis = sorted(df['Tipo'].astype(str).unique())
tipos_selecionados = st.sidebar.multiselect(
    "🎓 Tipo Específico de Formação",
    options=tipos_disponiveis,
    default=tipos_disponiveis
)

# Filtro por Instituição
instituicoes_disponiveis = sorted(df['Instituição responsável'].astype(str).unique())
instituicoes_selecionadas = st.sidebar.multiselect(
    "🏛️ Instituição Responsável",
    options=instituicoes_disponiveis,
    default=[]
)

# Botão para resetar filtros
if st.sidebar.button("🔄 Redefinir Todos os Filtros", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total de Cursos Cadastrados:** `{len(df)}`")
st.sidebar.markdown(f"**Instituições Únicas:** `{df['Instituição responsável'].nunique()}`")
st.sidebar.caption("🚀 Dashboard desenvolvido com Streamlit & Plotly.")


# ==============================================================================
# APLICAÇÃO DOS FILTROS
# ==============================================================================
df_filtrado = df[
    (df['Lote'].isin(lotes_selecionados)) &
    (df['Tipo'].isin(tipos_selecionados)) &
    (df['Macro_Tipo'].isin(macro_selecionados)) &
    (df['Ano de Lançamento'].astype(str).isin(anos_selecionados))
]

if instituicoes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['Instituição responsável'].isin(instituicoes_selecionadas)]

if topicos_selecionados:
    df_filtrado = df_filtrado[
        df_filtrado['Tags_Tematicas'].apply(lambda tags: any(t in tags for t in topicos_selecionados))
    ]

if busca_texto:
    termo = busca_texto.lower()
    df_filtrado = df_filtrado[
        df_filtrado['Nome do curso, guia ou programa'].str.lower().str.contains(termo, na=False) |
        df_filtrado['Principais conteúdos'].str.lower().str.contains(termo, na=False) |
        df_filtrado['Instituição responsável'].str.lower().str.contains(termo, na=False) |
        df_filtrado['Público-alvo'].str.lower().str.contains(termo, na=False) |
        df_filtrado['Estrutura de módulos'].str.lower().str.contains(termo, na=False) |
        df_filtrado['Pontos positivos'].str.lower().str.contains(termo, na=False)
    ]


# ==============================================================================
# CABEÇALHO HERO & CARDS DE INDICADORES (KPIS)
# ==============================================================================
_logo_hero_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img", "logo_ciia.png")
_hero_col_logo, _hero_col_text = st.columns([1, 4])
with _hero_col_logo:
    if os.path.exists(_logo_hero_path):
        st.image(_logo_hero_path, width=180)
with _hero_col_text:
    st.markdown("""
    <div class="hero-container" style="margin-bottom:0;">
        <div class="hero-title">📊 Panorama Nacional &amp; Internacional de Capacitação em IA &amp; ML</div>
        <div class="hero-subtitle">
            Mapeamento analítico e detalhado de graduações, pós-graduações, MBAs, certificações oficiais e cursos executivos de ponta em Inteligência Artificial, Machine Learning e Ciência de Dados.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Grid de KPIs Modernos
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_banco = len(df)
total_filtro = len(df_filtrado)
pct_filtro = (total_filtro / total_banco * 100) if total_banco > 0 else 0

with kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎯</div>
        <div class="kpi-value">{total_filtro}</div>
        <div class="kpi-label">Cursos Filtrados</div>
        <div class="kpi-sub">{pct_filtro:.1f}% do total mapeado</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    inst_count = df_filtrado['Instituição responsável'].nunique()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🏛️</div>
        <div class="kpi-value">{inst_count}</div>
        <div class="kpi-label">Instituições</div>
        <div class="kpi-sub">Universidades & Empresas</div>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    tipos_count = df_filtrado['Macro_Tipo'].nunique()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">🎓</div>
        <div class="kpi-value">{tipos_count}</div>
        <div class="kpi-label">Categorias</div>
        <div class="kpi-sub">Formatos de ensino</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    lotes_count = df_filtrado['Lote'].nunique()
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-value">{lotes_count}</div>
        <div class="kpi-label">Lotes Ativos</div>
        <div class="kpi-sub">De {df['Lote'].nunique()} lotes no banco</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    gratuitos_count = df_filtrado[df_filtrado['Pontos positivos'].str.lower().str.contains('gratuit|free|sem custo', na=False)].shape[0]
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">💡</div>
        <div class="kpi-value">{gratuitos_count}</div>
        <div class="kpi-label">Cursos Free / Abertos</div>
        <div class="kpi-sub">Destaque de acessibilidade</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# ABAS DE NAVEGAÇÃO PRINCIPAIS
# ==============================================================================
tab_graficos, tab_detalhes, tab_comparador, tab_tabela, tab_metodologia = st.tabs([
    "📈 Análise Visual & Estatísticas",
    "🔎 Ficha Técnica do Curso",
    "⚖️ Comparador Lado a Lado",
    "📋 Base Completa & Exportação",
    "ℹ️ Metodologia & Lotes"
])


# ------------------------------------------------------------------------------
# ABA 1: ANÁLISE VISUAL & GRÁFICOS
# ------------------------------------------------------------------------------
with tab_graficos:
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados. Ajuste as opções na barra lateral.")
    else:
        g_col1, g_col2 = st.columns([1.2, 1])
        
        with g_col1:
            st.markdown("#### 🏛️ Top 12 Instituições com Maior Oferta de Cursos")
            top_inst = df_filtrado['Instituição responsável'].value_counts().head(12).reset_index()
            top_inst.columns = ['Instituição', 'Quantidade']
            
            fig_inst = px.bar(
                top_inst,
                x='Quantidade',
                y='Instituição',
                orientation='h',
                color='Quantidade',
                color_continuous_scale='Blues',
                text='Quantidade'
            )
            fig_inst.update_traces(
                textposition='outside',
                marker_line_color='rgba(255,255,255,0.2)',
                marker_line_width=1
            )
            fig_inst.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#F8FAFC'},
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
                yaxis_title="",
                xaxis_title="Número de Cursos Oferecidos",
                margin=dict(l=10, r=30, t=10, b=20),
                height=420,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_inst, use_container_width=True)

        with g_col2:
            st.markdown("#### 🎓 Distribuição por Categoria Geral de Formação")
            macro_counts = df_filtrado['Macro_Tipo'].value_counts().reset_index()
            macro_counts.columns = ['Categoria', 'Quantidade']
            
            fig_macro = px.pie(
                macro_counts,
                names='Categoria',
                values='Quantidade',
                hole=0.48,
                color_discrete_sequence=px.colors.qualitative.Prism
            )
            fig_macro.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#0F172A', width=2))
            )
            fig_macro.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#F8FAFC'},
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=420
            )
            st.plotly_chart(fig_macro, use_container_width=True)

        st.markdown("---")
        
        c_row2_1, c_row2_2 = st.columns(2)
        
        with c_row2_1:
            st.markdown("#### 🏷️ Frequência de Tópicos & Tecnologias em Alta")
            
            # Contagem de tags
            all_tags_filtered = [tag for sublist in df_filtrado['Tags_Tematicas'] for tag in sublist]
            tags_series = pd.Series(all_tags_filtered).value_counts().reset_index()
            tags_series.columns = ['Tópico', 'Ocorrências']
            
            fig_tags = px.bar(
                tags_series,
                x='Ocorrências',
                y='Tópico',
                orientation='h',
                color='Ocorrências',
                color_continuous_scale='Purples',
                text='Ocorrências'
            )
            fig_tags.update_traces(textposition='outside')
            fig_tags.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#F8FAFC'},
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
                yaxis_title="",
                xaxis_title="Cursos que Cobrem o Tópico",
                margin=dict(l=10, r=30, t=10, b=20),
                height=360,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_tags, use_container_width=True)

        with c_row2_2:
            st.markdown("#### 📦 Volume de Cursos Mapeados por Lote")
            lotes_count = df_filtrado['Lote'].value_counts().reset_index()
            lotes_count.columns = ['Lote', 'Quantidade']
            
            fig_lotes = px.bar(
                lotes_count,
                x='Lote',
                y='Quantidade',
                color='Quantidade',
                color_continuous_scale='Teal',
                text='Quantidade'
            )
            fig_lotes.update_traces(textposition='outside')
            fig_lotes.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#F8FAFC'},
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
                xaxis_title="",
                yaxis_title="Total de Cursos",
                margin=dict(l=10, r=10, t=10, b=20),
                height=360,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_lotes, use_container_width=True)

        st.markdown("---")

        # ── Gráfico: Distribuição de Cursos por Ano de Lançamento ──────────────
        st.markdown("#### 📅 Distribuição de Cursos por Ano de Lançamento")
        anos_count = (
            df_filtrado['Ano de Lançamento']
            .astype(str)
            .value_counts()
            .reset_index()
        )
        anos_count.columns = ['Ano', 'Quantidade']
        # Ordenar: anos numéricos primeiro, depois 'Não informado'
        anos_count['_sort'] = anos_count['Ano'].apply(
            lambda x: int(x) if x.isdigit() else 9999
        )
        anos_count = anos_count.sort_values('_sort').drop(columns='_sort')

        fig_anos = px.bar(
            anos_count,
            x='Ano',
            y='Quantidade',
            color='Quantidade',
            color_continuous_scale='Viridis',
            text='Quantidade',
            labels={'Ano': 'Ano de Lançamento', 'Quantidade': 'Nº de Cursos'}
        )
        fig_anos.update_traces(
            textposition='outside',
            marker_line_color='rgba(255,255,255,0.2)',
            marker_line_width=1
        )
        fig_anos.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#F8FAFC'},
            xaxis=dict(type='category', showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.08)'),
            xaxis_title="Ano de Lançamento",
            yaxis_title="Número de Cursos",
            margin=dict(l=10, r=20, t=10, b=20),
            height=340,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_anos, use_container_width=True)


# ------------------------------------------------------------------------------
# ABA 2: FICHA TÉCNICA DO CURSO (DETALHES COMPLETOS)
# ------------------------------------------------------------------------------
with tab_detalhes:
    st.markdown("### 🔎 Ficha Técnica e Ementa Estruturada do Curso")
    
    if df_filtrado.empty:
        st.warning("⚠️ Nenhum curso encontrado com os filtros atuais.")
    else:
        col_sel1, col_sel2 = st.columns([3, 1])
        with col_sel1:
            lista_cursos = df_filtrado['Nome do curso, guia ou programa'].tolist()
            curso_escolhido = st.selectbox(
                "Selecione um curso para visualizar todos os detalhes:",
                options=lista_cursos,
                index=0
            )
        with col_sel2:
            st.metric("Total Disponível no Filtro", f"{len(lista_cursos)} opções")
        
        # Recupera registro do curso selecionado
        detalhe = df_filtrado[df_filtrado['Nome do curso, guia ou programa'] == curso_escolhido].iloc[0]
        
        # Header do Curso com Badges
        tags_html = "".join([f'<span class="badge badge-purple">{tag}</span>' for tag in detalhe['Tags_Tematicas']])
        
        _data_lancamento = detalhe.get('Data de lançamento', 'Não informado')
        _ano_lancamento  = detalhe.get('Ano de Lançamento', 'Não informado')
        _data_badge = (
            f'<span class="badge badge-amber">📅 Lançamento: {_data_lancamento}</span>'
            if str(_data_lancamento) not in ('Não informado', 'nan', '')
            else f'<span class="badge badge-amber">📅 Ano: {_ano_lancamento}</span>'
        )

        st.markdown(f"""
        <div style="background: #1E293B; border-radius: 14px; padding: 22px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.1);">
            <div style="font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin-bottom: 8px;">
                {detalhe['Nome do curso, guia ou programa']}
            </div>
            <div style="margin-bottom: 12px;">
                <span class="badge badge-primary">🏛️ {detalhe['Instituição responsável']}</span>
                <span class="badge badge-teal">🎓 {detalhe['Tipo']}</span>
                <span class="badge badge-amber">⏱️ Carga: {detalhe['Carga horária']}</span>
                <span class="badge badge-primary">📦 {detalhe['Lote']}</span>
                {_data_badge}
            </div>
            <div>
                {tags_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid 2x2 com cards de informação chave
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            st.markdown(f"""
            <div class="detail-card card-target">
                <div class="detail-card-title" style="color: #38BDF8;">
                    🎯 Público-Alvo e Perfil
                </div>
                <div class="detail-card-content">
                    {detalhe['Público-alvo']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="detail-card card-positive">
                <div class="detail-card-title" style="color: #34D399;">
                    💡 Pontos Positivos & Diferenciais
                </div>
                <div class="detail-card-content">
                    {detalhe['Pontos positivos']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown(f"""
            <div class="detail-card card-warning">
                <div class="detail-card-title" style="color: #FBBF24;">
                    ⚠️ Pré-requisitos, Desafios & Limitações
                </div>
                <div class="detail-card-content">
                    {detalhe['Limitações']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            feedback_val = detalhe.get('Satisfação / Feedback', 'Não informado')
            st.markdown(f"""
            <div class="detail-card card-feedback">
                <div class="detail-card-title" style="color: #A78BFA;">
                    ⭐ Satisfação, Avaliação & Reputação
                </div>
                <div class="detail-card-content">
                    {feedback_val}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Seções de Conteúdo e Ementa
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📚 **Estrutura Completa de Módulos & Ementa**", expanded=True):
            st.markdown(f"**Conteúdos Principais:**\n\n{detalhe['Principais conteúdos']}")
            st.markdown("---")
            st.markdown(f"**Estrutura de Módulos:**\n\n{detalhe['Estrutura de módulos']}")

        with st.expander("🎓 **Metodologia Pedagógica & Cronograma**", expanded=False):
            st.markdown(f"**Estratégia Pedagógica:**\n\n{detalhe['Estratégia pedagógica']}")
            cronograma_val = detalhe.get('Cronograma / Início / Fim', 'Não informado')
            st.markdown(f"**Cronograma / Período:**\n\n{cronograma_val}")
            
        # Link Oficial de Acesso
        link_acesso = detalhe.get('Link_Limpo', '')
        if link_acesso and link_acesso != "Não informado" and link_acesso.startswith("http"):
            st.markdown(f"""
            <div style="margin-top: 15px; text-align: center;">
                <a href="{link_acesso}" target="_blank" class="btn-access">
                    🔗 Acessar Página Oficial do Curso ↗
                </a>
            </div>
            """, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# ABA 3: COMPARADOR LADO A LADO
# ------------------------------------------------------------------------------
with tab_comparador:
    st.markdown("### ⚖️ Comparador Direto de Cursos")
    st.caption("Compare 2 ou 3 cursos lado a lado para avaliar instituições, carga horária, vantagens e pontos de atenção.")
    
    opcoes_cursos = df['Nome do curso, guia ou programa'].unique().tolist()
    
    cursos_comparar = st.multiselect(
        "Selecione de 2 a 3 cursos para comparar:",
        options=opcoes_cursos,
        default=opcoes_cursos[:2] if len(opcoes_cursos) >= 2 else opcoes_cursos,
        max_selections=3
    )
    
    if len(cursos_comparar) < 2:
        st.info("💡 Selecione pelo menos 2 cursos para exibir a tabela comparativa.")
    else:
        df_comp = df[df['Nome do curso, guia ou programa'].isin(cursos_comparar)].drop_duplicates(subset=['Nome do curso, guia ou programa']).copy()
        df_comp = df_comp.set_index('Nome do curso, guia ou programa').loc[cursos_comparar].reset_index()

        cols_comp = st.columns(len(cursos_comparar))
        
        for idx, (_, row) in enumerate(df_comp.iterrows()):
            with cols_comp[idx]:
                st.markdown(f"""
                <div class="detail-card" style="border-top: 4px solid #3B82F6;">
                    <h3 style="font-size: 1.15rem; color: #60A5FA; margin-bottom: 6px;">{row['Nome do curso, guia ou programa']}</h3>
                    <p style="color: #94A3B8; font-size: 0.88rem; margin-bottom: 12px;"><strong>🏛️ Instituição:</strong> {row['Instituição responsável']}</p>
                    <p><strong>🎓 Tipo:</strong> {row['Tipo']}</p>
                    <p><strong>⏱️ Carga Horária:</strong> {row['Carga horária']}</p>
                    <hr style="border-color: rgba(255,255,255,0.1);">
                    <p><strong style="color: #38BDF8;">🎯 Público:</strong><br>{row['Público-alvo']}</p>
                    <p><strong style="color: #34D399;">💡 Pontos Fortes:</strong><br>{row['Pontos positivos']}</p>
                    <p><strong style="color: #FBBF24;">⚠️ Limitações:</strong><br>{row['Limitações']}</p>
                    <p><strong style="color: #A78BFA;">⭐ Satisfação:</strong><br>{row.get('Satisfação / Feedback', 'Não informado')}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if row.get('Link_Limpo', '') != "Não informado" and str(row.get('Link_Limpo', '')).startswith("http"):
                    st.markdown(f"[🔗 Acessar Link]({row['Link_Limpo']})")


# ------------------------------------------------------------------------------
# ABA 4: TABELA COMPLETA & EXPORTAÇÃO
# ------------------------------------------------------------------------------
with tab_tabela:
    st.markdown("### 📋 Base de Dados Consolidada")
    st.caption("Filtre, explore e exporte os dados para análises externas.")
    
    col_exp1, col_exp2, col_exp3 = st.columns([2, 1, 1])
    
    with col_exp1:
        st.markdown(f"**Registros exibidos:** `{len(df_filtrado)}` de `{len(df)}` cursos cadastrados.")
        
    with col_exp2:
        # Download CSV
        csv_data = df_filtrado.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Baixar Dados (CSV)",
            data=csv_data,
            file_name="mapeamento_capacitacao_ia_filtrado.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    with col_exp3:
        # Download Excel
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, sheet_name='Cursos_Filtrados', index=False)
        excel_data = excel_buffer.getvalue()
        
        st.download_button(
            label="📥 Baixar Dados (Excel .xlsx)",
            data=excel_data,
            file_name="mapeamento_capacitacao_ia_filtrado.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Configuração de visualização da tabela
    _colunas_base = [
        'Nome do curso, guia ou programa',
        'Instituição responsável',
        'Ano de Lançamento',
        'Data de lançamento',
        'Macro_Tipo',
        'Tipo',
        'Carga horária',
        'Lote',
        'Público-alvo',
        'Pontos positivos',
        'Limitações',
        'Link_Limpo'
    ]
    # Incluir apenas colunas que existam no dataframe
    colunas_exibicao = [c for c in _colunas_base if c in df_filtrado.columns]

    st.dataframe(
        df_filtrado[colunas_exibicao],
        column_config={
            "Nome do curso, guia ou programa": st.column_config.TextColumn("Nome do Curso", width="large"),
            "Instituição responsável": st.column_config.TextColumn("Instituição", width="medium"),
            "Ano de Lançamento": st.column_config.TextColumn("Ano", width="small"),
            "Data de lançamento": st.column_config.TextColumn("Data de Lançamento", width="medium"),
            "Macro_Tipo": st.column_config.TextColumn("Categoria Geral", width="medium"),
            "Tipo": st.column_config.TextColumn("Tipo Específico", width="medium"),
            "Carga horária": st.column_config.TextColumn("Carga Horária", width="small"),
            "Lote": st.column_config.TextColumn("Lote", width="small"),
            "Link_Limpo": st.column_config.LinkColumn("Link Oficial", display_text="Acessar")
        },
        use_container_width=True,
        hide_index=True,
        height=520
    )


# ------------------------------------------------------------------------------
# ABA 5: METODOLOGIA & LOTES
# ------------------------------------------------------------------------------
with tab_metodologia:
    st.markdown("### ℹ️ Metodologia & Estrutura de Lotes Mapeados")
    st.markdown("""
    Este painel consolida uma pesquisa aprofundada sobre cursos e programas de formação em **Inteligência Artificial, Machine Learning, Deep Learning, Engenharia de Prompt e Ciência de Dados** no Brasil e no mundo.
    """)
    
    if not df_resumo.empty:
        st.markdown("#### 📑 Resumo por Lote de Mapeamento")
        st.dataframe(df_resumo.dropna(how='all'), use_container_width=True, hide_index=True)
    
    st.markdown("""
    #### 📌 Critérios e Dimensões Coletadas:
    1. **Identificação**: Nome oficial do curso, instituição promotora e lote de pesquisa.
    2. **Classificação**: Modalidade, nível acadêmico (graduação, especialização, MBA, extensão, short course).
    3. **Ementa e Conteúdo**: Estrutura modular, tecnologias ensinadas (Python, PyTorch, LangChain, RAG, etc.).
    4. **Metodologia**: Abordagem prática, projetos aplicados (capstone), avaliações e suporte.
    5. **Diferenciais & Limitações**: Análise crítica de vantagens competitivas e pré-requisitos exigidos.
    6. **Links & Acesso**: URLs verificadas para consulta e inscrição direta.
    """)

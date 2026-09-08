# 📊 Painel de Capacitação em IA, ML & Ciência de Dados

Dashboard analítico e interativo desenvolvido em **Python, Streamlit e Plotly** para visualização, exploração e comparação de cursos e formações de ponta em Inteligência Artificial no Brasil e no mundo.

---

## 🚀 Como Executar

### 1. Inicialização Rápida (Windows)
Dê um duplo clique no arquivo:
```bat
run_dashboard.bat
```

### 2. Ou via Linha de Comando (Terminal)
```bash
python -m streamlit run app.py
```
O dashboard abrirá automaticamente no seu navegador no endereço:
👉 **`http://localhost:8501`**

---

## 🛠️ Principais Recursos e Funcionalidades

1. **Indicadores Executivos (KPI Cards):**
   - Total de cursos filtrados e representatividade no banco (193 formações mapeadas).
   - Contagem de instituições únicas e diversidade de formatos.
   - Destaque de cursos gratuitos / comunitários.

2. **Filtros e Busca em Tempo Real:**
   - Busca textual geral em títulos, ementas, públicos-alvo e instituições.
   - Filtro por Categoria Geral (Pós/MBA, Graduação, Cursos Curtos, Certificações).
   - Filtro por Tópicos Tecnológicos (GenAI, RAG & Agentes, Visão Computacional, NLP, MLOps, Deep Learning, Governança/Ética).
   - Filtro por Lote de Mapeamento e Instituições Responsáveis.

3. **Abas de Navegação:**
   - **📈 Análise Visual & Estatísticas:** Gráficos interativos em Plotly (Top Instituições, Donut por Tipo de Formação, Volume por Lote, Frequência de Tecnologias).
   - **🔎 Ficha Técnica do Curso:** Card visual estruturado com Público-Alvo, Pontos Positivos, Limitações, Avaliação de Mercado, Ementa Modular e Link Oficial direto.
   - **⚖️ Comparador Lado a Lado:** Selecione 2 ou 3 cursos para comparação direta de pontos fortes, carga horária e objetivos.
   - **📋 Base Completa & Exportação:** Tabela interativa com pesquisa e botões de download em **CSV** e **Excel (.xlsx)**.
   - **ℹ️ Metodologia & Lotes:** Resumo estruturado do processo de pesquisa e lotes consolidados.

---

## 📦 Estrutura dos Arquivos

```
antigravity/
├── app.py                                                               # Aplicação principal Streamlit
├── Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx    # Base de dados consolidada
├── run_dashboard.bat                                                   # Launcher automático Windows
├── requirements.txt                                                    # Dependências do projeto
├── .streamlit/
│   └── config.toml                                                     # Configurações de tema escuro e UI
└── README.md                                                           # Documentação
```

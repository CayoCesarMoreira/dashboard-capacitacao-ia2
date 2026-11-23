# 📊 Dashboard de Capacitação em IA, ML & Ciência de Dados

**NIAUnDF / CIIA** — Painel analítico e interativo desenvolvido em **Python, Streamlit e Plotly** para mapear, explorar e comparar cursos e programas de formação em Inteligência Artificial, Machine Learning e Ciência de Dados no Brasil e no exterior (recorte 2022–2026).

---

## 🔭 Visão geral

- **Base atual:** 664 cursos únicos de 504 instituições, organizados em 77 lotes de mapeamento.
- **Origem dos dados:** união das planilhas em `dados/fontes/`:
  - `Mapeamento_..._Consolidado.xlsx` — 293 cursos (lotes originais);
  - `Mapeamento_..._2022_2026.xlsx` — 490 cursos com a coluna **Data de lançamento**.
  
  Duplicatas (mesmo curso + instituição) são removidas, priorizando o registro que tem data de lançamento.
- **Recursos do painel:**
  - **KPIs:** cursos filtrados, instituições, categorias, lotes ativos e cursos gratuitos/abertos.
  - **Filtros:** busca textual, categoria geral, tópicos (GenAI/LLMs, RAG & Agentes, NLP, Visão Computacional, MLOps, Deep Learning, Governança/Ética…), ano de lançamento, lote, tipo de formação e instituição.
  - **Abas:**
    - 📈 Análise Visual;
    - 🔎 Ficha Técnica do Curso;
    - ⚖️ Comparador Lado a Lado;
    - 📋 Base Completa com exportação em CSV/Excel;
    - ℹ️ Metodologia & Resumo por Lote.

---

## 📦 Estrutura do projeto

```
dashboard-capacitacao-ia2/
├── app.py                         # Aplicação principal Streamlit (lê base_consolidada_final.xlsx)
├── consolidar.py                  # Une as planilhas-fonte e gera base_consolidada_final.xlsx
├── base_consolidada_final.xlsx    # Base usada pelo dashboard (abas: Consolidado, Resumo por Lote)
├── dados/
│   └── fontes/                    # Planilhas originais do mapeamento (entrada do consolidar.py)
│       ├── Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx
│       └── Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_2022_2026.xlsx
├── assets/img/logo_ciia.png       # Logo CIIA
├── requirements.txt               # Dependências Python
├── iniciar.bat                    # Windows: instala dependências, consolida e abre o painel
├── run_dashboard.bat              # Windows: apenas abre o painel
├── .streamlit/config.toml         # Tema e configurações do servidor Streamlit
├── .devcontainer/                 # Ambiente para GitHub Codespaces / Dev Containers
└── README.md
```

---

## 🚀 Execução local

**Pré-requisitos:** Python 3.10 ou superior e Git.

### 1) Clonar o repositório
```bash
git clone https://github.com/CayoCesarMoreira/dashboard-capacitacao-ia2.git
cd dashboard-capacitacao-ia2
```

### 2) Criar/ativar ambiente virtual (opcional) e instalar dependências
```bash
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3) Executar o dashboard
```bash
streamlit run app.py
```
O painel abre em **http://localhost:8501**.

> 💡 **Windows:** basta dar duplo clique em `iniciar.bat`, que faz os três passos automaticamente (instala as dependências, consolida as planilhas e abre o painel).

---

## 🔄 Atualizar a base de dados

1. Substitua ou adicione a nova versão da planilha em `dados/fontes/`, mantendo o mesmo nome de arquivo e a aba `Consolidado`.
2. Gere novamente a base consolidada:
   ```bash
   python consolidar.py
   ```
3. Reinicie o Streamlit ou use **Clear cache** no menu do app.

Colunas esperadas na aba `Consolidado`:
- Lote
- Tipo
- Nome do curso, guia ou programa
- Instituição responsável
- Público-alvo
- Carga horária
- Estrutura de módulos
- Principais conteúdos
- Estratégia pedagógica
- Pontos positivos
- Limitações
- Link ou referência de acesso
- Cronograma / Início / Fim
- Satisfação / Feedback
- Data de lançamento (opcional)

---

## 🔐 Segurança

O projeto não usa chaves de API. Se no futuro for necessário algum segredo, use `.streamlit/secrets.toml` ou `.env`. Esses arquivos já estão no `.gitignore` e não devem ser versionados.

"""
Script de Consolidação das Bases de Dados
==========================================
Une as planilhas:
  - Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx  (aba: Consolidado)
  - Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_2022_2026.xlsx    (aba: Consolidado)

Remove duplicatas por ['Nome do curso, guia ou programa', 'Instituição responsável'],
priorizando registros que possuem 'Data de lançamento'.
Cria coluna 'Ano de Lançamento' e salva em 'base_consolidada_final.xlsx'.
"""

import os
import re
import pandas as pd

# ---------------------------------------------------------------------------
# Caminhos dos arquivos fonte
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ARQUIVO_CONSOLIDADO_V1 = os.path.join(BASE_DIR, "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado_2.xlsx")
ARQUIVO_CONSOLIDADO_V1_ALT = os.path.join(BASE_DIR, "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx")

ARQUIVO_2022_2026_OPCOES = [
    os.path.join(BASE_DIR, "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_2022_2026.xlsx"),
    os.path.join(os.path.dirname(BASE_DIR), "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_2022_2026.xlsx"),
]

ARQUIVO_SAIDA = os.path.join(BASE_DIR, "base_consolidada_final.xlsx")

CHAVE_DEDUP = ['Nome do curso, guia ou programa', 'Instituicao responsavel']
CHAVE_DEDUP_ORIGINAL = ['Nome do curso, guia ou programa', 'Instituição responsável']

# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def encontrar_arquivo(caminhos):
    for c in caminhos:
        if os.path.exists(c):
            return c
    raise FileNotFoundError(f"Nenhum dos caminhos encontrado: {caminhos}")


def ler_aba_consolidado(caminho):
    try:
        df = pd.read_excel(caminho, sheet_name="Consolidado")
        print(f"  OK Lido: {os.path.basename(caminho)}  ->  {len(df)} registros")
        return df
    except Exception as e:
        print(f"  AVISO  Erro ao ler '{caminho}': {e}")
        return pd.DataFrame()


def extrair_ano(valor):
    if pd.isna(valor) or str(valor).strip() == '':
        return 'Nao informado'
    texto = str(valor)
    match = re.search(r'\b(202\d)\b', texto)
    return match.group(1) if match else 'Nao informado'


# ---------------------------------------------------------------------------
# Carregamento
# ---------------------------------------------------------------------------
print("\n Carregando planilhas...\n")

try:
    caminho_v1 = encontrar_arquivo([ARQUIVO_CONSOLIDADO_V1, ARQUIVO_CONSOLIDADO_V1_ALT])
except FileNotFoundError as e:
    print(f"ERRO {e}")
    caminho_v1 = None

df_v1 = ler_aba_consolidado(caminho_v1) if caminho_v1 else pd.DataFrame()

try:
    caminho_2026 = encontrar_arquivo(ARQUIVO_2022_2026_OPCOES)
except FileNotFoundError as e:
    print(f"ERRO {e}")
    caminho_2026 = None

df_v2 = ler_aba_consolidado(caminho_2026) if caminho_2026 else pd.DataFrame()

if df_v1.empty and df_v2.empty:
    raise RuntimeError("Nenhuma planilha foi carregada. Verifique os caminhos.")

# ---------------------------------------------------------------------------
# Concatenação
# ---------------------------------------------------------------------------
print("\nConcatenando bases...\n")

if not df_v1.empty:
    df_v1['_origem'] = 'v1'
if not df_v2.empty:
    df_v2['_origem'] = 'v2'

df_total = pd.concat([df_v1, df_v2], ignore_index=True)
print(f"  Total bruto (antes de deduplicar): {len(df_total)} registros")

# ---------------------------------------------------------------------------
# Deduplicação: priorizar registros COM 'Data de lançamento'
# ---------------------------------------------------------------------------
print("\nRemovendo duplicatas...\n")

# Determinar a chave correta (com ou sem acento)
col_inst = 'Instituição responsável' if 'Instituição responsável' in df_total.columns else 'Instituicao responsavel'
col_nome = 'Nome do curso, guia ou programa'

for col in [col_nome, col_inst]:
    if col not in df_total.columns:
        df_total[col] = 'Nao informado'

df_total[col_nome] = df_total[col_nome].astype(str).str.strip()
df_total[col_inst] = df_total[col_inst].astype(str).str.strip()

# Detectar nome da coluna de data (com ou sem acento)
col_data = None
for _candidate in ['Data de lançamento', 'Data de lancamento']:
    if _candidate in df_total.columns:
        col_data = _candidate
        break

if col_data:
    df_total['_tem_data'] = df_total[col_data].notna().astype(int)
else:
    df_total['_tem_data'] = 0

df_total = df_total.sort_values('_tem_data', ascending=False)
df_dedup = df_total.drop_duplicates(subset=[col_nome, col_inst], keep='first')
df_dedup = df_dedup.drop(columns=['_tem_data', '_origem'], errors='ignore')

print(f"  Total apos deduplicacao: {len(df_dedup)} registros")

# ---------------------------------------------------------------------------
# Criação da coluna 'Ano de Lançamento'
# ---------------------------------------------------------------------------
print("\nCriando coluna 'Ano de Lancamento'...\n")

if col_data and col_data in df_dedup.columns:
    df_dedup['Ano de Lancamento'] = df_dedup[col_data].apply(extrair_ano)
    # Adicionar também com acento para compatibilidade com app.py
    df_dedup['Ano de Lancamento'] = df_dedup['Ano de Lancamento'].fillna('Nao informado')
else:
    df_dedup['Ano de Lancamento'] = 'Nao informado'
    print("  AVISO coluna 'Data de lancamento' nao encontrada.")

distribuicao = df_dedup['Ano de Lancamento'].value_counts().sort_index()
print("  Distribuicao por Ano de Lancamento:")
for ano, qtd in distribuicao.items():
    print(f"    {ano}: {qtd} cursos")

# ---------------------------------------------------------------------------
# Salvar resultado
# ---------------------------------------------------------------------------
print(f"\nSalvando base consolidada em '{ARQUIVO_SAIDA}'...\n")
df_dedup.to_excel(ARQUIVO_SAIDA, index=False, sheet_name="Consolidado")
print(f"  Arquivo salvo com {len(df_dedup)} registros e {len(df_dedup.columns)} colunas.\n")
print("=" * 60)
print("  Consolidacao concluida com sucesso!")
print("=" * 60)

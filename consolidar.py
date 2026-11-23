"""
Script de Consolidação das Bases de Dados
==========================================
Une as planilhas-fonte localizadas em `dados/fontes/`:
  - Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx  (aba: Consolidado)
  - Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_2022_2026.xlsx    (aba: Consolidado)

Remove duplicatas por ['Nome do curso, guia ou programa', 'Instituição responsável']
(comparação sem diferenciar maiúsculas/espaços), priorizando registros que possuem
'Data de lançamento'. Normaliza a coluna 'Data de lançamento', cria a coluna
'Ano de Lançamento' e salva em 'base_consolidada_final.xlsx' (abas
'Consolidado' e 'Resumo por Lote'), que é o arquivo lido pelo app.py.

Uso:  python consolidar.py
"""

import os
import re
import datetime as dt

import pandas as pd

# ---------------------------------------------------------------------------
# Caminhos dos arquivos
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONTES_DIR = os.path.join(BASE_DIR, "dados", "fontes")

NOME_V1 = "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_Consolidado.xlsx"
NOME_V2 = "Mapeamento_Capacitacao_IA_ML_CienciaDados_Brasil_2022_2026.xlsx"

# Procura primeiro em dados/fontes/ e, por compatibilidade, na raiz do projeto.
ARQUIVO_V1_OPCOES = [os.path.join(FONTES_DIR, NOME_V1), os.path.join(BASE_DIR, NOME_V1)]
ARQUIVO_V2_OPCOES = [os.path.join(FONTES_DIR, NOME_V2), os.path.join(BASE_DIR, NOME_V2)]

ARQUIVO_SAIDA = os.path.join(BASE_DIR, "base_consolidada_final.xlsx")

COL_NOME = "Nome do curso, guia ou programa"
COL_INST = "Instituição responsável"
COL_DATA = "Data de lançamento"
COL_ANO = "Ano de Lançamento"
NAO_INFORMADO = "Não informado"

# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

def encontrar_arquivo(caminhos):
    for c in caminhos:
        if os.path.exists(c):
            return c
    return None


def ler_aba_consolidado(caminho):
    try:
        df = pd.read_excel(caminho, sheet_name="Consolidado")
        print(f"  OK Lido: {os.path.relpath(caminho, BASE_DIR)}  ->  {len(df)} registros")
        return df
    except Exception as e:
        print(f"  AVISO  Erro ao ler '{caminho}': {e}")
        return pd.DataFrame()


def normalizar_data(valor):
    """Converte valores mistos (datetime, int, texto) em texto legível."""
    if valor is None or (not isinstance(valor, str) and pd.isna(valor)):
        return NAO_INFORMADO
    if isinstance(valor, (dt.datetime, dt.date, pd.Timestamp)):
        return valor.strftime("%m/%Y")
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    texto = str(valor).strip()
    return texto if texto else NAO_INFORMADO


def extrair_ano(valor):
    match = re.search(r"\b(20\d{2})\b", str(valor))
    return match.group(1) if match else NAO_INFORMADO


def chave_normalizada(serie):
    return serie.astype(str).str.strip().str.lower().str.replace(r"\s+", " ", regex=True)


def ordem_natural(texto):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(texto))]


def main():
    # -----------------------------------------------------------------------
    # Carregamento
    # -----------------------------------------------------------------------
    print("\n Carregando planilhas...\n")
    caminho_v1 = encontrar_arquivo(ARQUIVO_V1_OPCOES)
    caminho_v2 = encontrar_arquivo(ARQUIVO_V2_OPCOES)
    if not caminho_v1:
        print(f"  AVISO  '{NOME_V1}' não encontrado.")
    if not caminho_v2:
        print(f"  AVISO  '{NOME_V2}' não encontrado.")

    df_v1 = ler_aba_consolidado(caminho_v1) if caminho_v1 else pd.DataFrame()
    df_v2 = ler_aba_consolidado(caminho_v2) if caminho_v2 else pd.DataFrame()

    if df_v1.empty and df_v2.empty:
        raise RuntimeError("Nenhuma planilha foi carregada. Verifique a pasta 'dados/fontes/'.")

    # -----------------------------------------------------------------------
    # Concatenação
    # -----------------------------------------------------------------------
    print("\nConcatenando bases...\n")
    partes = []
    if not df_v1.empty:
        partes.append(df_v1.assign(_origem=os.path.basename(caminho_v1)))
    if not df_v2.empty:
        partes.append(df_v2.assign(_origem=os.path.basename(caminho_v2)))
    df_total = pd.concat(partes, ignore_index=True)
    print(f"  Total bruto (antes de deduplicar): {len(df_total)} registros")

    # Compatibilidade com colunas sem acento
    df_total = df_total.rename(columns={
        "Instituicao responsavel": COL_INST,
        "Data de lancamento": COL_DATA,
    })
    for col in (COL_NOME, COL_INST):
        if col not in df_total.columns:
            df_total[col] = NAO_INFORMADO
        df_total[col] = df_total[col].astype(str).str.strip()

    # -----------------------------------------------------------------------
    # Deduplicação: priorizar registros COM 'Data de lançamento'
    # -----------------------------------------------------------------------
    print("\nRemovendo duplicatas...\n")
    if COL_DATA in df_total.columns:
        df_total["_tem_data"] = df_total[COL_DATA].notna().astype(int)
    else:
        df_total["_tem_data"] = 0
    df_total["_k_nome"] = chave_normalizada(df_total[COL_NOME])
    df_total["_k_inst"] = chave_normalizada(df_total[COL_INST])

    df_total = df_total.sort_values("_tem_data", ascending=False, kind="stable")
    df_dedup = df_total.drop_duplicates(subset=["_k_nome", "_k_inst"], keep="first").sort_index()
    print(f"  Total após deduplicação: {len(df_dedup)} registros "
          f"({len(df_total) - len(df_dedup)} duplicatas removidas)")

    # -----------------------------------------------------------------------
    # Normalização da data e criação de 'Ano de Lançamento'
    # -----------------------------------------------------------------------
    print("\nCriando coluna 'Ano de Lançamento'...\n")
    if COL_DATA in df_dedup.columns:
        df_dedup[COL_DATA] = df_dedup[COL_DATA].apply(normalizar_data)
    else:
        df_dedup[COL_DATA] = NAO_INFORMADO
        print("  AVISO coluna 'Data de lançamento' não encontrada.")
    df_dedup[COL_ANO] = df_dedup[COL_DATA].apply(extrair_ano)

    distribuicao = df_dedup[COL_ANO].value_counts().sort_index()
    print("  Distribuição por Ano de Lançamento:")
    for ano, qtd in distribuicao.items():
        print(f"    {ano}: {qtd} cursos")

    # -----------------------------------------------------------------------
    # Resumo por Lote (exibido na aba "Metodologia & Lotes" do dashboard)
    # -----------------------------------------------------------------------
    resumo = (
        df_dedup.groupby("Lote", dropna=False)
        .agg(Quantidade=(COL_NOME, "size"),
             Instituicoes=(COL_INST, "nunique"),
             Fonte=("_origem", lambda s: ", ".join(sorted(set(s)))))
        .reset_index()
        .rename(columns={"Instituicoes": "Instituições únicas", "Fonte": "Planilha de origem"})
    )
    resumo = resumo.sort_values("Lote", key=lambda s: s.map(ordem_natural)).reset_index(drop=True)
    resumo.loc[len(resumo)] = ["TOTAL", int(resumo["Quantidade"].sum()),
                               df_dedup[COL_INST].nunique(), ""]

    df_dedup = df_dedup.drop(columns=["_tem_data", "_origem", "_k_nome", "_k_inst"], errors="ignore")

    # -----------------------------------------------------------------------
    # Salvar resultado
    # -----------------------------------------------------------------------
    print(f"\nSalvando base consolidada em '{os.path.basename(ARQUIVO_SAIDA)}'...\n")
    with pd.ExcelWriter(ARQUIVO_SAIDA, engine="openpyxl") as writer:
        df_dedup.to_excel(writer, index=False, sheet_name="Consolidado")
        resumo.to_excel(writer, index=False, sheet_name="Resumo por Lote")
    print(f"  Arquivo salvo com {len(df_dedup)} registros e {len(df_dedup.columns)} colunas.\n")
    print("=" * 60)
    print("  Consolidação concluída com sucesso!")
    print("=" * 60)


if __name__ == "__main__":
    main()

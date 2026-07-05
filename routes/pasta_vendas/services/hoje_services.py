# services/hoje_services.py
from utils.conexao_global.conexao_firebird import FirebirdConnection

db = FirebirdConnection()


"""
TP_STATUS
ABERTO = 0
FINALIZADO = 1
EXCLUIDO = 2
VINCULADO = 3
CANCELADO = 4
"""

# ============================================
# FUNÇÕES POR PERÍODO (inicio e fim)
# ============================================

def buscar_vendas_finalizados_por_periodo(data_inicio, data_fim):
    """Busca vendas FINALIZADAS (TP_STATUS = 1) em um período"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT VL_TOTAL_NOTA
            FROM movimentos
            WHERE DT_EMISSAO BETWEEN ? AND ?
            AND TIPO = 0
            AND TP_STATUS = 1
        """, (data_inicio, data_fim))

        dados = cursor.fetchall()
        total_finalizados = len(dados)
        faturamento_finalizados = sum(float(row[0] or 0) for row in dados)
        return total_finalizados, faturamento_finalizados


def buscar_vendas_excluidos_por_periodo(data_inicio, data_fim):
    """Busca vendas EXCLUÍDOS (TP_STATUS = 2) em um período"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT VL_TOTAL_NOTA
            FROM movimentos
            WHERE DT_EMISSAO BETWEEN ? AND ?
            AND TIPO = 0
            AND TP_STATUS = 2
        """, (data_inicio, data_fim))

        dados = cursor.fetchall()
        total_excluidos = len(dados)
        faturamento_excluidos = sum(float(row[0] or 0) for row in dados)
        return total_excluidos, faturamento_excluidos


def buscar_vendas_abertas_por_periodo(data_inicio, data_fim):
    """Busca vendas ABERTAS (TP_STATUS = 0) em um período"""
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT VL_TOTAL_NOTA
            FROM movimentos
            WHERE DT_EMISSAO BETWEEN ? AND ?
            AND TIPO = 0
            AND TP_STATUS = 0
        """, (data_inicio, data_fim))

        dados = cursor.fetchall()
        total_abertos = len(dados)
        faturamento_abertos = sum(float(row[0] or 0) for row in dados)
        return total_abertos, faturamento_abertos


# ============================================
# FUNÇÕES POR DATA ÚNICA (backwards compatibility)
# ============================================

def buscar_vendas_finalizados(data_consulta):
    """Busca vendas FINALIZADAS de uma data específica"""
    return buscar_vendas_finalizados_por_periodo(data_consulta, data_consulta)


def buscar_vendas_excluidos(data_consulta):
    """Busca vendas EXCLUÍDOS de uma data específica"""
    return buscar_vendas_excluidos_por_periodo(data_consulta, data_consulta)


def buscar_vendas_abertas(data_consulta):
    """Busca vendas ABERTAS de uma data específica"""
    return buscar_vendas_abertas_por_periodo(data_consulta, data_consulta)
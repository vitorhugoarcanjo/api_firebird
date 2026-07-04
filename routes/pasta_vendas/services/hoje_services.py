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
" FINALIZADO "
def buscar_vendas_finalizados(data_consulta):
    """
    Busca todas as vendas FINALIZADAS (TP_STATUS = 1) de uma data específica.
    Retorna: (total_vendas, faturamento)
    """
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT VL_TOTAL_NOTA
            FROM movimentos
            WHERE DT_EMISSAO = ?
            AND TIPO = 0
            AND TP_STATUS = 1
        """, (data_consulta,))

        dados = cursor.fetchall()

        total_finalizados = len(dados)
        faturamento_finalizados = sum(float(row[0] or 0) for row in dados)

        return total_finalizados, faturamento_finalizados

" EXCLUIDO "
def buscar_vendas_excluidos(data_consulta):
    """
    Busca todas as vendas EXCLUIDOS (TP_STATUS = 2)
    """
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT VL_TOTAL_NOTA
            FROM movimentos
            WHERE DT_EMISSAO = ?
            AND TP_STATUS = 2
        """, (data_consulta,))
        dados = cursor.fetchall()

        total_excluidos = len(dados)
        faturamento_excluidos = sum(float(row[0] or 0) for row in dados)

        return total_excluidos, faturamento_excluidos

" ABERTOS "
def buscar_vendas_abertas(data_consulta):
    """
    Busca vendas ABERTAS (TP_STATUS = 0)
    """
    with db.get_cursor() as cursor:
        cursor.execute("""
            SELECT VL_TOTAL_NOTA
            FROM movimentos
            WHERE DT_EMISSAO = ?
            AND TP_STATUS = 0
        """, (data_consulta,))
        dados = cursor.fetchall()

        total_abertos = len(dados)
        faturamento_abertos = sum(float(row[0] or 0) for row in dados)

        return total_abertos, faturamento_abertos

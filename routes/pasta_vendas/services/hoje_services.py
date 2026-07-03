from utils.conexao_global.conexao_firebird import FirebirdConnection

db = FirebirdConnection()

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

        total_vendas = len(dados)
        faturamento = sum(float(row[0] or 0) for row in dados)

        return total_vendas, faturamento

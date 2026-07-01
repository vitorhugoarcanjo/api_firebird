# routes/pasta_vendas/hoje.py
from flask import jsonify
from utils.conexao_global.conexao_firebird import FirebirdConnection

db = FirebirdConnection()

def ini_hoje():
    """Retorna vendas do dia atual (status 1 = faturado)"""
    try:
        with db.get_cursor() as cursor:
            # Busca os valores de VL_TOTAL_NOTA do dia
            cursor.execute("""
                SELECT VL_TOTAL_NOTA
                FROM movimentos
                WHERE DT_EMISSAO = CURRENT_DATE
                AND TP_STATUS = 1
            """)
            
            dados = cursor.fetchall()
            
            # Calcula no Python
            total_vendas = len(dados)
            faturamento = sum(float(row[0] or 0) for row in dados)
            
            return jsonify({
                'status': 'sucesso',
                'total_vendas': total_vendas,
                'faturamento': faturamento
            })
            
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500
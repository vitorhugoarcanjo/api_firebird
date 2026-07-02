# routes/pasta_vendas/hoje.py
from flask import jsonify, request
from utils.conexao_global.conexao_firebird import FirebirdConnection
from datetime import datetime

db = FirebirdConnection()

def ini_hoje():
    """
        Retorna vendas de uma data específica.
            - Se enviar ?data=YYYY-MM-DD, consulta essa data
            - Se não enviar data, consulta hoje
    """
    try:
        # Pega a data da requisição
        data_param = request.args.get('data', '')

        if data_param:
            # Valida o formato para nao ter SQL injection
            try:
                datetime.strptime(data_param, '%Y-%m-%d')
                data_consulta = data_param
            
            except ValueError:
                return jsonify ({
                    'status': 'erro',
                    'mensagem': 'Data inválida. Use o formato YYYY-MM-DD'
                }), 400
        
        else:
            # Se não houver data, usa hoje
            data_consulta = datetime.now().strftime('%Y-%m-%d')

        # Executa a consulta com a data escolhida
        with db.get_cursor() as cursor:
            # Busca os valores de VL_TOTAL_NOTA do dia
            cursor.execute("""
                SELECT VL_TOTAL_NOTA
                FROM movimentos
                WHERE DT_EMISSAO = CURRENT_DATE
                AND TP_STATUS = 1
            """, (data_consulta,))
            
            dados = cursor.fetchall()
            
            # Calcula no Python
            total_vendas = len(dados)
            faturamento = sum(float(row[0] or 0) for row in dados)
            
            return jsonify({
                'status': 'sucesso',
                'data_consulta': data_consulta,
                'total_vendas': total_vendas,
                'faturamento': faturamento
            })
            
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500
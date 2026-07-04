# routes/pasta_vendas/hoje.py
from flask import jsonify, request
from datetime import datetime
from utils.conexao_global.conexao_firebird import FirebirdConnection
from .services.hoje_services import buscar_vendas_finalizados, buscar_vendas_excluidos, buscar_vendas_abertas

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

        total_finalizados, faturamento_finalizados = buscar_vendas_finalizados(data_consulta)
        total_excluidos, faturamento_excluidos = buscar_vendas_excluidos(data_consulta)
        total_abertos, faturamento_abertos = buscar_vendas_abertas(data_consulta)
            
        return jsonify({
            'status': 'sucesso',
            'data_consulta': data_consulta,
            'total_finalizados': total_finalizados,
            'faturamento_finalizados': faturamento_finalizados,
            'total_excluidos': total_excluidos,
            'faturamento_excluidos': faturamento_excluidos,
            'total_abertos': total_abertos,
            'faturamento_abertos': faturamento_abertos
        })
            
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)}), 500
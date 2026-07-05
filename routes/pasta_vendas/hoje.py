# routes/pasta_vendas/hoje.py
from flask import jsonify, request
from datetime import datetime
from utils.conexao_global.conexao_firebird import FirebirdConnection
from .services.hoje_services import (
    buscar_vendas_finalizados_por_periodo,
    buscar_vendas_excluidos_por_periodo,
    buscar_vendas_abertas_por_periodo
)

db = FirebirdConnection()

def ini_hoje():
    """
    Retorna vendas de um período específico.
    - Se enviar ?inicio=YYYY-MM-DD&fim=YYYY-MM-DD, consulta o período
    - Se enviar ?data=YYYY-MM-DD, consulta uma data específica (backwards compatibility)
    - Se não enviar nada, consulta hoje
    """
    try:
        # Pega os parâmetros
        inicio = request.args.get('inicio', '')
        fim = request.args.get('fim', '')
        data_param = request.args.get('data', '')

        # 🔥 PRIORIDADE: inicio + fim
        if inicio and fim:
            # Valida as datas
            try:
                datetime.strptime(inicio, '%Y-%m-%d')
                datetime.strptime(fim, '%Y-%m-%d')
                data_inicio = inicio
                data_fim = fim
                data_consulta = f"{datetime.strptime(inicio, '%Y-%m-%d').strftime('%d/%m/%Y')} a {datetime.strptime(fim, '%Y-%m-%d').strftime('%d/%m/%Y')}"
            except ValueError:
                return jsonify({
                    'status': 'erro',
                    'mensagem': 'Datas inválidas. Use o formato YYYY-MM-DD'
                }), 400
        
        # 🔥 BACKWARDS COMPATIBILITY: data (antigo)
        elif data_param:
            try:
                datetime.strptime(data_param, '%Y-%m-%d')
                data_inicio = data_param
                data_fim = data_param
                data_consulta = datetime.strptime(data_param, '%Y-%m-%d').strftime('%d/%m/%Y')
            except ValueError:
                return jsonify({
                    'status': 'erro',
                    'mensagem': 'Data inválida. Use o formato YYYY-MM-DD'
                }), 400
        
        # 🔥 DEFAULT: hoje
        else:
            hoje = datetime.now().strftime('%Y-%m-%d')
            data_inicio = hoje
            data_fim = hoje
            data_consulta = datetime.now().strftime('%d/%m/%Y')

        # 🔥 CHAMA AS FUNÇÕES COM PERÍODO
        total_finalizados, faturamento_finalizados = buscar_vendas_finalizados_por_periodo(data_inicio, data_fim)
        total_excluidos, faturamento_excluidos = buscar_vendas_excluidos_por_periodo(data_inicio, data_fim)
        total_abertos, faturamento_abertos = buscar_vendas_abertas_por_periodo(data_inicio, data_fim)
            
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
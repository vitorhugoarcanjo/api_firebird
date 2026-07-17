# routes/pasta_conexoes/routes.py
from flask import Blueprint, render_template, request, jsonify, url_for, redirect
import fdb
from .gerenciador_conexoes import gerenciador

bp_conexoes = Blueprint('conexoes', __name__, url_prefix='/conexoes')

@bp_conexoes.route('/tela_conexoes', methods=['GET'])
def page_cadastrar():
    """Página de cadastro de conexão"""
    conexoes_cadastradas = gerenciador.listar_todas()

    return render_template('pasta_conexoes/conexoes.html', conexoes_cadastradas=conexoes_cadastradas)

@bp_conexoes.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    """Processa o cadastro de conexão"""
    try:
        nome = request.form.get('nome')
        host = request.form.get('host')
        database = request.form.get('database')
        usuario = request.form.get('usuario') or 'SYSDBA'
        senha = request.form.get('senha') or 'masterkey'
        porta = int(request.form.get('porta') or 3050)
        padrao = request.form.get('padrao') == 'on'

        if not nome or not host or not database:
            return render_template(
                'pasta_conexoes/cadastrar_conexao.html',
                mensagem='Preencha os campos obrigatórios: Nome, Host e Database.',
                tipo_mensagem='erro'
            )

        id_conn = gerenciador.cadastrar(nome, host, database, usuario, senha, porta, padrao)

        if padrao:
            gerenciador.definir_ativa(id_conn)

        return redirect(url_for('conexoes.page_cadastrar'))

    except Exception as e:
        return render_template(
            'pasta_conexoes/cadastrar_conexao.html',
            mensagem=f'❌ Erro ao cadastrar: {str(e)}',
            tipo_mensagem='erro'
        )
    


# ============================================
# ROTA PARA TESTAR CONEXÃO (AJAX)
# ============================================
@bp_conexoes.route('/testar', methods=['POST'])
def testar_conexao():
    """
    Testa a conexão com o Firebird usando as credenciais enviadas.
    """
    try:
        dados = request.get_json()
        
        host = dados.get('host')
        database = dados.get('database')
        usuario = dados.get('usuario') or 'SYSDBA'
        senha = dados.get('senha') or 'masterkey'
        porta = dados.get('porta') or 3050

        # Tenta conectar
        conn = fdb.connect(
            host=host,
            database=database,
            user=usuario,
            password=senha,
            port=int(porta),
            charset='UTF8'
        )
        
        # Tenta fazer uma consulta simples pra ver se tá tudo ok
        cursor = conn.cursor()
        cursor.execute("SELECT RDB$GET_CONTEXT('SYSTEM', 'ENGINE_VERSION') FROM RDB$DATABASE")
        versao = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'status': 'sucesso',
            'mensagem': f'Conexão estabelecida com sucesso!',
            'versao': versao.strip()
        })
        
    except fdb.Error as e:
        return jsonify({
            'status': 'erro',
            'mensagem': f'Erro Firebird: {str(e)}'
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'mensagem': f'Erro: {str(e)}'
        }), 400
from flask import Flask, render_template, redirect

from config.imports_blueprints import ini_imports_blueprints
from config.imports_tabelas import ini_imports_tabelas
from routes.pasta_conexoes_bd.conexoes import gerenciador

from utils.conexao_global.conexao_firebird import verificar_conexao, db

app = Flask(__name__)

# 1. Registra os blueprints (rotas)
ini_imports_blueprints(app)

# 2. Inicializa as tabelas do SQLite
ini_imports_tabelas()


# ==========================================
# 🔥 CONTEXT PROCESSOR - DISPONÍVEL EM TODAS AS PÁGINAS
# ==========================================
@app.context_processor
def inject_globals():
    """Variáveis disponíveis em TODOS os templates"""
    # Verifica se tem conexão ativa
    tem_conexao = db.tem_conexao if hasattr(db, 'tem_conexao') else False

    return {
        'tem_conexao': tem_conexao,
        'versao_sistema': 'v1.0'
    }

@app.route('/')
def inicio():
    # Verifica se tem conexão ativa
    conexao = gerenciador.buscar_ativa()
    
    if not conexao:
        # Verifica se tem alguma cadastrada
        todas = gerenciador.listar_todas()
        if todas:
            # Ativa a primeira
            gerenciador.definir_ativa(todas[0]['id'])
            conexao = gerenciador.buscar_ativa()
        else:
            # 🔥 AVISO: mostra a página inicial com aviso
            return render_template(
                'pasta_inicio/inicio.html',
                aviso_sem_conexao=True
            )
    
    return render_template('pasta_inicio/inicio.html', aviso_sem_conexao=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

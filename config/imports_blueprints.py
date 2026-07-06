from routes.pasta_vendas import bp_vendas
from routes.pasta_conexoes_bd.conexoes import bp_conexoes

def ini_imports_blueprints(app):
    app.register_blueprint(bp_vendas, url_prefix="/vendas")
    app.register_blueprint(bp_conexoes, url_prefix="/conexoes")
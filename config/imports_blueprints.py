from routes.pasta_vendas import bp_vendas

def ini_imports_blueprints(app):
    app.register_blueprint(bp_vendas, url_prefix="/vendas")
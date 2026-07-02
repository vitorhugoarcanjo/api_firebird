from flask import Blueprint

from .paginas import pagina_vendas
from .hoje import ini_hoje
# from .mensal import ini_mensal

bp_vendas = Blueprint('vendas', __name__)

# ROTAS -- PAGINAS HTML GLOBAL
bp_vendas.add_url_rule('', view_func=pagina_vendas, methods=['GET'])

# ROTAS -- HOJE
bp_vendas.add_url_rule('/hoje', view_func=ini_hoje, methods=['GET'])

# ROTAS -- MENSAL
# bp_vendas.add_url_rule('/mensal', view_func=ini_mensal, methods=['GET'])
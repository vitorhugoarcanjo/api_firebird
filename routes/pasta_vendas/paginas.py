# routes/pasta_vendas/paginas.py
from flask import render_template

def pagina_vendas():
    """Página HTML com o dashboard de vendas"""
    return render_template('pasta_vendas/vendas.html')
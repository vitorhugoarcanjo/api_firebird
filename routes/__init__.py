from flask import Blueprint
bp_vendas = Blueprint('vendas', __name__)

from .pasta_vendas import diaria, mensal
# config/imports_tabelas.py
import os
import sqlite3
from routes.pasta_conexoes_bd.tabela_conexoes import criar_tabela_conexoes_sqlite

# Caminho do banco SQLite
CAMINHO_BANCO = os.path.join(os.getcwd(), 'instance', 'conexoes_externa.db')

def ini_imports_tabelas():
    """Inicializa as tabelas no SQLite"""
    
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    criar_tabela_conexoes_sqlite(cursor)

    conexao.commit()
    cursor.close()
    conexao.close()
    print("✅ Tabelas inicializadas com sucesso!")
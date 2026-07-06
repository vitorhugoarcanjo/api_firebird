# routes/pasta_conexoes_bd/tabela_conexoes.py

def criar_tabela_conexoes_sqlite(cursor):
    """Cria a tabela de conexões se não existir"""
    # Verifica se a tabela existe
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='conexoes_firebird'
    """)
    resultado = cursor.fetchone()

    # Se não existir, cria
    if not resultado:
        cursor.execute("""
            CREATE TABLE conexoes_firebird (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                host TEXT NOT NULL,
                database TEXT NOT NULL,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL,
                porta INTEGER DEFAULT 3050,
                ativa INTEGER DEFAULT 0,
                padrao INTEGER DEFAULT 0
            )
        """)
        print("✅ Tabela 'conexoes_firebird' criada com sucesso!")
    else:
        print("ℹ️ Tabela 'conexoes_firebird' já existe.")
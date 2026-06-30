from conexao_firebird import FirebirdConnection

db = FirebirdConnection()

with db.get_cursor() as cursor:
    # Query mais simples possível pra testar conexão
    cursor.execute("SELECT 1 FROM RDB$DATABASE")
    resultado = cursor.fetchone()
    
    if resultado:
        print("✅ CONEXÃO OK! Banco acessível!")
        print(f"   Resultado do teste: {resultado[0]}")
    else:
        print("❌ Deu ruim na conexão...")
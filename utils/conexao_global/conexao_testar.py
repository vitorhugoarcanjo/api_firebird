from conexao_firebird import FirebirdConnection

db = FirebirdConnection()

with db.get_cursor() as cursor:
    print("🔍 Buscando VL_TOTAL_NOTA de hoje...")
    cursor.execute("""
        SELECT VL_TOTAL_NOTA
        FROM movimentos
        WHERE DT_EMISSAO = CURRENT_DATE
        AND TIPO = 0
    """)
    
    dados = cursor.fetchall()
    
    if dados:
        total = len(dados)
        soma = sum(float(row[0] or 0) for row in dados)
        print(f"✅ Total vendas: {total}")
        print(f"✅ Faturamento: R$ {soma:.2f}")
        
        # Mostra os 5 primeiros valores
        print("\n📋 Primeiros valores:")
        for i, row in enumerate(dados[:5]):
            print(f"   {i+1}: R$ {row[0]:.2f}")
    else:
        print("❌ Nenhuma venda encontrada para hoje com status 1")
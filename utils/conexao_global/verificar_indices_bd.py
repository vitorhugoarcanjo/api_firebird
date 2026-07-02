from conexao_firebird import FirebirdConnection

db = FirebirdConnection()

with db.get_cursor() as cursor:
    cursor.execute("""
        SELECT 
            RDB$INDEX_NAME,
            RDB$FIELD_NAME
        FROM RDB$INDEX_SEGMENTS
        WHERE RDB$FIELD_NAME IN ('DT_EMISSAO', 'TP_STATUS')
    """)
    
    indices = cursor.fetchall()
    
    if indices:
        print("✅ Índices encontrados:")
        for idx in indices:
            print(f"   - {idx[0].strip()} (campo: {idx[1].strip()})")
    else:
        print("❌ NENHUM índice encontrado para DT_EMISSAO ou TP_STATUS!")
        print("⚠️ Isso vai deixar as consultas LENTAS!")
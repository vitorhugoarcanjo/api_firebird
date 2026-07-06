# core/gerenciador_conexoes.py
import sqlite3
import os

CAMINHO_BANCO = os.path.join(os.getcwd(), 'instance', 'conexoes_externa.db')

class GerenciadorConexoes:
    """Gerencia as conexões cadastradas no SQLite"""
    
    def __init__(self):
        self.caminho = CAMINHO_BANCO
    
    def _conectar(self):
        return sqlite3.connect(self.caminho)
    
    # ============================================
    # CADASTRAR (COM OPÇÃO DE PADRÃO)
    # ============================================
    def cadastrar(self, nome, host, database, usuario, senha, porta=3050, padrao=False):
        """Cadastra uma nova conexão"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Se esta conexão for marcada como padrão, desmarca todas as outras
            if padrao:
                cursor.execute("UPDATE conexoes_firebird SET padrao = 0")
            
            cursor.execute("""
                INSERT INTO conexoes_firebird (nome, host, database, usuario, senha, porta, padrao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (nome, host, database, usuario, senha, porta, 1 if padrao else 0))
            
            conn.commit()
            return cursor.lastrowid
    
    # ============================================
    # LISTAR TODAS (COM ORDEM: PADRÃO PRIMEIRO)
    # ============================================
    def listar_todas(self):
        """Lista todas as conexões cadastradas"""
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, host, database, usuario, porta, ativa, padrao
                FROM conexoes_firebird
                ORDER BY padrao DESC, ativa DESC, nome
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    # ============================================
    # BUSCAR PADRÃO
    # ============================================
    def buscar_padrao(self):
        """Retorna a conexão marcada como padrão"""
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, host, database, usuario, senha, porta
                FROM conexoes_firebird
                WHERE padrao = 1
                LIMIT 1
            """)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    # ============================================
    # BUSCAR ATIVA
    # ============================================
    def buscar_ativa(self):
        """Retorna a conexão que está ativa (prioriza padrão)"""
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 🔥 Primeiro tenta buscar a ativa
            cursor.execute("""
                SELECT id, nome, host, database, usuario, senha, porta
                FROM conexoes_firebird
                WHERE ativa = 1
                LIMIT 1
            """)
            row = cursor.fetchone()
            
            # Se não tiver ativa, busca a padrão
            if not row:
                cursor.execute("""
                    SELECT id, nome, host, database, usuario, senha, porta
                    FROM conexoes_firebird
                    WHERE padrao = 1
                    LIMIT 1
                """)
                row = cursor.fetchone()
                # Se tiver padrão, ativa ela automaticamente
                if row:
                    self.definir_ativa(row['id'])
            
            return dict(row) if row else None
    
    # ============================================
    # DEFINIR ATIVA
    # ============================================
    def definir_ativa(self, id_conexao):
        """Define qual conexão está ativa (desativa as outras)"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE conexoes_firebird SET ativa = 0")
            cursor.execute("UPDATE conexoes_firebird SET ativa = 1 WHERE id = ?", (id_conexao,))
            conn.commit()
    
    # ============================================
    # DEFINIR PADRÃO
    # ============================================
    def definir_padrao(self, id_conexao):
        """Define qual conexão é a padrão (desmarca as outras)"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE conexoes_firebird SET padrao = 0")
            cursor.execute("UPDATE conexoes_firebird SET padrao = 1 WHERE id = ?", (id_conexao,))
            conn.commit()
    
    # ============================================
    # ATUALIZAR
    # ============================================
    def atualizar(self, id_conexao, nome, host, database, usuario, senha, porta=3050, padrao=False):
        """Atualiza uma conexão existente"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Se esta conexão for marcada como padrão, desmarca todas as outras
            if padrao:
                cursor.execute("UPDATE conexoes_firebird SET padrao = 0")
            
            cursor.execute("""
                UPDATE conexoes_firebird
                SET nome = ?, host = ?, database = ?, usuario = ?, senha = ?, porta = ?, padrao = ?
                WHERE id = ?
            """, (nome, host, database, usuario, senha, porta, 1 if padrao else 0, id_conexao))
            conn.commit()
    
    # ============================================
    # EXCLUIR
    # ============================================
    def excluir(self, id_conexao):
        """Exclui uma conexão"""
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM conexoes_firebird WHERE id = ?", (id_conexao,))
            conn.commit()
    
    # ============================================
    # BUSCAR POR ID
    # ============================================
    def buscar_por_id(self, id_conexao):
        """Busca uma conexão pelo ID"""
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome, host, database, usuario, senha, porta, ativa, padrao
                FROM conexoes_firebird
                WHERE id = ?
            """, (id_conexao,))
            row = cursor.fetchone()
            return dict(row) if row else None

# Instância única (singleton)
gerenciador = GerenciadorConexoes()
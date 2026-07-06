# core/conexao_firebird.py
import fdb
import logging
from contextlib import contextmanager
from typing import Generator
from routes.pasta_conexoes_bd.gerenciador_conexoes import gerenciador

logger = logging.getLogger(__name__)

class FirebirdConnection:
    """
    CLASSE SINGLETON PARA GERENCIAR CONEXÕES COM FIREBIRD.
    USA A CONEXÃO ATIVA CADASTRADA NO GERENCIADOR.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebirdConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._carregar_conexao()
    
    def _carregar_conexao(self):
        dados = gerenciador.buscar_ativa()
        
        if dados:
            self.host = dados['host']
            self.database = dados['database']
            self.user = dados['usuario']
            self.password = dados['senha']
            self.port = dados['porta']
            self.nome_conexao = dados['nome']
            logger.info(f"🔗 Conexão ativa: {self.nome_conexao} ({self.host})")
        else:
            self.host = '127.0.0.1'
            self.database = 'D:/Sol.NET/Banco de Dados/JI-PARANA/SOLNET.FDB'
            self.user = 'SYSDBA'
            self.password = 'masterkey'
            self.port = 3050
            self.nome_conexao = 'Padrão (fallback)'
            logger.warning("⚠️ Nenhuma conexão ativa. Usando fallback.")
        
        self.isolation_level = fdb.ISOLATION_LEVEL_READ_COMMITED

    def recarregar_conexao(self):
        self._carregar_conexao()
        logger.info("🔄 Conexão recarregada com sucesso!")

    @contextmanager
    def get_cursor(self) -> Generator[fdb.Cursor, None, None]:
        conexao = None
        cursor = None

        try:
            conexao = fdb.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                isolation_level=self.isolation_level,
                charset='UTF8'
            )
            cursor = conexao.cursor()
            logger.info(f"Conexão aberta em {self.host}")
            yield cursor
            conexao.commit()

        except fdb.Error as e:
            logger.error(f"Erro no Firebird: {e}")
            if conexao:
                conexao.rollback()
            raise

        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            if conexao:
                conexao.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
                logger.info("Conexão fechada")

    @contextmanager
    def get_connection(self) -> Generator[fdb.Connection, None, None]:
        conexao = None
        try:
            conexao = fdb.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port,
                isolation_level=self.isolation_level,
                charset='UTF8'
            )
            logger.info(f"Conexão aberta em {self.host}")
            yield conexao
            conexao.commit()
        
        except Exception as e:
            logger.error(f"Erro: {e}")
            if conexao:
                conexao.rollback()
            raise

        finally:
            if conexao:
                conexao.close()
                logger.info("Conexão fechada")


# ============================================
# FUNÇÕES UTILITÁRIAS
# ============================================

def verificar_conexao():
    """
    Verifica se existe conexão ativa ou cadastrada.
    Retorna: (tem_conexao, mensagem, dados_conexao)
    """
    dados = gerenciador.buscar_ativa()
    
    if dados:
        return True, f"Conexão ativa: {dados['nome']}", dados
    
    todas = gerenciador.listar_todas()
    
    if todas:
        primeira = todas[0]
        gerenciador.definir_ativa(primeira['id'])
        dados = gerenciador.buscar_ativa()
        return True, f"Conexão '{primeira['nome']}' ativada automaticamente", dados
    
    return False, "Nenhuma conexão cadastrada. Cadastre uma para começar.", None


def verificar_antes_de_consultar():
    """Versão simplificada para usar antes de qualquer consulta"""
    tem, msg, _ = verificar_conexao()
    if tem:
        return True, None
    return False, msg
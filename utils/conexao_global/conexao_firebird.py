import fdb
import logging
from contextlib import contextmanager
from typing import Optional, Generator

# configuração para logging para ver erros
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirebirdConnection:
    """
    CLASE SINGLETON PARA GERENCIAR CONEXÕES COM FIREBIRD.
    ABE E FECHA A CONEXÃO AUTOMATICAMENTE USANDO O CONTEXT MANAGER
    """

    _instance = None
    _connection = None

    def __new__(cls):
        """ GARANTE QUE SÓ EXISTA UMA INSTANCIA DA CLASSE (SINGLETON)"""
        if cls._instance is None:
            cls._instance = super(FirebirdConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """ CONFIGURA OS PARAMETROS DE CONEXÃO """
        self.host = '127.0.0.1' # IP SERVIDOR
        self.database = 'D:/Sol.NET/Banco de Dados/SOLNET.FDB' # CAMINHO DO .FDB
        self.user = 'SYSDBA'
        self.password = 'masterkey'
        self.port = 3050 # Porta padrão Firebird

        # Configuração para leitura SEM TRAVAR o banco
        self.isolation_level = fdb.ISOLATION_LEVEL_READ_COMMITED

    @contextmanager
    def get_cursor(self) -> Generator[fdb.Cursor, None, None]:
        """
        GERENCIADOR DE CONTEXTO - A mágica acontece aqui!
        Use com 'with' para abrir e fechar a conexão automaticamente.
        """
        conexao = None
        cursor = None

        try:
            # Abre a conexão apenas quando for usar
            conexao = fdb.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port,
                isolation_level = self.isolation_level,
                charset = 'UTF8'
            )
            # Cria o cursor
            cursor = conexao.cursor()
            
            logger.info(f"Conexão aberta com sucesso em {self.host}")
            
            # Retorna o cursor pro bloco 'with' usar
            yield cursor

            # Se chegou aqui sem erros, confirma a transação (SELECT não precisa, mas mantém padrão)
            conexao.commit()

        except fdb.Error as e:
            logger.error(f"Erro no firebird: {e}")
            if conexao:
                conexao.rollback() # Desfaz qualquer transação pendente
            raise # Repassa o erro pra quem chamou

        except Exception as e:
            logger.error(f"Erro inesperado: {e}")
            if conexao:
                conexao.rollback()
            raise

        finally:
            # FECHA TUDO - Isso é executado SEMPRE, mesmo com erro!
            if cursor:
                cursor.close()
                logger.debug("Cursor Fechado")

            if conexao:
                conexao.close()
                logger.info("Conexão fechada com sucesso")

        
    @contextmanager
    def get_connection(self) -> Generator[fdb.Connection, None, None]:
        """
        Caso você precise da conexão inteira (não só do cursor)
        """
        conexao = None
        try:
            conexao = fdb.connect(
                host = self.host,
                database = self.database,
                user = self.user,
                password = self.password,
                port = self.port,
                isolation_level = self.isolation_level,
                charset = 'UTF8'
            )

            logger.info(f"Conexão aberta com sucesso em {self.host}")
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
                logger.info("Conexão fechada com sucesso")

import sqlite3
import os

'''
Gerencia a conexão com o banco de dados SQLite e a execução de comandos SQL.
'''

class DBManager:
    '''Inicializa o gerenciador de banco de dados, criando o banco e a tabela se necessário.'''
    def __init__(self, DB_NOME='tb_logs.db', SCHEMA_NOME='schema.sql'):

        self.diretorio_base = os.path.dirname(os.path.abspath(__file__))
        
        self.pasta_db = self.diretorio_base 
        
        self.db_path = os.path.join(self.pasta_db, DB_NOME)
        self.schema_path = os.path.join(self.pasta_db, SCHEMA_NOME)
        self.connection = None

        self._inicializar()

    def _inicializar(self):
        # Cria a pasta caso ela não exista (útil se você mover o script depois)
        os.makedirs(self.pasta_db, exist_ok=True)
        try:
            with sqlite3.connect(self.db_path) as conn:
                with open(self.schema_path, 'r', encoding='utf-8') as f:
                    conn.executescript(f.read())
            print(f"[INFO] Banco inicializado em: {self.db_path}")
        except FileNotFoundError:
            print(f"[ERRO] O arquivo de schema não foi encontrado em: {self.schema_path}")
        except sqlite3.Error as e:
            print(f"[ERRO] Falha ao inicializar o banco: {e}")

    def salvar(self, entrada: str, tipo_com: str, status: int, saida: str, tipo_saida: str, path: str):
        '''Salva um log no banco de dados.'''
        sql = """
        INSERT INTO tb_logs 
        (entrada_comunicacao, tpcomunicacao, status_mensagem, saida_comunicacao, tpsaida, logging_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(sql, (entrada, tipo_com, status, saida, tipo_saida, path))
            print(f"[SUCESSO] Log salvo: {entrada[:20]}... -> {tipo_com}")
            return True
        except sqlite3.Error as e:
            print(f"[ERRO] Não foi possível salvar no banco: {e}")
            return False

    def consultar_logs(self):
        '''Consulta todos os logs armazenados no banco de dados.'''
        
        sql = "SELECT * FROM tb_logs"
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(sql)
                logs = cursor.fetchall()
            return logs
        except sqlite3.Error as e:
            print(f"[ERRO] Não foi possível consultar os logs: {e}")
            return []
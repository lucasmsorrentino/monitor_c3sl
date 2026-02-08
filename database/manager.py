import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="historico.db"):
        # Define o caminho absoluto para evitar criar o banco no lugar errado
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, 'data', db_name)
        
        # Cria a pasta data se não existir
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        print(f"--- BANCO DE DADOS: {self.db_path} ---") # Debug para sabermos onde ele está
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        # AQUI ESTÁ O SEGREDO: A tabela tem que ter as 4 colunas!
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS noticias (
                link TEXT PRIMARY KEY,
                titulo TEXT,
                content_hash TEXT,
                data_ultima_verificacao TIMESTAMP
            )
        """)
        self.conn.commit()

    def obter_hash_salvo(self, link):
        """Retorna o hash (impressão digital) salvo para um link."""
        try:
            self.cursor.execute("SELECT content_hash FROM noticias WHERE link = ?", (link,))
            resultado = self.cursor.fetchone()
            return resultado[0] if resultado else None
        except sqlite3.OperationalError:
            # Se der erro aqui, é porque a tabela está errada
            return None

    def salvar_ou_atualizar(self, titulo, link, content_hash):
        """Insere se for novo, atualiza se já existir."""
        data_atual = datetime.now()
        
        try:
            # Tenta inserir uma nova linha
            self.cursor.execute(
                "INSERT INTO noticias (link, titulo, content_hash, data_ultima_verificacao) VALUES (?, ?, ?, ?)",
                (link, titulo, content_hash, data_atual)
            )
        except sqlite3.IntegrityError:
            # Se já existe (IntegrityError), fazemos o UPDATE
            self.cursor.execute(
                "UPDATE noticias SET titulo = ?, content_hash = ?, data_ultima_verificacao = ? WHERE link = ?",
                (titulo, content_hash, data_atual, link)
            )
        self.conn.commit()

    def existe(self, link):
        self.cursor.execute("SELECT 1 FROM noticias WHERE link = ?", (link,))
        return self.cursor.fetchone() is not None
        
    def fechar(self):
        self.conn.close()
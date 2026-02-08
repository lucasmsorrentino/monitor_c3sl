import requests
from bs4 import BeautifulSoup
import hashlib
import time

class C3SLScraper:
    def __init__(self):
        self.url = "https://www.c3sl.ufpr.br/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def _gerar_hash(self, texto):
        """Cria uma assinatura única (MD5) para o texto."""
        return hashlib.md5(texto.encode('utf-8')).hexdigest()
    
    def extrair_conteudo_pagina(self, url):
        """
        Entra na página específica e pega o texto principal.
        Retorna o texto limpo e o seu Hash.
        """
        try:
            # Pausa para ser gentil com o servidor
            time.sleep(1) 
            
            print(f"   -> Acessando: {url}") # Log para você ver o progresso
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                return None, None

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Tenta encontrar o conteúdo principal.
            # No C3SL, muitas vezes fica em 'div.content' ou 'article' ou 'div.node__content'
            conteudo = soup.find('div', class_='content') or soup.find('article') or soup.find('div', class_='node__content')
            
            if not conteudo:
                # Se não achar a área específica, pega o body (menos preciso, mas funciona)
                conteudo = soup.body

            if conteudo:
                texto_limpo = conteudo.get_text(separator=' ', strip=True)
                hash_texto = self._gerar_hash(texto_limpo)
                return texto_limpo, hash_texto
            
            return None, None

        except Exception as e:
            print(f"   -> Erro ao ler página interna {url}: {e}")
            return None, None

    def obter_lista_links(self):
        """
        Acessa o site e retorna uma lista de dicionários:
        [{'titulo': '...', 'link': '...'}, ...]
        """
        try:
            print(f"Escaneando a home: {self.url}...")
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            links_encontrados = []
            # Lógica de extração: Busca todos os links que podem ser notícias
            # DICA: Ajuste o 'find_all' conforme a estrutura real do site mudar
            elementos = soup.find_all('a') # Refinar se possível

            for item in elementos:
                titulo = item.get_text().strip()
                link = item.get('href')

                # Filtros para pegar apenas notícias prováveis
                if link and titulo and len(titulo) > 15:
                    # Corrige links relativos
                    if not link.startswith('http'):
                        if link.startswith('/'):
                            link = self.url.rstrip('/') + link
                        else:
                            link = self.url.rstrip('/') + '/' + link
                        
                    links_encontrados.append({'titulo': titulo, 'link': link})
            
            return links_encontrados

        except Exception as e:
            print(f"Erro ao raspar dados: {e}")
            return []

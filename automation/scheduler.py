import schedule
import time
from database.manager import DatabaseManager
from scraper.c3sl import C3SLScraper
# Importamos o novo notificador
from notifications.telegram_sender import TelegramNotifier

class BotScheduler:
    def __init__(self):
        self.db = DatabaseManager()
        self.scraper = C3SLScraper()
        self.notifier = TelegramNotifier()

    def tarefa_verificacao(self):
        """Lógica principal executada pelo agendador."""
        print("\n--- Iniciando tarefa de verificação ---")

        lista_links = self.scraper.obter_lista_links()
        notificacoes = []

        for item in lista_links:
            link = item['link']
            titulo = item['titulo']
            
            print(f"Analisando: {titulo[:30]}...")

            # Entra na página para ler o conteúdo atual
            _, hash_atual = self.scraper.extrair_conteudo_pagina(link)
            
            if not hash_atual:
                print(" -> Erro ao ler conteúdo. Pulando.")
                continue

            # Pega o que temos no banco
            hash_salvo = self.db.obter_hash_salvo(link)

            # LÓGICA DE COMPARAÇÃO
            if hash_salvo is None:
                # Caso A: Nunca vimos esse link
                print(f" -> [NOVO POST DETECTADO]")
                self.db.salvar_ou_atualizar(titulo, link, hash_atual)
                item['tipo'] = 'NOVO POST'
                #notificacoes.append(item)
                # Prepara mensagem para o Telegram
                notificacoes.append(f"🆕 *NOVO POST:*\n[{titulo}]({link})")
            
            elif hash_atual != hash_salvo:
                # Caso B: O link existe, mas o texto mudou
                print(f" -> [CONTEÚDO ALTERADO]")
                self.db.salvar_ou_atualizar(titulo, link, hash_atual)
                item['tipo'] = 'ATUALIZAÇÃO DE TEXTO'
                # notificacoes.append(item)
                # Prepara mensagem para o Telegram
                notificacoes.append(f"🔄 *ATUALIZADO:*\n[{titulo}]({link})")
            else:
                # Caso C: Tudo igual
                pass # Não faz nada
        
        # Se houver novidades, envia para o Telegram
        if notificacoes:
            print(f"\nResumo: {len(notificacoes)} mudanças encontradas.")
            for msg in notificacoes:
                self.notifier.enviar_mensagem(msg)
        else:
            print("Nenhuma alteração encontrada.")
            self.notifier.enviar_mensagem("Nenhuma alteração encontrada.")

    def iniciar(self):
        # Define os horários (pode ser ajustado)
        # Exemplo: Rodar todo dia às 09:00 e 17:00
        schedule.every().day.at("09:00").do(self.tarefa_verificacao)
        schedule.every().day.at("17:00").do(self.tarefa_verificacao)
        
        # Para testes imediatos, descomente a linha abaixo (roda a cada 10 seg)
        #schedule.every(2).minutes.do(self.tarefa_verificacao)

        print("Bot iniciado. Aguardando horários agendados...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nParando o bot...")
            self.db.fechar()
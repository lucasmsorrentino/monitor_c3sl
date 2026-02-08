import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        if not self.token or not self.chat_id:
            print("⚠️ AVISO: Token ou Chat ID do Telegram não configurados no .env")

    def enviar_mensagem(self, mensagem):
        """Envia uma mensagem de texto simples."""
        if not self.token or not self.chat_id:
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": mensagem,
            "parse_mode": "Markdown" # Permite usar negrito, links, etc.
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Notificação enviada via Telegram!")
            else:
                print(f"❌ Erro Telegram: {response.text}")
        except Exception as e:
            print(f"❌ Erro ao conectar com Telegram: {e}")
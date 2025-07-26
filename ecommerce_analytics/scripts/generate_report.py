import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

# Variáveis do ambiente
DBT_DIR = os.getenv('DBT_DIR')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def render_report_text():
    # Carregar dados
    sales_df = pd.read_csv(f"{DBT_DIR}/seeds/orders.csv")
    produtos_df = pd.read_csv(f"{DBT_DIR}/seeds/products.csv")

    # Calcular métricas
    total_pedidos = len(sales_df)
    total_cancelados = len(sales_df[sales_df["status"] == "cancelado"])
    taxa_cancelamento = round((total_cancelados / total_pedidos) * 100, 2)
    top_produto = produtos_df.sort_values(by="price", ascending=False).iloc[0]["product_name"]

    # Formatar mensagem com Markdown
    message = (
        "📊 *Relatório Semanal - E-commerce*\n\n"
        f"• Total de pedidos: *{total_pedidos}*\n"
        f"• Pedidos cancelados: *{total_cancelados}*\n"
        f"• Taxa de cancelamento: *{taxa_cancelamento}%*\n"
        f"• Produto mais caro: *{top_produto}*\n"
    )
    return message

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Erro ao enviar mensagem: {response.text}")
        response.raise_for_status()
    else:
        print("Mensagem enviada com sucesso!")

def notify_weekly_report_telegram():
    message = render_report_text()
    send_telegram_message(message)

if __name__ == "__main__":
    notify_weekly_report_telegram()

import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do env
load_dotenv()

#criando instancia do faker
fake = Faker()
random.seed(42) # para garantir reprodutibilidade

# Buscar as variaveis do env
N_CUSTOMERS = int(os.getenv("N_CUSTOMERS"))
N_PRODUCTS = int(os.getenv("N_PRODUCTS"))
N_ORDERS = int(os.getenv("N_ORDERS"))
output_dir_path = os.getenv("OUTPUT_DIR")

output_dir = Path(output_dir_path)
output_dir.mkdir(parents=True, exist_ok=True) # cria pasta, se ela existir ignora erro

# -------------- 1. CLIENTES -------------------
customers = []

for i in range (1, N_CUSTOMERS + 1):
    customers.append({
        "customer_id": i,
        "name": fake.name(),
        "email": fake.email(),
        "signup_date": fake.date_between(start_date="-2y", end_date="today")
    })

df_customers = pd.DataFrame(customers)
df_customers.to_csv(output_dir/"customers.csv",index=False)

# ------------- 2. PRODUTOS -------------------
categories = ["Eletrônicos", "Roupas", "Beleza", "Livros", "Casa", "Esporte"]

products = []
for i in range(1, N_PRODUCTS +1):
    categoria = random.choice(categories)
    custo = round(random.uniform(5, 100), 2)
    preco = round(custo * random.uniform(1.2, 2.5), 2)
    products.append({
        "product_id": i,
        "product_name": fake.word().capitalize() + " " + fake.word().capitalize(),
        "category": categoria,
        "custo": custo,
        "price": preco
    })
df_products = pd.DataFrame(products)
df_products.to_csv(output_dir/"products.csv",index=False)

# ---------- 3. PEDIDOS E ITENS ----------
orders = []
order_items = []
for i in range(1, N_ORDERS + 1):
    customer_id = random.randint(1, N_CUSTOMERS)
    order_date = fake.date_between(start_date="-1y", end_date="today")
    status = random.choices(["completo", "cancelado"], weights=[0.85, 0.15])[0]

    orders.append({
        "order_id": i,
        "customer_id": customer_id,
        "order_date": order_date,
        "status": status 
    })

    n_items = random.randint(1, 4)
    for _ in range(n_items):
        product_id = random.randint(1, N_PRODUCTS)
        quantity = random.randint(1, 3)
        order_items.append({
            "order_id": i,
            "product_id": product_id,
            "quantity": quantity            
        })

df_orders = pd.DataFrame(orders)
df_orders.to_csv(output_dir / "orders.csv", index=False)

df_order_items = pd.DataFrame(order_items)
df_order_items.to_csv(output_dir / "order_items.csv", index=False)

# ---------- 4. CANCELAMENTOS ----------
cancelamentos = df_orders[df_orders["status"]== "cancelado"].copy()
cancelamentos["cancel_reason"] = [fake.sentence(nb_words=4) for _ in range(len(cancelamentos))]
cancelamentos["cancel_date"] =  cancelamentos["order_date"].apply(lambda d: d + timedelta(days=random.randint(1, 3)))

df_canc = cancelamentos[["order_id", "cancel_reason", "cancel_date"]]
df_canc.to_csv(output_dir / "cancelamentos.csv", index=False)

print("✅ Dados gerados em:", output_dir.resolve())
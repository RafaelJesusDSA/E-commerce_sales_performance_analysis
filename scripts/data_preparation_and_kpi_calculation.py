# -*- coding: utf-8 -*-
"""
Script para carregar, preparar e calcular KPIs de desempenho de vendas de e-commerce.
Autor: Rafael
Data: 10 de julho de 2025
"""

import pandas as pd
import os

# --- 0. Configuração de Caminho ---
# Caminho EXATO para a pasta 'data' onde os arquivos CSV brutos estão salvos.
# Este caminho foi confirmado por você e está ajustado para lidar com espaços.
data_path = r'C:\Users\rafae\OneDrive\Área de Trabalho\Documentos Gerais\MBA\DSA\Projetos\Projeto Analise Desempenho Vendas e-commerce\e-commerce_sales_performance_analysis\data'

# Definindo os caminhos completos para cada arquivo CSV
orders_file = os.path.join(data_path, 'olist_orders_dataset.csv')
order_items_file = os.path.join(data_path, 'olist_order_items_dataset.csv')
customers_file = os.path.join(data_path, 'olist_customers_dataset.csv')

# --- 1. Carregamento dos Datasets ---
try:
    print("Iniciando o carregamento dos datasets...")
    # Verifica se os arquivos existem antes de tentar ler. Isso evita o 'NameError'.
    if not os.path.exists(orders_file):
        raise FileNotFoundError(f"Arquivo 'olist_orders_dataset.csv' não encontrado. Caminho verificado: {orders_file}")
    if not os.path.exists(order_items_file):
        raise FileNotFoundError(f"Arquivo 'olist_order_items_dataset.csv' não encontrado. Caminho verificado: {order_items_file}")
    if not os.path.exists(customers_file):
        raise FileNotFoundError(f"Arquivo 'olist_customers_dataset.csv' não encontrado. Caminho verificado: {customers_file}")

    orders_df = pd.read_csv(orders_file)
    order_items_df = pd.read_csv(order_items_file)
    customers_df = pd.read_csv(customers_file)
    
    print("Datasets carregados com sucesso!")
    print(f"orders_df carregado com {orders_df.shape[0]} linhas.")
    print(f"order_items_df carregado com {order_items_df.shape[0]} linhas.")
    print(f"customers_df carregado com {customers_df.shape[0]} linhas.")
    
except FileNotFoundError as e:
    print(f"ERRO CRÍTICO: {e}")
    print("Por favor, verifique se todos os arquivos CSV originais estão na pasta 'data' e se o caminho 'data_path' no script está correto.")
    print("A execução será interrompida.")
    exit() # Interrompe o script se os arquivos não forem encontrados
except Exception as e:
    print(f"OCORREU UM ERRO INESPERADO DURANTE O CARREGAMENTO DOS DADOS: {e}")
    print("A execução será interrompida.")
    exit() # Interrompe o script em caso de outros erros


# --- 2. Pré-processamento de Dados ---
print("\nIniciando o pré-processamento dos dados...")

# 2.1. Conversão de Colunas de Data para datetime
date_columns = [
    'order_purchase_timestamp', 'order_approved_at', 
    'order_delivered_carrier_date', 'order_delivered_customer_date', 
    'order_estimated_delivery_date'
]
for col in date_columns:
    if col in orders_df.columns:
        orders_df[col] = pd.to_datetime(orders_df[col], errors='coerce') # 'coerce' transforma valores inválidos em NaT (Not a Time)
    else:
        print(f"Aviso: Coluna de data '{col}' não encontrada em orders_df.")

print("Colunas de data convertidas para datetime.")

# 2.2. Filtragem de Pedidos 'delivered'
# Focamos em pedidos entregues para ter uma base sólida para cálculos de receita.
orders_delivered_df = orders_df[orders_df['order_status'] == 'delivered'].copy()
print(f"Pedidos filtrados: {orders_delivered_df.shape[0]} pedidos com status 'delivered'.")

# 2.3. União (Merge) dos DataFrames
# Juntando pedidos entregues com os itens desses pedidos
df_merged = pd.merge(orders_delivered_df, order_items_df, on='order_id', how='inner')
print(f"Orders e Order Items unidos. Shape: {df_merged.shape}")

# Juntando o resultado com as informações dos clientes
df_final = pd.merge(df_merged, customers_df, on='customer_id', how='inner')
print(f"DataFrame final criado (com informações de clientes). Shape: {df_final.shape}")

# 2.4. Cálculo da Receita por Item
# A receita de um item é a soma do preço do item e o valor do frete.
df_final['item_revenue'] = df_final['price'] + df_final['freight_value']
print("Coluna 'item_revenue' adicionada (preço do item + valor do frete).")

# 2.5. Conversão da data limite de envio no df_final (para validações futuras se necessário)
if 'shipping_limit_date' in df_final.columns:
    df_final['shipping_limit_date'] = pd.to_datetime(df_final['shipping_limit_date'], errors='coerce')
else:
    print("Aviso: Coluna 'shipping_limit_date' não encontrada no DataFrame final.")

print("\nPré-processamento de dados concluído com sucesso.")
print("\nPrimeiras 5 linhas do DataFrame final:")
print(df_final.head())
print("\nInformações do DataFrame final (df_final.info()):")
df_final.info()


# --- 3. Verificação de Exemplos de 'item_revenue' (Validação dos Dados) ---
print("\n--- Verificação de Exemplos de Item Revenue ---")

# Exemplo 1: Verificando um item específico
target_date_str_1 = '2017-10-23 17:14:35'
target_order_id_1 = '3480c6733692db0895d7f240dc18d9d6'
target_product_id_1 = '511565b2987c19e165331306886f10f8'

found_item_1 = df_final[
    (df_final['order_id'] == target_order_id_1) &
    (df_final['product_id'] == target_product_id_1) &
    (df_final['shipping_limit_date'] == pd.to_datetime(target_date_str_1))
]

if not found_item_1.empty:
    print(f"\nExemplo 1 (Order ID: {target_order_id_1}):")
    print(f"  Item Revenue: R$ {found_item_1['item_revenue'].iloc[0]:.2f}")
    print(f"  Preço (price): R$ {found_item_1['price'].iloc[0]:.2f}")
    print(f"  Frete (freight_value): R$ {found_item_1['freight_value'].iloc[0]:.2f}")
else:
    print(f"\nExemplo 1 (Order ID: {target_order_id_1}): Item não encontrado no DataFrame final. Verifique os IDs ou datas.")

# Exemplo 2: Outro item para validação
target_date_str_2 = '2017-10-13 04:05:54'
target_order_id_2 = 'c301f64860cec992f8d9c532fb00f867'
target_product_id_2 = '7cd7d781203890be0d18accf75bd90d5'

found_item_2 = df_final[
    (df_final['order_id'] == target_order_id_2) &
    (df_final['product_id'] == target_product_id_2) &
    (df_final['shipping_limit_date'] == pd.to_datetime(target_date_str_2))
]

if not found_item_2.empty:
    print(f"\nExemplo 2 (Order ID: {target_order_id_2}):")
    print(f"  Item Revenue: R$ {found_item_2['item_revenue'].iloc[0]:.2f}")
    print(f"  Preço (price): R$ {found_item_2['price'].iloc[0]:.2f}")
    print(f"  Frete (freight_value): R$ {found_item_2['freight_value'].iloc[0]:.2f}")
else:
    print(f"\nExemplo 2 (Order ID: {target_order_id_2}): Item não encontrado no DataFrame final. Verifique os IDs ou datas.")


# --- 4. Cálculo dos KPIs (Key Performance Indicators) ---
print("\n--- Cálculo dos KPIs ---")

total_revenue = df_final['item_revenue'].sum()
total_orders = df_final['order_id'].nunique()
# Prevenção de divisão por zero para Ticket Médio
average_order_value = total_revenue / total_orders if total_orders > 0 else 0
unique_customers = df_final['customer_unique_id'].nunique()

print(f"KPI 1: Receita Total = R$ {total_revenue:,.2f}")
print(f"KPI 2: Número Total de Pedidos = {total_orders}")
print(f"KPI 3: Ticket Médio = R$ {average_order_value:,.2f}")
print(f"KPI 4: Número de Clientes Únicos = {unique_customers}")

# Opcional: Criar um DataFrame de KPIs para fácil visualização ou exportação
kpis_summary = pd.DataFrame({
    'KPI': ['Receita Total', 'Número Total de Pedidos', 'Ticket Médio', 'Número de Clientes Únicos'],
    'Valor': [total_revenue, total_orders, average_order_value, unique_customers]
})
print("\n--- Resumo dos KPIs ---")
print(kpis_summary.round(2)) # Arredondando para 2 casas decimais para melhor visualização


# --- 5. Exportação do DataFrame Final Processado ---
output_file_name = 'e-commerce_data_processed.csv'
output_path_full = os.path.join(data_path, output_file_name) # Cria o caminho completo para o arquivo de saída

try:
    df_final.to_csv(output_path_full, index=False)
    print(f"\nDataFrame final exportado com sucesso para: {output_path_full}")
    print("Você pode carregar este arquivo no Power BI.")
except Exception as e:
    print(f"ERRO AO EXPORTAR O CSV: {e}")
    print(f"Por favor, verifique permissões de escrita ou se o caminho de saída está acessível: {output_path_full}")

print("\nProcessamento de dados e cálculo de KPIs concluídos.")
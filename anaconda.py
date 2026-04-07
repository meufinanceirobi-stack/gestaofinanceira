import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Carregar dados existentes do arquivo CSV se ele existir
def carregar_dados():
    if os.path.exists('vendas.csv'):
        return pd.read_csv('vendas.csv')
    else:
        return pd.DataFrame(columns=['Data', 'Produto', 'Quantidade', 'Valor Unitário', 'Total'])

# Salvar dados no arquivo CSV
def salvar_dados(df):
    df.to_csv('vendas.csv', index=False)

# Inicializar dados
df = carregar_dados()

# Título do app
st.title('Sistema de Registro de Vendas')

# Formulário para registrar venda
st.header('Registrar Nova Venda')
with st.form('form_venda'):
    data = st.date_input('Data')
    produto = st.text_input('Produto')
    quantidade = st.number_input('Quantidade', min_value=1, step=1)
    valor_unitario = st.number_input('Valor Unitário', min_value=0.0, step=0.01)
    total = quantidade * valor_unitario
    st.write(f'Total: R$ {total:.2f}')
    submitted = st.form_submit_button('Registrar Venda')
    if submitted:
        nova_venda = pd.DataFrame({
            'Data': [data],
            'Produto': [produto],
            'Quantidade': [quantidade],
            'Valor Unitário': [valor_unitario],
            'Total': [total]
        })
        df = pd.concat([df, nova_venda], ignore_index=True)
        salvar_dados(df)
        st.success('Venda registrada com sucesso!')

# Dashboard
st.header('Dashboard de Vendas')

# Tabela de vendas
st.subheader('Tabela de Vendas')
st.dataframe(df)

# Métricas
if not df.empty:
    total_vendas = df['Total'].sum()
    num_registros = len(df)
    media_vendas = df['Total'].mean()
    col1, col2, col3 = st.columns(3)
    col1.metric('Total de Vendas', f'R$ {total_vendas:.2f}')
    col2.metric('Número de Registros', num_registros)
    col3.metric('Vendas Média', f'R$ {media_vendas:.2f}')

    # Gráfico de barras: Vendas por Produto
    st.subheader('Vendas por Produto')
    vendas_por_produto = df.groupby('Produto')['Total'].sum().reset_index()
    st.bar_chart(vendas_por_produto.set_index('Produto'))

    # Gráfico de linha: Vendas ao longo do tempo
    st.subheader('Vendas ao Longo do Tempo')
    df['Data'] = pd.to_datetime(df['Data'])
    vendas_por_data = df.groupby('Data')['Total'].sum().reset_index()
    st.line_chart(vendas_por_data.set_index('Data'))
else:
    st.write('Nenhuma venda registrada ainda.')

# Botão para limpar dados
if st.button('Limpar Todos os Dados'):
    if os.path.exists('vendas.csv'):
        os.remove('vendas.csv')
    df = pd.DataFrame(columns=['Data', 'Produto', 'Quantidade', 'Valor Unitário', 'Total'])
    st.success('Dados limpos com sucesso!')
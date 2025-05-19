import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc

# Dados
df = pd.read_csv(r'C:\Users\OQUARTO\Documents\ecommerce\ecommerce_estatistica.csv')

# Limpeza do Gênero
df['Gênero_Limpo'] = df['Gênero'].str.strip().str.lower()
genero_map = {
    'masculino': 'Masculino',
    'feminino': 'Feminino',
    'bebês': 'Unissex',
    'meninos': 'Masculino',
    'meninas': 'Feminino',
    'roupa para gordinha pluss p ao 52': 'Feminino',
    'sem gênero': 'Unissex',
    'sem gênero infantil': 'Unissex',
    'unissex': 'Unissex'
}
df['Gênero_Limpo'] = df['Gênero_Limpo'].replace(genero_map)

# Gráfico 1 - Histograma Top 10 notas (entre 4 e 5)
top10_notas = df[df['Nota'].between(4, 5)].sort_values(by='Nota', ascending=False).head(10)
fig_hist = px.bar(
    top10_notas.sort_values(by='Nota'),
    x='Nota',
    y='Título',
    orientation='h',
    title='Top 10 Produtos com Maiores Notas (entre 4 e 5)'
)

# Gráfico 2 - Dispersão: Avaliações vs Nota
fig_disp = px.scatter(
    df,
    x='N_Avaliações',
    y='Nota',
    title='Nota vs Número de Avaliações'
)

# Gráfico 3 - Mapa de Calor
cols = ['Nota', 'N_Avaliações', 'Desconto', 'Preço_MinMax', 'Qtd_Vendidos_Cod']
fig_heatmap = px.imshow(df[cols].corr(), text_auto=True, title='Mapa de Calor')

# Gráfico 4 - Barras: Top 10 Marcas por Vendas
top_marcas = df.groupby('Marca')['Qtd_Vendidos_Cod'].sum().sort_values(ascending=False).head(10)
fig_barras = px.bar(
    top_marcas,
    x=top_marcas.index,
    y=top_marcas.values,
    title='Top 10 Marcas por Quantidade Vendida',
    labels={'x': 'Marca', 'y': 'Qtd Vendidos'}
)

# Gráfico 5 - Pizza por Gênero
fig_pizza = px.pie(
    df,
    names='Gênero_Limpo',
    title='Distribuição de Produtos por Gênero'
)

# Gráfico 6 - Densidade das Notas
notas = pd.to_numeric(df['Nota'], errors='coerce').dropna()
fig_densidade = go.Figure()
fig_densidade.add_trace(go.Histogram(x=notas, histnorm='probability density'))
fig_densidade.update_layout(title='Densidade das Notas dos Produtos', xaxis_title='Nota')

# Gráfico 7 - Regressão: Preço vs Vendas
fig_reg = px.scatter(
    df,
    x='Preço_MinMax',
    y='Qtd_Vendidos_Cod',
    trendline='ols',
    title='Preço vs Quantidade Vendida'
)

# App
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Análise E-commerce', style={'textAlign': 'center'}),

    dcc.Graph(figure=fig_hist),
    dcc.Graph(figure=fig_disp),
    dcc.Graph(figure=fig_heatmap),
    dcc.Graph(figure=fig_barras),
    dcc.Graph(figure=fig_pizza),
    dcc.Graph(figure=fig_densidade),
    dcc.Graph(figure=fig_reg)
])

if __name__ == '__main__':
    app.run(debug=True)


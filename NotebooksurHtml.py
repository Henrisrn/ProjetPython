# %%
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#EXCELS OU TU PEUX RENTRER DEPENSE OU REVENUE
depense = pd.read_csv("export-operations-10-05-2023_14-04-34.csv", sep=';')
revenue = pd.read_csv("export-operations-10-05-2023_14-04-48.csv", sep=';')
print(depense)
 

# %%
depense['dateOp'] = pd.to_datetime(depense['dateOp'], format="%d/%m/%Y")
print(depense['amount'].dtypes)
#depense['amount'] = depense['amount'].str.replace(',', '.').astype(float)
depense['amount'] = depense['amount'].astype(str).str.replace(',', '.').astype(float)

monthly_data = depense.groupby(depense['dateOp'].dt.to_period('M')).sum(numeric_only=True).reset_index()
monthly_data['dateOp'] = monthly_data['dateOp'].apply(lambda x: x.to_timestamp())


fig1 = px.line(monthly_data, x='dateOp', y='amount', title='Dépenses mensuelles totales')
#fig1.show()

# %%
revenue['dateOp'] = pd.to_datetime(revenue['dateOp'], format="%d/%m/%Y")
print(revenue['amount'].dtypes)
#depense['amount'] = depense['amount'].str.replace(',', '.').astype(float)
revenue['amount'] = revenue['amount'].astype(str).str.replace(',', '.').astype(float)

monthly_data = revenue.groupby(revenue['dateOp'].dt.to_period('M')).sum(numeric_only=True).reset_index()
monthly_data['dateOp'] = monthly_data['dateOp'].apply(lambda x: x.to_timestamp())


fig2 = px.line(monthly_data, x='dateOp', y='amount', title='Dépenses mensuelles totales')
#fig2.show()

# %%
cat_parent_data = revenue.groupby('categoryParent').sum(numeric_only=True).reset_index()
fig3 = px.pie(cat_parent_data, values='amount', names='categoryParent', title='Dépenses par catégorie parent')
#fig3.show()


# %%
evol_data = depense.groupby([depense['dateOp'], 'categoryParent']).sum(numeric_only=True).reset_index()
fig4 = px.line(evol_data, x='dateOp', y='amount', color='categoryParent', title="Évolution des dépenses par catégorie parent")
#fig4.show()


# %%
evol_data = revenue.groupby([depense['dateOp'], 'categoryParent']).sum(numeric_only=True).reset_index()
fig5 = px.line(evol_data, x='dateOp', y='amount', color='categoryParent', title="Évolution des dépenses par catégorie parent")
#fig5.show()


# %%
top_suppliers = depense.groupby('supplierFound').sum(numeric_only=True).sort_values(by='amount', ascending=False).head(10).reset_index()
fig6 = px.bar(top_suppliers, x='supplierFound', y='amount', title='Top 10 des fournisseurs par dépenses')
#fig6.show()


# %%
top_suppliers = revenue.groupby('supplierFound').sum(numeric_only=True).sort_values(by='amount', ascending=False).head(10).reset_index()
fig7 = px.bar(top_suppliers, x='supplierFound', y='amount', title='Top 10 des fournisseurs par revenue')
#fig7.show()


# %%
weekday_data = depense.groupby(depense['dateOp'].dt.dayofweek).sum(numeric_only=True).reset_index()
weekday_data['dateOp'] = weekday_data['dateOp'].apply(lambda x: pd.Timestamp(x, unit='D').day_name(locale='French'))
fig8 = px.bar(weekday_data, x='dateOp', y='amount', title='Répartition des dépenses par jour de la semaine', labels={'dateOp': 'Jour de la semaine'})
#fig8.show()

# %%
weekday_data = revenue.groupby(revenue['dateOp'].dt.dayofweek).sum(numeric_only=True).reset_index()
weekday_data['dateOp'] = weekday_data['dateOp'].apply(lambda x: pd.Timestamp(x, unit='D').day_name(locale='French'))
fig9 = px.bar(weekday_data, x='dateOp', y='amount', title='Répartition des dépenses par jour de la semaine', labels={'dateOp': 'Jour de la semaine'})
#fig9.show()

# %%
monthly_data = depense.groupby(depense['dateOp'].dt.to_period('M')).sum(numeric_only=True).reset_index()
monthly_data['dateOp'] = monthly_data['dateOp'].apply(lambda x: x.to_timestamp().strftime('%B %Y'))
fig10 = px.line(monthly_data, x='dateOp', y='amount', title='Dépenses mensuelles totales')
#fig10.show()

# %%
monthly_data = revenue.groupby(revenue['dateOp'].dt.to_period('M')).sum(numeric_only=True).reset_index()
monthly_data['dateOp'] = monthly_data['dateOp'].apply(lambda x: x.to_timestamp().strftime('%B %Y'))
fig11 = px.line(monthly_data, x='dateOp', y='amount', title='Dépenses mensuelles totales')
#fig11.show()

# %%
yearly_data = depense.groupby(depense['dateOp'].dt.to_period('Y')).sum(numeric_only=True).reset_index()
yearly_data['dateOp'] = yearly_data['dateOp'].apply(lambda x: x.to_timestamp().strftime('%Y'))
fig12 = px.bar(yearly_data, x='dateOp', y='amount', title='Dépenses annuelles totales')
#fig12.show()

# %%
yearly_data = revenue.groupby(revenue['dateOp'].dt.to_period('Y')).sum(numeric_only=True).reset_index()
yearly_data['dateOp'] = yearly_data['dateOp'].apply(lambda x: x.to_timestamp().strftime('%Y'))
fig13 = px.bar(yearly_data, x='dateOp', y='amount', title='Dépenses annuelles totales')
#fig13.show()

# %%
heatmap_data = depense.groupby([depense['dateOp'], 'category']).sum(numeric_only=True).reset_index()
fig14 = px.density_heatmap(heatmap_data, x='dateOp', y='category', z='amount', nbinsx=20, title='Dépenses par catégorie et par mois')
#fig14.show()


# %%
heatmap_data = revenue.groupby([revenue['dateOp'], 'category']).sum(numeric_only=True).reset_index()
fig15 = px.density_heatmap(heatmap_data, x='dateOp', y='category', z='amount', nbinsx=20, title='Dépenses par catégorie et par mois')
#fig15.show()


# %%
revenue_monthly_type = revenue.groupby([revenue['dateOp'].dt.to_period('M'), 'category']).sum(numeric_only=True).reset_index()
revenue_monthly_type['dateOp'] = revenue_monthly_type['dateOp'].apply(lambda x: x.to_timestamp().strftime('%B %Y'))
fig16 = px.bar(revenue_monthly_type, x='dateOp', y='amount', color='category', title='Montant des revenus par mois et par type de revenus')
#fig16.show()

# %%
revenue_monthly_type = depense.groupby([depense['dateOp'].dt.to_period('M'), 'category']).sum(numeric_only=True).reset_index()
revenue_monthly_type['dateOp'] = revenue_monthly_type['dateOp'].apply(lambda x: x.to_timestamp().strftime('%B %Y'))
fig17 = px.bar(revenue_monthly_type, x='dateOp', y='amount', color='category', title='Montant des depenses par mois et par type de revenus')
#fig17.show()

# %%
revenue_by_supplier = revenue.groupby('supplierFound').sum(numeric_only=True).reset_index()
fig18 = px.pie(revenue_by_supplier, values='amount', names='supplierFound', title='Répartition des revenus par fournisseur')
#fig18.show()

# %%
revenue['weekday'] = revenue['dateOp'].dt.day_name()
revenue_weekday = revenue.groupby('weekday').sum(numeric_only=True).reset_index()
fig19 = px.bar(revenue_weekday, x='weekday', y='amount', title='Montant des revenus par jour de la semaine')
#fig19.show()

# %%
revenue['dateOp'] = pd.to_datetime(revenue['dateOp'], format="%d/%m/%Y")
revenue_cumulative = revenue.groupby(['dateOp', 'category']).sum(numeric_only=True).groupby('category').cumsum().reset_index()
fig20 = px.line(revenue_cumulative, x='dateOp', y='amount', color='category', title='Montant cumulé des revenus par type de revenus au fil du temps')
#fig20.show()

# %%
depense['dateOp'] = pd.to_datetime(depense['dateOp'], format="%d/%m/%Y")
revenue_cumulative = depense.groupby(['dateOp', 'category']).sum(numeric_only=True).groupby('category').cumsum().reset_index()
fig21 = px.line(revenue_cumulative, x='dateOp', y='amount', color='category', title='Montant cumulé des depenses par type de revenus au fil du temps')
#fig21.show()

# %%
revenue_account_category = revenue.groupby(['accountLabel', 'category']).sum(numeric_only=True).reset_index()
fig22 = px.bar(revenue_account_category, x='accountLabel', y='amount', color='category', title='Montant des revenus par type de revenus et par compte bancaire')
#fig22.show()

# %%
revenue_account_category = depense.groupby(['accountLabel', 'category']).sum(numeric_only=True).reset_index()
fig23 = px.bar(revenue_account_category, x='accountLabel', y='amount', color='category', title='Montant des depenses par type de revenus et par compte bancaire')
#fig23.show()


app = dash.Dash(__name__)
server = app.server

app.layout = dbc.Container([
    dbc.Row([
    dcc.Graph(id='graph1', figure=fig1),
    dcc.Graph(id='graph2', figure=fig2),
    ]),
    dbc.Row([
    dcc.Graph(id='graph3', figure=fig3),
    dcc.Graph(id='graph4', figure=fig4),
    ]),
    dbc.Row([
    dcc.Graph(id='graph5', figure=fig5),
    dcc.Graph(id='graph6', figure=fig6),
    ]),
    dbc.Row([
    dcc.Graph(id='graph7', figure=fig7),
    dcc.Graph(id='graph8', figure=fig8),
    ]),
    dbc.Row([
    dcc.Graph(id='graph9', figure=fig9),
    dcc.Graph(id='graph10', figure=fig10),
    ]),
    dbc.Row([
    dcc.Graph(id='graph11', figure=fig11),
    dcc.Graph(id='graph12', figure=fig12),
    ]),
    dbc.Row([
    dcc.Graph(id='graph13', figure=fig13),
    dcc.Graph(id='graph14', figure=fig14),
    ]),
    dbc.Row([
    dcc.Graph(id='graph15', figure=fig15),
    dcc.Graph(id='graph16', figure=fig16),
    ]),
    dbc.Row([
    dcc.Graph(id='graph17', figure=fig17),
    dcc.Graph(id='graph18', figure=fig18),
    ]),
    dbc.Row([
    dcc.Graph(id='graph19', figure=fig19),
    dcc.Graph(id='graph20', figure=fig20),
    ]),
    dbc.Row([
    dcc.Graph(id='graph21', figure=fig21),
    dcc.Graph(id='graph22', figure=fig22),
    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)

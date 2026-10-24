import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image



caminho_rec = 'recebiveis.xlsx'
caminho_desp = 'despesas.xlsx'
df_recebiveis = pd.read_excel(caminho_rec)
df_despesas = pd.read_excel(caminho_desp)


pd.set_option('display.max_columns', None)
pd.set_option('display.float_format','{:.2f}'.format)

#PAGE CONFIG
st.set_page_config(layout='wide')


st.markdown("""<style>
                .stApp{
                    background-color: #F4F4F4;
                }
                .stMultiSelect > div > div {
                    background-color: #E8E8E8;
                    color: #5C6354;
                    border: 1px solid #D4D4D4;
                }
                .stMultiSelect > div > div > div {
                    color: #5C6354;
                    border: 1px solid #D4D4D4;
                }
                [data-testid="stPlotlyChart"] {
                    border-radius: 15px;
                    overflow: hidden;
                    border: 1px solid #D9DDD5;
                    }    
                </style>
                """, unsafe_allow_html=True)


df_recebiveis['data']= pd.to_datetime(df_recebiveis['data'])
df_recebiveis['ano']= df_recebiveis['data'].dt.year
df_recebiveis['mes']= df_recebiveis['data'].dt.month_name()
df_recebiveis['quantidade']= df_recebiveis['quantidade'].astype('Int64')
df_recebiveis['forma_pgt'] = df_recebiveis['forma_pgt'].fillna('nao informado')
df_recebiveis = df_recebiveis.fillna({
    'quantidade':0,
    'valor':0,
    'pg_parcerias':0 })


df_despesas['data']= pd.to_datetime(df_despesas['data'])
df_despesas['ano']= df_despesas['data'].dt.year
df_despesas['mes']= df_despesas['data'].dt.month_name()
df_despesas['quantidade']= df_despesas['quantidade'].astype('Int64')
df_despesas = df_despesas.fillna({
    'forma_pgt':'nao informado',
    'observacao':'nao informado',
    'quantidade': 0,
    'valor': 0
})

ordem_mes = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']



col_logo, col_titulo = st.columns([1,6])
with col_logo:
    logo = Image.open('cv_vidal.jpg')
    st.image(logo, width=200)
with col_titulo:
    st.markdown('<h1 style="color: #5C6354; font-family: Aptos; margin-top: 40px; ">Financeiro - Mimos da Gih</h1>', unsafe_allow_html=True)

#FILTROS
fil1, fil2 = st.columns([2,2])

with fil1:
    fil_ano = st.multiselect('',sorted(df_recebiveis['ano'].unique()),
                            default=sorted(df_recebiveis['ano'].unique()))
with fil2:
    fil_mes = st.multiselect('', sorted(df_recebiveis['mes'].unique()),
                             default=sorted(df_recebiveis['mes'].unique()))   


df_filtro_recebiveis = df_recebiveis[(df_recebiveis['ano'].isin(fil_ano))&
                                    (df_recebiveis['mes'].isin(fil_mes))].copy()

df_filtro_despesas = df_despesas[(df_despesas['ano'].isin(fil_ano))&
                                 (df_despesas['mes'].isin(fil_mes))].copy()
                                    

#DATA FRAME
valor_total = df_filtro_recebiveis['valor'].sum()
qtd_dias = df_filtro_recebiveis['data'].count()


df_recebiveis_anual = df_filtro_recebiveis.groupby('ano')['valor'].sum().reset_index()
graf_anual = px.bar(df_recebiveis_anual, x='ano',y='valor',text='valor')
graf_anual.update_traces(textposition='outside')


df_recebiveis_mensal = df_filtro_recebiveis.groupby(['ano','mes'])['valor'].sum().reset_index()
df_recebiveis_mensal['mes']=pd.Categorical(df_recebiveis_mensal['mes'],categories=ordem_mes,ordered=True)
df_recebiveis_mensal=df_recebiveis_mensal.sort_values('mes')

graf_mensal = px.bar(df_recebiveis_mensal,x='ano', y='valor',color='mes', barmode='group',text='valor',title='Recebíveis por mês')
graf_mensal.update_traces(textposition = 'outside')
graf_mensal.update_layout(xaxis_title='Ano', yaxis_title='Valor', paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    title_font=dict(color='#5C6354'),
    margin=dict(l=60, r=60))

df_recebiveis_desc = (df_filtro_recebiveis.groupby('descricao_produto').agg(
    quantidade= ('quantidade','sum'),
    valor= ('valor','sum'),
    pg_parcerias= ('pg_parcerias','sum')       
)).reset_index()

#DESPESAS
valor_desp_total = df_filtro_despesas['valor'].sum()
qtd_desp_dias = df_filtro_despesas['data'].count()

df_despesas_anual= df_filtro_despesas.groupby('ano')['valor'].sum().reset_index()
graf_desp_anual = px.bar(df_despesas_anual, x='ano',y='valor', text='valor')
graf_desp_anual.update_traces(textposition='outside')

df_despesas_mensal = df_filtro_despesas.groupby(['ano','mes'])['valor'].sum().reset_index()
df_despesas_mensal['mes']=pd.Categorical(df_despesas_mensal['mes'],categories=ordem_mes,ordered=True)
df_despesas_mensal=df_despesas_mensal.sort_values('mes')

graf_desp_mensal = px.bar(df_despesas_mensal,x='ano', y='valor',color='mes', barmode='group', text='valor',title='Despesas por mês')
graf_desp_mensal.update_traces(textposition = 'outside')
graf_desp_mensal.update_layout(xaxis_title='Ano', yaxis_title='Valor', paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    title_font=dict(color='#5C6354'),
    margin=dict(l=60, r=60))

df_despesas_desc= (df_filtro_despesas.groupby('descricao_pgt').agg(
    quantidade= ('quantidade','sum'),
    valor= ('valor','sum')   
)).reset_index()



#RECEBIVEIS
col1, col2, col3, col4 = st.columns([3,2,3,2])

col1.metric('Valor Total',valor_total)
col2.metric('Qtd dias',qtd_dias)
col3.metric('Valor despesas',valor_desp_total)
col4.metric('Despesa dias',qtd_desp_dias)

col5, col6 = st.columns([2,2])

with col5:
    st.plotly_chart(graf_anual)

with col6:
    st.plotly_chart(graf_mensal)


#DESPESAS

col7, col8 = st.columns([2,2])

with col7:
    st.plotly_chart(graf_desp_anual,key='graf_desp_anual')

with col8:
    st.plotly_chart(graf_desp_mensal,key='graf_desp_mensal')

st.markdown('<h2 style="color: #5C6354; font-family: Aptos; margin-top: 40px; ">Produtos</h2>', unsafe_allow_html=True)
st.dataframe(df_recebiveis_desc)

st.markdown('<h2 style="color: #5C6354; font-family: Aptos; margin-top: 40px; ">Descrição despesas</h2>', unsafe_allow_html=True)
st.dataframe(df_despesas_desc)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 14:39:46 2021

@author: Marco de la Cruz
"""

#Importamos paqueterías y datasets
import pandas as pd
import numpy as np
#import random
import matplotlib.pyplot as plt
from matplotlib import ticker
import scipy.stats as st

df_prob = pd.read_excel('Probabilities.xlsx', sheet_name='Hoja1')
df_buy = pd.read_excel('Buying price.xlsx', sheet_name='Hoja1')
df_sell = pd.read_excel('Aggregators prices.xlsx', sheet_name='Hoja1')

#Creamos una función acumulada en df_prob, primero haciendo una lista de ceros
#df_prob['Accumulated'] = np.zeros(len(df_prob))
#df_prob['Accumulated'] = np.cumsum(df_prob['Probability'])

#Creamos una lista vacía con los 200 totales y una sublista para cada simulación
simulations = 200
sell_1 = 0.60 #Equipos vendidos al mejor precio
sell_2 = 0.30 #Equipos vendidos al segundo mejor precio
sell_3 = 0.10 #Equipos vendidos al tercer mejor precio


subtotal= pd.DataFrame({
    'Pieces': np.zeros(simulations),
    'Buying': np.zeros(simulations),
    'Selling': np.zeros(simulations),
    'Margin': np.zeros(simulations)
    })
subsubtotal = pd.DataFrame({
    'Model': np.zeros(700),
    'Buying': np.zeros(700),
    'Selling': np.zeros(700),
    'Margin': np.zeros(700)
    })

#Juntamos df_buy y df_sell en un solo data set creando una columna que se pueda relacionar
df_buy['union']= df_buy['Device name'] + " " + df_buy['Grading']
df_sell['union']= df_sell['Model'] + " " + df_sell['Grade']
df = pd.merge(df_buy, df_sell, how='left', on='union')

#Definimos la primera simulación de equipos recibidos con una distribución Beta(4,5)
for i in range(0, len(subtotal)):
    np.random.seed(df_prob.index[i]*100)
    subtotal['Pieces'].loc[i] = np.round(st.beta(4, 5, loc=400, scale=200).rvs(),
                                         decimals = 0)

#Determinamos el modelo y grading que recibiremos en las doscientas simulaciones
#Para determinar el modelo y grading usaremos el df que creamos de buy y sell
for i in range(0, len(subtotal)):
    print(i / len(subtotal)*100)
    subsubtotal['Model'] = np.zeros(700) #resetear datos
    subsubtotal['Buying'] = np.zeros(700)
    subsubtotal['Selling'] = np.zeros(700)
    subsubtotal['Margin'] = np.zeros(700)
    for j in range(0, subtotal['Pieces'].loc[i].astype(int)):
        np.random.seed(j*i)
        modelindex = np.random.choice(df_prob.index, 1, p=df_prob['Probability']) #Inidica el index del modelo
        subsubtotal['Model'].loc[j] = str(df_prob['Device name'].loc[modelindex[0]] +
                                          " " + df_prob['Grade'].loc[modelindex[0]]) #Indica el modelo y grading con el index
        subsubtotal['Buying'].loc[j] = float(df[df['union'] == subsubtotal['Model'].loc[j]]['Buying price']) #Usa filtro para buscar el precio de compra
        np.random.seed(j*i*20)
        to_who = np.random.choice([1, 2, 3], 1, p=[sell_1, sell_2, sell_3])#A quién se venderá dependerá del peso indicado al inicio
        if to_who == 1:
            subsubtotal['Selling'].loc[j] = float(df[df['union'] == subsubtotal['Model'].loc[j]]['Selling price 1'])
        elif to_who == 2:
            subsubtotal['Selling'].loc[j] = float(df[df['union'] == subsubtotal['Model'].loc[j]]['Selling price 2'])
        else:
            subsubtotal['Selling'].loc[j] = float(df[df['union'] == subsubtotal['Model'].loc[j]]['Selling price 2'])
        subsubtotal['Margin'] = subsubtotal['Selling'] - subsubtotal['Buying'] #Venta menos compra
    subtotal['Buying'].loc[i] = sum(subsubtotal['Buying'])
    subtotal['Selling'].loc[i] = sum(subsubtotal['Selling'])
    subtotal['Margin'].loc[i] = sum(subsubtotal['Margin'])

#Resumen de los resultados
subtotal.describe()

#Gráfico de los resultados
q_min = min(subtotal['Margin'])
q_max = max(subtotal['Selling'])
plt.style.use('bmh')
fig1 = plt.figure(figsize=(6*1, 4*4))
ax1 = plt.subplot(411)
ax1.bar(list(subtotal.index),subtotal['Pieces'], color= 'gray')
ax1.hlines(subtotal['Pieces'].mean(), xmax=simulations, xmin=0, 
           color='black', label='Average')
ax1.set_title("Pieces per simulation", fontstyle='italic')
ax1.set_ylabel('Received pieces')
ax2 = plt.subplot(412)
ax2.hlines(subtotal['Buying'].mean(), xmax=simulations, xmin=0, 
           color='black', label='Average')
ax2.bar(list(subtotal.index),subtotal['Buying'], color= 'gray')
ax2.set_title("Buying amount per simulation", fontstyle='italic')
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax2.set_ylabel('Millions of MXN')
ax3 = plt.subplot(413)
ax3.hlines(subtotal['Selling'].mean(), xmax=simulations, xmin=0, 
           color='black', label='Average')
ax3.bar(list(subtotal.index),subtotal['Selling'], color= 'gray')
ax3.set_title("Selling amount per simulation", fontstyle='italic')
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax3.set_ylabel('Millions of MXN')
ax4 = plt.subplot(414)
ax4.hlines(subtotal['Margin'].mean(), xmax=simulations, xmin=0, 
           color='black', label='Average')
ax4.bar(list(subtotal.index),subtotal['Margin'], color= 'gray')
ax4.set_title("Margin per simulation", fontstyle='italic')
ax4.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax4.set_ylabel('Millions of MXN')
ax4.set_xlabel('Number of simulation')

fig2 = plt.figure(figsize=(6*1, 4*4))
ax5 = plt.subplot(411)
ax5.hist(subtotal['Pieces'], density=True, color='gray')
ax5.set_title('Histogram for received pieces', fontstyle='italic')
ax5.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.2%')))
ax5.set_ylabel('Percentage of appearence')
ax6 = plt.subplot(412)
ax6.hist(subtotal['Buying'], density=True, color='gray')
ax6.set_title('Histogram for buying amount (in millions MXN)', fontstyle='italic')
ax6.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.5%')))
ax6.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax6.set_ylabel('Percentage of appearence')
ax6.set_xlim(q_min, q_max)
ax7 = plt.subplot(413)
ax7.hist(subtotal['Selling'], density=True, color='gray')
ax7.set_title('Histogram for selling amount (in millions MXN)', fontstyle='italic')
ax7.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.5%')))
ax7.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax7.set_ylabel('Percentage of appearence')
ax7.set_xlim(q_min, q_max)
ax8 = plt.subplot(414)
ax8.hist(subtotal['Margin'], density=True, color='gray')
ax8.set_title('Histogram for margin amount (in millions MXN)', fontstyle='italic')
ax8.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.4%')))
ax8.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax8.set_ylabel('Percentage of appearence')
ax8.set_xlim(q_min, q_max)

#Crear intérvalo de confianza del 95% para hallar el promedio real de cada medida.
pieces_min, pieces_max = st.t.interval(alpha=0.95, df=len(subtotal['Pieces'])-1, 
              loc=np.mean(subtotal['Pieces']), 
              scale=st.sem(subtotal['Pieces'])) 
buy_min, buy_max = st.t.interval(alpha=0.95, df=len(subtotal['Buying'])-1, 
              loc=np.mean(subtotal['Buying']), 
              scale=st.sem(subtotal['Buying'])) 
sell_min, sell_max = st.t.interval(alpha=0.95, df=len(subtotal['Selling'])-1, 
              loc=np.mean(subtotal['Selling']), 
              scale=st.sem(subtotal['Selling'])) 
margin_min, margin_max = st.t.interval(alpha=0.95, df=len(subtotal['Margin'])-1, 
              loc=np.mean(subtotal['Margin']), 
              scale=st.sem(subtotal['Margin'])) 



#Gráfico de la densidad de probabilidad
fig3 = plt.figure(figsize=(6*1, 4*4))
ax9 = plt.subplot(411)
ax9_line = np.linspace(min(subtotal['Pieces']), max(subtotal['Pieces']), 1000)
ax9.plot(ax9_line, st.gaussian_kde(subtotal['Pieces']).evaluate(ax9_line),
         color='black', linewidth=1)
ax9.set_title('Kernel-density estimate of pieces', fontstyle='italic')
ax9.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.5%')))
ax9.set_ylabel('% KDE density')
ax9.plot(ax9_line, st.norm(loc=np.mean(subtotal['Pieces']), 
                 scale=np.std(subtotal['Pieces'])).pdf(ax9_line), color='black', 
         linewidth= 2)
ax9.fill_between(ax9_line, st.norm(loc=np.mean(subtotal['Pieces']), 
                 scale=np.std(subtotal['Pieces'])).pdf(ax9_line), 
                 where= (ax9_line > pieces_min) & (ax9_line < pieces_max),
                 color= 'gray', alpha= 0.6)    
ax10 = plt.subplot(412)
ax10_line = np.linspace(q_min, q_max, 1000)
ax10.plot(ax10_line,
         st.gaussian_kde(subtotal['Buying']).evaluate(ax10_line),
         color='black', linewidth= 1)
ax10.set_title('Kernel-density estimate of buying amount (in millions MXN)', fontstyle='italic')
ax10.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.5%')))
ax10.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax10.set_ylabel('% KDE density')
ax10.set_xlim(q_min, q_max)
ax10.plot(ax10_line, st.norm(loc=np.mean(subtotal['Buying']), 
                 scale=np.std(subtotal['Buying'])).pdf(ax10_line), color='black', 
          linewidth= 2)
ax10.fill_between(ax10_line, st.norm(loc=np.mean(subtotal['Buying']), 
                 scale=np.std(subtotal['Buying'])).pdf(ax10_line), 
                 where= (ax10_line > buy_min) & (ax10_line < buy_max),
                 color= 'gray', alpha= 0.6)  
ax11 = plt.subplot(413)
ax11_line = np.linspace(q_min, q_max, 1000)
ax11.plot(ax11_line,
         st.gaussian_kde(subtotal['Selling']).evaluate(ax11_line),
         color= 'black', linewidth= 1)
ax11.set_title('Kernel-density estimate of selling amount (in millions MXN)', fontstyle='italic')
ax11.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.5%')))
ax11.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax11.set_ylabel('% KDE density')
ax11.set_xlim(q_min, q_max)
ax11.plot(ax11_line, st.norm(loc=np.mean(subtotal['Selling']), 
                 scale=np.std(subtotal['Selling'])).pdf(ax11_line), color='black', 
          linewidth= 2)
ax11.fill_between(ax11_line, st.norm(loc=np.mean(subtotal['Selling']), 
                 scale=np.std(subtotal['Selling'])).pdf(ax11_line), 
                 where= (ax11_line > sell_min) & (ax11_line < sell_max),
                 color= 'gray', alpha= 0.6)  
ax12 = plt.subplot(414)
ax12_line = np.linspace(q_min, q_max, 1000)
ax12.plot(ax12_line,
         st.gaussian_kde(subtotal['Margin']).evaluate(ax12_line),
         color= 'black', linewidth= 1)
ax12.set_title('Kernel-density estimate of amount (in millions MXN)', fontstyle='italic')
ax12.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x, '.4%')))
ax12.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(x/1000000, '.2f')))
ax12.set_ylabel('% KDE density')
ax12.set_xlim(q_min, q_max)
ax12.plot(ax12_line, st.norm(loc=np.mean(subtotal['Margin']), 
                 scale=np.std(subtotal['Margin'])).pdf(ax12_line), color='black', 
          linewidth= 2)
ax12.fill_between(ax12_line, st.norm(loc=np.mean(subtotal['Margin']), 
                 scale=np.std(subtotal['Margin'])).pdf(ax12_line), 
                 where= (ax12_line > margin_min) & (ax12_line < margin_max),
                 color= 'gray', alpha= 0.6)  

#Crear un intervalo de confianza 
st.norm.interval(alpha= 0.95, loc= np.mean(subtotal['Buying']), scale= st.sem(subtotal['Buying']))

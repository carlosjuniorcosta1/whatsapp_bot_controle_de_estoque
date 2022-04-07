# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 13:10:33 2021

@author: Usuario
"""

#robô em fase de implementação. Por enquanto, ele só cadastra produtos e emite uma nota fiscal fictícia
#a base de dados utilizadas é das ofertas do mercado livre

import pandas as pd 
import time  
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import requests
import re
import random
import os
from webdriver_manager.chrome import ChromeDriverManager

nome_do_grupo = input('Digite o nome do grupo do whatsapp - exatamente igual ')
df_ml = pd.read_csv('df_estoque.csv')
df_ml  = df_ml[:200]
df_ml.columns = ['codigo', 'produto', 'preco', 'preco_antigo', 'descricao_produto',
       'parcelas_sem_juros', 'frete_gratis', 'diferenca', 'desconto_porcento',
       'media_desconto', 'mediana']

df_ml = df_ml[['codigo', 'produto', 'preco']]

df_estoque_novo = df_ml.copy()


navegador = webdriver.Chrome(ChromeDriverManager().install())
navegador.get('https://web.whatsapp.com/')

while len(navegador.find_elements_by_id('side')) < 1:
    time.sleep(1)
    
busca = navegador.find_element_by_xpath('//div[@class="_13NKt copyable-text selectable-text"]')
time.sleep(2)
busca.send_keys(nome_do_grupo)
time.sleep(3)
campo_msg = navegador.find_element_by_xpath('//span[@class="matched-text i0jNr"]').click()
time.sleep(3)

while True:

    variavel = navegador.find_elements_by_xpath('//div[@class="_1Gy50"]')[-1].text
    variavel = variavel.lower()
    
    if variavel == 'emitir nota':
        
        while True:
            
           
            escreve_msg = navegador.find_element_by_css_selector('div[title="Mensagem"').send_keys('Ei, digita o código do produto que a gente te manda a nota fiscal :)')
            time.sleep(4)
            navegador.find_element_by_class_name('_4sWnG').click() #envia
        
       
            time.sleep(15)
         
            codigo_digitado = navegador.find_elements_by_xpath('//div[@class="_1Gy50"]')[-1].text
              
            
            time.sleep(6)
              
            codigo_digitado = int(codigo_digitado) #pega o último código digitado pelo usuario
            time.sleep(1)
                
            nota_fiscal_prev = df_ml.loc[codigo_digitado, :]
            nota_fiscal_prev = pd.DataFrame(nota_fiscal_prev)
            nota_fiscal_prev = nota_fiscal_prev.transpose()
            
            nota_fiscal_prev['numero_da_nota'] = random.randint(10000,200000) #cria um codigo pra notas
            nota_fiscal_prev['comprador'] = 'grupo_teste'
            nota_fiscal_prev['nf_emitida_em'] = pd.Timestamp.now() #coloca a hora da emissão
            
            nota_fiscal_prev.reset_index(inplace=True)
        
            numero_nf_str = str(nota_fiscal_prev['numero_da_nota'][0])
        
            nota_fiscal_prev.to_excel(f'nota_fiscal_{nota_fiscal_prev["numero_da_nota"][0]}.xlsx')
            nome_do_arquivo_da_nota = 'nota_fiscal_' + numero_nf_str + '.xlsx'
            dirname, filename = os.path.split(os.path.abspath(nome_do_arquivo_da_nota))
            arquivo_da_nota = os.path.join(dirname, filename)
        
            df_ml = df_ml.query('codigo != @codigo_digitado')
            numero_estoque_atualizado = str(random.randint(50000, 800000))
            nome_do_arquivo_do_estoque = 'estoque_atualizado_' + numero_estoque_atualizado + '.xlsx'          
            df_ml.to_excel(nome_do_arquivo_do_estoque)
            
            dirname_estoque, filename_estoque = os.path.split(os.path.abspath(nome_do_arquivo_do_estoque))
            arquivo_do_estoque = os.path.join(dirname_estoque, filename_estoque)
            
            time.sleep(1)
            clica_no_clip= navegador.find_element_by_css_selector('span[data-icon="clip"').click()
            time.sleep(2)
            anexa = navegador.find_element_by_css_selector('input[type="file"]')
            time.sleep(2)
            anexa.send_keys(arquivo_da_nota)
            time.sleep(2)
            
             
            nota = navegador.find_element_by_css_selector('span[data-testid="send"]').click()
            time.sleep(2)
            #envio do estoque
            
            time.sleep(1)
            clica_no_clip= navegador.find_element_by_css_selector('span[data-icon="clip"').click()
            time.sleep(2)
            anexa = navegador.find_element_by_css_selector('input[type="file"]')
            time.sleep(2)
            anexa.send_keys(arquivo_do_estoque)
            time.sleep(2)
            
              
            nota = navegador.find_element_by_css_selector('span[data-testid="send"]').click()
            time.sleep(3)
            
           
            while len(navegador.find_elements_by_id('side')) < 1:
                time.sleep(4)
                
            break
       
    if variavel == "cadastrar produto":
                
        while True:
        
            
            escreve_msg = navegador.find_element_by_css_selector('div[title="Mensagem"').send_keys('Digite o nome do produto a ser incluído no estoque:')
            time.sleep(4)
            navegador.find_element_by_class_name('_4sWnG').click() #envia
            time.sleep(10)
            produto_digitado = navegador.find_elements_by_xpath('//div[@class="_1Gy50"]')[-1].text
            time.sleep(3)

            
            escreve_msg_3 = navegador.find_element_by_css_selector('div[title="Mensagem"').send_keys(f'Agora digite o preço do produto:')
            time.sleep(2)
            navegador.find_element_by_class_name('_4sWnG').click() 
            time.sleep(15)
            produto_digitado_preco = navegador.find_elements_by_xpath('//div[@class="_1Gy50"]')[-1].text
            time.sleep(6)
            produto_digitado_preco = re.sub(r',', '.', produto_digitado_preco)
            produto_digitado_preco = float(produto_digitado_preco)
            
            df_cadastro = pd.DataFrame()
            df_cadastro['produto'] = [produto_digitado]
            df_cadastro['preco'] = [produto_digitado_preco]
            df_cadastro.reset_index(inplace=True)
            df_cadastro.columns = ['codigo', 'produto', 'preco']
            
            
            df_estoque_novo = pd.concat([df_estoque_novo, df_cadastro], ignore_index = True)
            
            escreve_msg_4 = navegador.find_element_by_css_selector('div[title="Mensagem"').send_keys(f'{produto_digitado} adicionado com sucesso!')
            time.sleep(4)
            navegador.find_element_by_class_name('_4sWnG').click() #envia
            
            
            df_estoque_novo.drop('codigo', axis = 1, inplace=True)
            df_estoque_novo.reset_index(inplace=True)
            df_estoque_novo.columns = ['codigo', 'produto', 'preco'] #até aqui rodou
            
            numero_estoque_atualizado_cadastro = str(random.randint(50000, 800000))
            nome_do_arquivo_do_estoque_cadastro = 'estoque_atualizado_' + numero_estoque_atualizado_cadastro + '.xlsx'          
            df_estoque_novo.to_excel(nome_do_arquivo_do_estoque_cadastro)
            
            dirname_estoque_cadastro, filename_estoque_cadastro = os.path.split(os.path.abspath(nome_do_arquivo_do_estoque_cadastro))
            arquivo_do_estoque_cadastro = os.path.join(dirname_estoque_cadastro, filename_estoque_cadastro)
            
            time.sleep(1)
            clica_no_clip= navegador.find_element_by_css_selector('span[data-icon="clip"').click()
            time.sleep(2)
            anexa = navegador.find_element_by_css_selector('input[type="file"]')
            time.sleep(2)
            anexa.send_keys(arquivo_do_estoque_cadastro)
            
            time.sleep(2)
            navegador.find_element_by_css_selector('span[data-testid="send"]').click() #mantenha a tela maximizada
            
            break 

       
    else:
        continue
    


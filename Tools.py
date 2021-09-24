# !/usr/bin/python3

######################################################################################################################################
#                                                                                                                                    #
#   Code created as a library for the Main.py code                                                                                          #
#                                                                                                                                    #
#   Author: odinhr (odinhenrod@gmail.com)                                                                                            #
#                                                                                                                                    #
######################################################################################################################################


from bs4 import BeautifulSoup
from price_parser import Price
import requests
import pandas as pd
import re
from io import StringIO
import os
from tkinter import *


def linkExtractor(raw_prod,precio):    #Function to extract the link to look for the products of the ticket
    #print(raw_prod)
    isThereSpaces = raw_prod.find(" ", 0, len(raw_prod)) 
    if isThereSpaces != -1:
        producto=raw_prod.replace(" ", "+")
    else:
        producto=raw_prod
    url_corte ='https://www.dia.es/compra-online/search?text='
    final_url = '&x=0&y=0'
    url = url_corte + producto + final_url
    retailerWebPage = requests.get(url)
    soup = BeautifulSoup(retailerWebPage.content,'html.parser')
    allPrices = soup.find_all('p',class_='price')
    allLinks = soup.find_all('a', class_='productMainLink')
    precios = list()
    enlaces=list()
    for link in allLinks:
        if 'href' in link.attrs:
            enlaces.append(str(link.attrs['href']))
    for i in allPrices:
        precios.append((i.text))
    for i in allLinks:
        enlaces.append(i.href)
    for i in range(len(precios)):
        precios[i]=precios[i].replace(",", ".")
        precios[i]= Price.fromstring(precios[i])
        precios[i]=precios[i].amount_float
    prices=list()
    for i in range(len(precios)):
        a=float(precio[0])
        if precios[i] == a:
            finalLink = 'https://www.dia.es/'+enlaces[i]
            break
        else:
            finalLink = None
    return finalLink


def getNutriTable(link):            #Function to extract a table with the nutritional values
    if link != None:
        URL = link
        r = requests.get(URL).text
        pos=r.find('valor energ')
        if pos != -1:
            tables = pd.read_html(URL,match="valor energético")
            return [tables[0],0]
            
        else:
            return [None,None]
    else:
        return [None,None]
        
def infoToTable(price,product,table):           #Function to introduce the info in an excel and csv tables
    if table[1] == None:
        return '2'
    else:
        strpri = str(price)
        strprice=strpri.replace(".", "dot")
        directorio = '/'+ str(price)
        if not os.path.exists('/home/uipo/resultados'+directorio):
            os.makedirs('/home/uipo/resultados'+directorio)
        nombrearchivo='/'+strprice + '.csv'
        nombrearchivoexcel='/'+ strprice + '.xlsx'
        new_header = table[0].iloc[0] #grab the first row for the header

        table[0].to_csv(r'/home/uipo/resultados'+ directorio + nombrearchivo , index = False, header=True)
        table[0].to_excel(r'/home/uipo/resultados'+ directorio + nombrearchivoexcel, sheet_name='Valor Nutricional', index = False)

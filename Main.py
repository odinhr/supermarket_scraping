# !/usr/bin/python3

######################################################################################################################################
#                                                                                                                                    #
#   Code created to take nutritional tables from a supermarket website after taking elements from a ticket image. This is customized #
#   for DIA, a spanish supermarket.                                                                                                  #
#                                                                                                                                    #
#   Author: odinhr (odinhenrod@gmail.com)                                                                                            #
#                                                                                                                                    #
######################################################################################################################################

import cv2 
import pytesseract
import re
from Tools import linkExtractor, infoToTable, getNutriTable   #small library created for this code
from price_parser import Price
import tkinter as tk


def show_entry_fields():
    img=e1.get()
    custom_config = r'--oem 3 --psm 6'
    string = pytesseract.image_to_string(img, config=custom_config)
    num_caja=string.find('N.CAJA')
    num_total_compra=string.find('TOTAL COMPRA')
    new_string_prev = string[(num_caja+10):(num_total_compra-1)] #Create an string to delete elements which are not important for webscraping
    new_string=new_string_prev.split('\n')
    prices=[]

    for i in range(len(new_string)):
        new_string[i]=new_string[i].replace('\n','')  #Change \ for spaces
        new_string[i]=new_string[i].replace(',','.')
    new_string = list(filter(None, new_string)) #Remove empty elements from the list of products + prices
    #print(new_string)

    for i in range(len(new_string)):
        prices.append(re.findall("\d+\.\d+", new_string[i]))

    for i in range(len(new_string)):
        productLink = linkExtractor(new_string[i],prices[i])
        table=getNutriTable(productLink)
        infoToTable(new_string[i],prices[i],table)

##################
## GUI CREATION ##
##################

master = tk.Tk()
master.title('WEB SCRAPPER DIA')
master.geometry("400x150")
master.resizable(True, True)

tk.Label(master, text="Path to ticket").pack(side = tk.TOP, pady = 0)

e1 = tk.Entry(master,textvariable=1)
e1.place(x= 10, y=30, width = 380, height = 20)

tk.Button(master, text='Close', command=master.quit).pack(side = tk.BOTTOM, pady = 10)

tk.Button(master, text='Analize', command=show_entry_fields).pack(side = tk.BOTTOM, pady = 0)

tk.mainloop()


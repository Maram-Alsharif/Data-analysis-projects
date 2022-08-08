# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 11:10:22 2022

@author: Russa
"""
import re
import pandas as pd

df = pd.read_excel(r"FILE PATH")


for column in df.columns:

    df[column] = df[column].str.replace("[إأٱآا]","ا")
    df[column] = df[column].str.replace("ى", "ي")
    df[column] = df[column].str.replace("ئ", "ي")
    df[column] = df[column].str.replace("ؤ", "و")
    df[column] = df[column].str.replace("ة", "ه")
    df[column] = df[column].str.replace(""" ّ    | # Tashdid
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         ""","")
    df[column] = df[column].str.replace(r'[^\w\s]','')

df.to_excel(r"FILE PATH", index=False)
print("done")
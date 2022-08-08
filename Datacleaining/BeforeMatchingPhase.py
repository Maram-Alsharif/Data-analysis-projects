#!/usr/bin/env python
# coding: utf-8

# In[27]:


#needed packages
import numpy as np
import pandas as pd
import re


# In[28]:


#The location of researches file
loc ='Shareaa College - Normalized.xlsx' 
data = pd.read_excel(loc)


# In[ ]:


df2 = pd.DataFrame(data)
df2.astype('string')


# In[ ]:


# Normalize the file
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
    
#save the changes 
df2.to_excel(r"Shareaa College - Normalized.xlsx", index=False)
print("done")


# In[ ]:


# prefix operations


# In[30]:


import re
def Aboprefix(AuthorName):

#---------------------#1-----------------    
#First we split the string based on prefix Aboo to list
    r = re.compile('(\sابو)')

    SplitAuthorName=r.split(AuthorName)
    
#---------------------#2-----------------
#we split the string based on whitespases

    
    AuthorNameList=(' '.join(SplitAuthorName)).split(" ")

#---------------------#3-----------------
#remove all whitespases   
 
    NewAuthorNameList=list(filter(('').__ne__, AuthorNameList))

#---------------------#4-----------------
#remove all bent and ben prefixes 
    NewAuthorNameList=Remove_Prefix(NewAuthorNameList)

#---------------------#5-----------------
#to delete all spaces and lines 

    List2 = [ x.replace('\t', '').replace('\n', '') for x in NewAuthorNameList ]
    NameOfAuther=' '.join(List2)

    return NameOfAuther


# In[31]:


#To replace all unwanted words
def Remove_Prefix(AuthorNameList):
    PrefixList=['بن','بنت']
    AuthorNameListAfterRemovePrefix=list(filter(lambda i: i not in PrefixList,AuthorNameList))
    return AuthorNameListAfterRemovePrefix


# In[32]:


#to compare the UQU_LeadAuthor with faculty  
for j in range(0,len(df2)):
        str1=str(df2.loc[j,'Name'])
        df2.at[j, "Name"] = Aboprefix(str1)
           


# In[ ]:


#to remove all al and abo prifex 
PrefixList=['ال','ابو']                
for i in range(0,len(PrefixList)):
      for j in range(0,len(df2)):
            InnerList=str(df2.loc[j, "Name"]).split()
            for m in range(0,len(InnerList)-1):
                if(InnerList[m]==PrefixList[i]):
                    NextValue=InnerList[m+1]
                    InnerList[m+1]=InnerList[m]+""+NextValue
                    InnerList[m]=' '
                    df2.loc[j, "Name"]=' '.join(InnerList)


# In[33]:


df2.to_excel('Shareaa College - Normalized.xlsx'  ,index=False)


# In[34]:


df2


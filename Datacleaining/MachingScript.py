#!/usr/bin/env python
# coding: utf-8

# In[166]:


#import needed packages
import numpy as np
import pandas as pd
import re


# In[167]:


#get the info from the excel sheet
#The location of dar almandumah dataset  
loc = 'Dawaa_Dataset_After_Split_Column.xlsx'
#The location of faculty members dataset
loc2='Dawaa College - Normalized.xlsx'
data = pd.read_excel(loc)
data2 = pd.read_excel(loc2)


# In[168]:


#Create dataframe as type string
df = pd.DataFrame(data2)
df.astype('string')
df2 = pd.DataFrame(data, columns= ['Column2'])
df2.astype('string')
df


# In[169]:


# then apply groupby (FirstName) from faculty members dataset
GroupFistName=df.groupby(by=["FirstName"])
GroupFistName


# In[170]:


#after that we put the results in a dictionary as list
Dictofgroups=df.groupby('FirstName')['Name'].apply(list).to_dict()


# In[171]:


Dictofgroups


# In[172]:


# create a rule number column that represents the degree of ambiguity of the name
df2["Column3"] = ""
df2.loc[0, "Column3"]="UQU_Rule_Number"
df2["Column4"] = ""
# create a new column that holds T/F value to determine if the name exists in the faculty members' dataset or not 
df2.loc[0, "Column4"]="UQU_existence"
# create a new column that holds researcher's name as it exists on the faculty members' dataset
df2["Column5"]=""
df2.loc[0, "Column5"]="UQU_Name"


# In[173]:


df


# In[175]:


#apply the loop in dar almandumah dataset starting from index 1
#note: Dawaa college only apply to the first part of  rule 3
for i in range(1,len(df2)):
    #get the researcher name as list
    authorNameAsList=splitName(str(df2.loc[i, "Column2"]))
    #take the first index on the list
    keyValue=authorNameAsList[0]
    indexOfName=i
    #Check if the key (first name) is exist in the dictionary
    if(checkKey(keyValue)=='Key exists'):
        if(len(authorNameAsList)==2):
            #if the name list length == 2
            Rule_Number_4(keyValue,authorNameAsList,indexOfName)
        if(len(authorNameAsList)>=3):
            #if the name list length >= 3, then check rule number 1 
            matchingValue=Rule_Number_1(keyValue,authorNameAsList,indexOfName)
            if(matchingValue=='F'):
                #if rule number 1 return F , then check rule number 2
                matchingValue2=Rule_Number_2(keyValue,authorNameAsList,indexOfName)
                if(matchingValue2=='F'):
                    #if rule number 2 return F , then check rule number 3
                    matchingValue3=Rule_Number_3(keyValue,authorNameAsList,indexOfName)
                    if(matchingValue3=='F'):
                        #if rule number 3 return F, then the first index exists in the dataset but no name match  the rest index
                        df2.loc[indexOfName, "Column3"]='Rule_Number_5'
                        df2.loc[indexOfName, "Column4"]="False"
    else:
        #if the key (first name) dosent exist update column 3 value 
        df2.loc[indexOfName, "Column3"]='No_Rule'
        df2.loc[indexOfName, "Column4"]="False"


# In[156]:


#to check if the key is exist in dictionary
def checkKey(key):
    if key in Dictofgroups:
        return "Key exists"
    else:
        return "Key does not exist"


# In[157]:


def splitName(authorName):
    #split the string based on spaces 
    splitAuthorName=authorName.split(" ")
    #remove all whitespases   
    authorNameList=list(filter(('').__ne__,splitAuthorName))
    #retun the name list
    return authorNameList


# In[ ]:


def unifyFormat(value):
    #remove the bracket 
    value=value.replace('[','').replace(']','').replace("'",'')
    #add the values in list and split them based on comma if exist
    listOfvalues = re.split(",+", value)
    return listOfvalues


# In[17]:


# If name exist in the dar almandumahd atasest as the same format in faculty members' dataset
def Rule_Number_1(keyValue,authorNameAsList,indexOfName):
    #take the value as string
    value=str(Dictofgroups.get(keyValue))
    #remove the bracket 
    value=value.replace('[','').replace(']','').replace("'",'')
    #add the values in list and split them based on comma if exist
    listOfvalues = re.split(",+", value)
    match='F'
    for m in range(0,len(listOfvalues)):
        if(authorNameAsList[1:]==splitName(listOfvalues[m])): 
            df2.loc[indexOfName, "Column3"]='Rule_Number_1'
            df2.loc[indexOfName, "Column4"]="True"
            match='T'

    return  match   


# In[18]:


#only length of 3 or 4 (simple -ambiguity) 
#in case, researcher's name format include first and second proper laqab
#while the naming format in umm al-qura university may uses the second proper laqab only
def Rule_Number_2(keyValue,authorNameAsList,indexOfName):
    #take the values from dictofgroups as list and unify its format
    listOfvalues=unifyFormat(str(Dictofgroups.get(keyValue)))
    match='F' 
    for m in range(0,len(listOfvalues)):
        innerList=splitName(listOfvalues[m])
            
        if(len(authorNameAsList[1:])<len(innerList)):
                    minList=authorNameAsList[1:]
                    maxlist=innerList
        else:
            minList=innerList
            maxlist=authorNameAsList[1:]
      
        minList_copy = minList[0:len(minList)-1]
        maxlist_copy = maxlist[0:len(maxlist)-2]
        if(minList_copy==maxlist_copy): 
                if minList[len(minList)-1] == maxlist[len(maxlist)-2]:
                        df2.loc[indexOfName, "Column3"]='Rule_Number_2'
                        df2.loc[indexOfName, "Column4"]="True"
                        match='T'
                        
            
                elif minList[len(minList)-1] == maxlist[len(maxlist)-1]:
                        df2.loc[indexOfName, "Column3"]='Rule_Number_2'
                        df2.loc[indexOfName, "Column4"]="True"
                        match='T'
                        
                else:
                    match='F'
        else:
                    return match


# In[136]:


# to delete the middle name from the faculty dataset as dar al mandumah naming format does not contain it (medium -ambiguity) 
def Rule_Number_3(keyValue,authorNameAsList,indexOfName):
    #take the values from dictofgroups as list and unify its format
    listOfvalues=unifyFormat(str(Dictofgroups.get(keyValue)))
    match='F'
    for m in range(0,len(listOfvalues)):
        #remove grandfather name
        firstList=splitName(listOfvalues[m])
        firstList[1]=' '
        innerList=list(filter((' ').__ne__, firstList))
        if(len(innerList)==2):
            if(authorNameAsList[1:]==innerList): 
                df2.loc[indexOfName, "Column3"]='Rule_Number_3'
                df2.loc[indexOfName, "Column4"]="True"
                match='T'
        if(len(innerList)==3):
                authorNameAsList=authorNameAsList[1:]
                if authorNameAsList[len(authorNameAsList)-1] == innerList[len(innerList)-2]:
                        df2.loc[indexOfName, "Column3"]='Rule_Number_3'
                        df2.loc[indexOfName, "Column4"]="True"
                        match='T'
                        
            
                elif authorNameAsList[len(authorNameAsList)-1] == innerList[len(innerList)-1]:
                        df2.loc[indexOfName, "Column3"]='Rule_Number_3'
                        df2.loc[indexOfName, "Column4"]="True"
                        match='T'
                        
                else:
                    match='F'
          
            

    return  match


# In[20]:


#only name of length 2 (High-Ambiguity) 
def Rule_Number_4(keyValue,authorNameAsList,indexOfName):
    #take the value as string
    value=str(Dictofgroups.get(keyValue))
    #remove the bracket 
    value=value.replace('[','').replace(']','').replace("'",'')
    #add the values in list and split them based on comma if exist
    listOfvalues = re.split(",+", value)
    #to print if value is not exist as false
    match='F' 
    for m in range(0,len(listOfvalues)):
            innerList=splitName(listOfvalues[m])
            if(authorNameAsList[len(authorNameAsList)-1]==innerList[len(innerList)-2]): 
                    df2.loc[indexOfName, "Column3"]='Rule_Number_4'
                    df2.loc[indexOfName, "Column4"]="True"
                    match='T'
            if(authorNameAsList[len(authorNameAsList)-1]==innerList[len(innerList)-1]):
                    df2.loc[indexOfName, "Column3"]='Rule_Number_4'
                    df2.loc[indexOfName, "Column4"]="True"
                    match='T'
    #If the name dosent match 
    if(match=='F'):
        df2.loc[indexOfName, "Column3"]='Rule_Number_4'
        df2.loc[indexOfName, "Column4"]="False"
    


# In[180]:


df2


# In[185]:


#add all mapped names on the list  
NamesList = list() ;
for i in range(1,len(df2)):
    if ((df2.loc[i,"Column3"]=="Rule_Number_1" or df2.loc[i,"Column3"]=="Rule_Number_2"  or df2.loc[i,"Column3"]=="Rule_Number_3"  ) and (df2.loc[i,"Column4"]=="True")):
            NamesList.append(df2.loc[i,"Column2"])


# In[186]:


print(len(set(NamesList)))


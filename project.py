#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 17:14:02 2024

@author: samuelesottile
"""

import os
import pandas as pd
import numpy as np
import csv as csv
import shutil




# Change directory where to handle the files
os.chdir('/Users/samuelesottile/Desktop/Test/mol files')

#Print the new directory
print(os.getcwd())

number=[]
title=[]

#Get lists as number and title from the name of the .mol files

for file in os.listdir():
    name, ext = os.path.splitext(file)
    title.append(file)
    splitted = name.split('_')
    #number.append(int(splitted))
    number.append(splitted[-1])


#Create a DataFrame from the title and the Cid number of the .mol files

df = pd.DataFrame()
df['Molecule']=title
df['Cid'] = number

print(df.head())

#Create a DataFrame out of the NPASS csv file

os.chdir('/Users/samuelesottile/Desktop/Test')

npass=pd.read_csv('data_catalogue_NPASS_plant_compounds.csv',
                  sep = '|', 
             on_bad_lines = "skip")
print(npass['pubchem_cid'])

#Create a DataFrame with elements that have the Cid of the df DataFrame and drop duplicates

da=npass[npass['pubchem_cid'].isin(df['Cid'])].drop_duplicates()

print(da.info())


#By sorting values in terms of pubchem_cid we see that there are elements with same pref_name or np_id

print(da.sort_values("pubchem_cid"))

#Keep only the first of the duplicates having the same pref_name or np_id

da = da.drop_duplicates(subset=['np_id', 'pref_name'], keep='first')

#Check how many rows are left

print(da.count())

#Count the different values for different columns in order to choose the best partition

print(da['genus_name'].value_counts(sort=True))

print(da['org_name'].value_counts(sort=True))

print(da['species_name'].value_counts(sort=True))

print(da['family_name'].value_counts(sort=True))

print(da.isna().sum())


#Add another column family_name in df Dataframe with the corresponding name of the family for each Molecule and Cid

df['family_name'] = df['Cid']    

for j,l in zip(df['Cid'], range(0,311)):
    for i,k in zip(da['pubchem_cid'], da['family_name']):
            if j!=i:
                continue
            df.iloc[l, df.columns.get_loc('family_name')] = k

        
# Change directory where to handle the files
os.chdir('/Users/samuelesottile/Desktop/Test/mol files')


col='family_name'

colu='Molecule'

#Create folders for each values of the family_name and add in those folders the files with corresponding family name.

for value, val in zip(df[col], df[colu]):
    path = f'../mol files/{col}/{value}'
    exists = os.path.exists(path)
    if not exists:
        os.makedirs(path)
    shutil.move(val, path)
    


    
    
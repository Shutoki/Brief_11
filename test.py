#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
#from itables import init_notebook_mode
#import itables.options as opt

#init_notebook_mode(all_interactive=True)


# In[2]:


from web.path import file


# In[3]:


df = pd.read_csv(file, delimiter=',', encoding='utf-8')


# In[4]:


df.dtypes


# In[10]:


rom = ('M1805', 'M1403')

test = df.loc[df['romeCode'].str.startswith(rom)]
test


# In[4]:


# test2 = test.loc[test['romeLibelle'].str.contains('dév')]
# test3= test.loc[test['romeLibelle'].str.contains('Dév')]
# test4 = test.loc[test['romeLibelle'].str.contains('data')]
# test5 = test.loc[test['romeLibelle'].str.contains('Data')]

# combined_df = pd.concat([test2, test3, test4, test5])
# combined_df


# In[11]:


combined_df = test.drop_duplicates(subset=['id'])


# In[13]:


combined_df


# In[14]:


new_df = pd.concat([combined_df['id'],combined_df['intitule'],combined_df['description'],combined_df['dateCreation'],combined_df['dateActualisation'],combined_df['lieuTravail_latitude'],combined_df['lieuTravail_longitude'],combined_df['lieuTravail_libelle'],combined_df['romeCode'],combined_df['typeContrat'],combined_df['experienceExige'],combined_df['alternance'],combined_df[ 'origineOffre_urlOrigine'],combined_df['dureeTravailLibelleConverti'],combined_df['competences'],combined_df['qualitesProfessionnelles'],combined_df['formations']], axis = 1)


# In[15]:


new_df.shape


# In[16]:


new_df.fillna(value= 'Non Renseigné', inplace=True)


# In[17]:


new_df.to_csv('france_travail_clean.csv', index=False)


# In[18]:


new_df.dtypes


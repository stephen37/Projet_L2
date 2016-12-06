
# coding: utf-8

# In[33]:

codedir = ''                        # Change this to the directory where you put the code
from sys import path; path.append(codedir)
get_ipython().magic(u'matplotlib inline')


# In[4]:

datadir = '/publicData'                        # Change this to the directory where you put the input data

basename = datadir  + dataname
import os 
os.listdir(datadir) 


# In[46]:

#The database is loaded in a dictionary. A key represent the id of a given user 
#and a value is another dictionary of the rated items of the user with thier respectives rates
import csv
train_path = datadir+"/"+'MovieLens_train.solution'
file_train = csv.reader(open(train_path,"rb"))
dataset = {}
for row in file_train:
    splited_row = row[0].split(" ")
    userID = splited_row[0]
    rates = {}
    for rate in splited_row[1:]:
        rate = rate.split(":")
        if len(rate)>1:
            rates[rate[0]] = float(rate[1])

    dataset[userID] = rates


# In[13]:

#Get the first rated movies of user 5
movies = dataset["5"]
print movies.keys()[0:5]


# In[14]:

#Get the rating of movie 1788 by user 5
print dataset["5"]["1788"]


# In[30]:

#Get the frequency of each rating

import matplotlib.pyplot as plt
import numpy as np


freq = {}
freq[1.0] = 0 
freq[2.0] = 0 
freq[3.0] = 0 
freq[4.0] = 0 
freq[5.0] = 0 

for user in dataset : 
    for movies in dataset[user] : 
        freq[dataset[user][movies]]+=1

plt.bar([1, 2 ,3,4,5], freq.values())

#n, bins, patches = P.hist([1, 2 ,3,4,5], freq.values(), normed=1, histtype='bar', rwidth=0.8)


# # Make recommendations

# In[54]:

import FiltrageCollaboratif as FC
reload(FiltrageCollaboratif)


# In[52]:

#Get the first recommended items for user 5 
print FiltrageCollaboratif.user_reommendations("5", dataset)[0:10]


# In[ ]:

#Make submission file from Collaborative Filtering

FC.makeSubmissionFile("FC.predict", "MovieLens_valid.data")


# In[ ]:




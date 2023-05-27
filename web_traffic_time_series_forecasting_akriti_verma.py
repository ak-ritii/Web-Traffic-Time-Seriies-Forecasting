# -*- coding: utf-8 -*-
"""Web Traffic Time Series Forecasting-Akriti Verma.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CSesG01DNBDm0AquSQ07M8_q74XdTAx8

# Dataset

About Dataset -The training dataset consists of approximately 145k time series. Each of these time series represent a number of daily views of a different Wikipedia article, starting from July, 1st, 2015 up until December 31st, 2016. 

For each time series, you are provided the name of the article as well as the type of traffic that this time series represent (all, mobile, desktop, spider). You may use this metadata and any other publicly available data to make predictions. Unfortunately, the data source for this dataset does not distinguish between traffic values of zero and missing values. A missing value may mean the traffic was zero or that the data is not available for that day.

Link- https://www.kaggle.com/code/bodamanojkumar/web-traffic-time-series-forecasting-eda/input

#Importing the Libraries
"""

import numpy as np #Numerical Python -> Mathematical Operation
import pandas as pd #Data Manipulation

#Loading Dataset from Drive
df = pd.read_csv("/content/drive/MyDrive/Web Traffic Time Series Analysis/train_1.csv.zip", compression = "zip")

#Fiirst 5 rows of Dataset
df.head()

"""Here we can see that the Dataset consists of 5 rows and 551 columns. Each column is of Date category so for clear understanding we take transpose.

#Data Cleaning
"""

#Transposing Data i.e Converting rows into columns and vice versa.
df=df.T

#First 5 Rows of dataset
df.head()

#To give each row an index
df=df.reset_index()

#First 5 rows
df.head()

#For column head, capture the 1st row of data and make it column head
column_head=df.iloc[0,:].values
df.columns=column_head

#First 5 rows
df.head()

#Now we will drop the 1st row as it is assigned as column head
df.drop(0,axis=0,inplace=True)

#First 5 rows
df.head()

#Renaming page column to Date 
df.rename(columns={"Page":"Date"},inplace=True)

#First 5 rows
df.head()

#Datatype of column Date
print(df["Date"].dtype)

"""As it is clear that Date has an object datatype so we will convert it into Date using pandas."""

#Converting Date column datatype to Datetime
df["Date"]=pd.to_datetime(df["Date"])

#Checking if the datatype is changed or not
print(df["Date"].dtype)

#Now we will set the Date column as index
df=df.set_index("Date")

#First 5 rows
df.head()

"""#Splitting the Data

Dataset consists of differnt access types and agents so we will spli the data into these two categories for better analysis.
"""

#Finding number of access_types and agents
access_types=[]  #Creating list for agent_types
agents=[]        #Creating list for agents
for column in df.columns:               #Iterating in columns
  agent=column.split("_")[-1]
  access_type=column.split("_")[-2]      
  access_types.append(access_type)      #adding access_type to list
  agents.append(agent)                  #adding agent to list

#Counting unique access types
from collections import Counter
access_unique=Counter(access_types)
access_unique

#Printing the access types
print("Number of Access Types with all-access type: ",access_unique["all-access"])
print("Number of Access Types with desktop type: ",access_unique["desktop"])
print("Number of Access Types with mobile-web type: ",access_unique["mobile-web"])

#Creating a dataframe
access_df=pd.DataFrame({"Access Type": access_unique.keys(),"Number of Columns":access_unique.values()})

#displaying dataframe
access_df

#Counting agents
agents_unique=Counter(agents)

#Unique value in agents
agents_unique

#Printing number of topics with each agent
print("Number of topics with Agent as spider: ",agents_unique["spider"])
print("Number of topics with Agent as all-agents: ",agents_unique["all-agents"])

#Creating dataFrame
agents_df=pd.DataFrame({"Agent":agents_unique.keys(),"Number of Columns":agents_unique.values()})

#Agent dataframe
agents_df

#Number of columns with null values with respect to access_type
def count_null_columns(pattern):
  pattern_columns=[column for column in df.columns if pattern in column]
  return len(df[pattern_columns].isnull().sum()[df[pattern_columns].isnull().sum()>0])

null_cols_no=[count_null_columns(access_type) for access_type in access_df["Access Type"]]

access_df["No of columns with Nulls"]=null_cols_no

access_df

#Number of columns with null values with respect to agents
def count_null_columns(pattern):
  pattern_columns=[column for column in df.columns if pattern in column]
  return len(df[pattern_columns].isnull().sum()[df[pattern_columns].isnull().sum()>0])

null_cols_no=[count_null_columns(agent) for agent in agents_df["Agent"]]

agents_df["No of columns with Nulls"]=null_cols_no

agents_df

#Calculating Percentage of Null values in access type
access_df["% of nulls"]=access_df["No of columns with Nulls"]/access_df["Number of Columns"]*100
access_df

#Calculating Percentage of Null values in agent
agents_df["% of nulls"]=agents_df["No of columns with Nulls"]/agents_df["Number of Columns"]*100
agents_df

"""#Splitting data based on Projects"""

df.columns[23903].split("_")[-3:]

"_".join(df.columns[23903].split("_")[-3:])

df.columns[23903]

projects=[] #Making project list
for column in df.columns:
  project=column.split("_")[-3] #Etracting language code column name
  projects.append(project)

#Countinng Unique project categories
project_unique=Counter(projects)
project_unique

#Converting into dataframe
project_df=pd.DataFrame({"Project":project_unique.keys(),"Number of columns":project_unique.values()})

#project Dataframe
project_df

#Number of columns with null values with respect to projects
def count_null_columns(pattern):
  pattern_columns=[column for column in df.columns if pattern in column]
  return len(df[pattern_columns].isnull().sum()[df[pattern_columns].isnull().sum()>0])

null_cols_no=[count_null_columns(project) for project in project_df["Project"]]

project_df["No of columns with Nulls"]=null_cols_no

project_df

#Calculating Percentage of Null values in project
project_df["% of nulls"]=project_df["No of columns with Nulls"]/project_df["Number of columns"]*100
project_df

#Sorting values by %of nulls
j

"""It is clear tat columns with commoms.wikimedia.org and www.mediawiki.org have 48% columns with null values"""

df.columns

#Columns with commons.wikimedia.org
req_column_names=[column for column in df.columns if "commons.wikimedia.org" in column]

#mean of req columns
df[req_column_names].sum().mean()

df[req_column_names]

project_df["Project"]

def extract_total_views(project):
  req_col_names=[column for column in df.columns if project in column]
  total_views=df[req_col_names].sum().sum()
  return total_views

total_views=[]
for project in project_df["Project"]:
  total_views.append(extract_total_views(project))

total_views

#New column
project_df["Total views"]=total_views
project_df

def extract_avg_views(project):
  req_col_names=[column for column in df.columns if project in column]
  avg_views=df[req_col_names].sum().mean()
  return avg_views

avg_views=[]
for project in project_df["Project"]:
  avg_views.append(extract_avg_views(project))

avg_views

#New column
project_df["Average views"]=avg_views
project_df

#Changing datatype
project_df['Total views']=project_df['Total views'].astype('int64')
project_df['Average views']=project_df['Average views'].astype('int64')

project_df

#Sorting values by avg views
project_df_sorted=project_df.sort_values(by="Average views",ascending=False)
project_df_sorted

"""#Data Visualization"""

import seaborn as sns  #Data Visualization
import matplotlib.pyplot as plt #Data visualization

plt.figure(figsize=(10,6))
sns.barplot(x=project_df_sorted["Project"],y=project_df_sorted["Average views"])
plt.xticks(rotation="vertical")
plt.title("Average views pereach project")
plt.show

"""**Popular Pages in "en.wikipedia.org"**"""

en_wikipedia_org_cols=[column for column in df.columns if "en.wikipedia.org" in column]

top_pages_en=df[en_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_en

df[top_pages_en.index].plot(figsize = (16,9));

"""**Popular pages in "es.wikipedia.org"**"""

es_wikipedia_org_cols=[column for column in df.columns if "es.wikipedia.org" in column]

top_pages_es=df[es_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_es

df[top_pages_es.index].plot(figsize = (16,9));

"""**Popular pages in "ru.wikipedia.org"**"""

ru_wikipedia_org_cols=[column for column in df.columns if "ru.wikipedia.org" in column]

top_pages_ru=df[ru_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_ru

df[top_pages_ru.index].plot(figsize = (16,9));

"""**Popular pages in "de.wikipedia.org"**"""

de_wikipedia_org_cols=[column for column in df.columns if "de.wikipedia.org" in column]

top_pages_de=df[de_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_de

df[top_pages_de.index].plot(figsize = (16,9));

"""**Popular pages in "ja.wikipedia.org"**"""

ja_wikipedia_org_cols=[column for column in df.columns if "ja.wikipedia.org" in column]

top_pages_ja=df[ja_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_ja

df[top_pages_ja.index].plot(figsize = (16,9));

"""**Popular pages in "fr.wikipedia.org"**"""

fr_wikipedia_org_cols=[column for column in df.columns if "fr.wikipedia.org" in column]

top_pages_fr=df[fr_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_fr

df[top_pages_fr.index].plot(figsize = (16,9));

"""**Popular pages in "zh.wikipedia.org"**"""

zh_wikipedia_org_cols=[column for column in df.columns if "zh.wikipedia.org" in column]

top_pages_zh=df[zh_wikipedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_zh

df[top_pages_zh.index].plot(figsize = (16,9));

"""**Popular pages in "commons.wikipedia.org"**"""

commons_wikimedia_org_cols=[column for column in df.columns if "commons.wikimedia.org" in column]

top_pages_commons=df[commons_wikimedia_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_commons

df[top_pages_commons.index].plot(figsize = (16,9));

"""**Popular pages in "www.mediawiki.org"**"""

mediawiki_org_cols=[column for column in df.columns if "www.mediawiki.org" in column]

top_pages_mediawiki=df[mediawiki_org_cols].mean().sort_values(ascending=False)[0:5]
top_pages_mediawiki

df[top_pages_mediawiki.index].plot(figsize = (16,9));

"""Result- This is all the Web traffic in the websites of wikipedia."""
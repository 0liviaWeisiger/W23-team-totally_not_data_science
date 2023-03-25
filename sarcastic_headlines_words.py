#standard imports
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
from collections import Counter
from wordcloud import WordCloud, STOPWORDS 

# import first dataset
df1 = pd.read_csv("Data.csv")

df1.dropna(inplace=True)
L = [0 for i in range(len(df1['target']))]
df1['headline'] = df1['headlines'].map(str.lower) #convert headlines to lowercase
for i in range(len(df1['target'])):
    if df1['target'][i] == 'Sarcastic':
        L[i] = 1
df1['is_sarcastic'] = L
df1 = df1.drop(columns=['headlines', 'target'], axis = 1)

#import second dataset
l = []
for line in open('Sarcasm_Headlines_Dataset.json', 'r'):
    l.append(json.loads(line))
df2 = pd.DataFrame(l)
df2 = df2.drop('article_link', axis=1)


# combine two dfs to create one big df
frames = [df1, df2]
df = pd.concat(frames)

df["headline"] = df['headline'].str.replace('[^\w\s]','') # remove punctuation



# find most commonly used words in sarcastic and non-sarcastic headlines and remove words if in both

#filter out non-sarcastic headlines from df1
sarcastic = df[df['is_sarcastic']==1]

# count the most commonly used words in the sarcastic headlines col of df1
sarcastic_words = Counter(" ".join(sarcastic["headline"]).split()).most_common(200)

#filter out sarcastic headlines from df1
nonsarcastic = df[df['is_sarcastic']==0]

# count the most commonly used words in the nonsarcastic headlines col of df1
nonsarcastic_words = Counter(" ".join(nonsarcastic["headline"]).split()).most_common(200)

sarcastic_words = dict(sarcastic_words)
nonsarcastic_words = dict(nonsarcastic_words)

# create list of most used words unique to sarcastic headlines 
top_sarcastic_words = list()
for i in sarcastic_words:
    if i not in nonsarcastic_words:
        top_sarcastic_words.append(i)

# create list of most used words unique to non-sarcastic headlines
top_nonsarcastic_words = list()
for i in nonsarcastic_words:
    if i not in sarcastic_words:
        top_nonsarcastic_words.append(i)
        
        
# create dictionary of most used words unique to sarcastic headlines 
D = {}

for i in sarcastic_words:
    for j in top_sarcastic_words:
        if i == j:
            D[i] = sarcastic_words[i]

# convert dict to final dataframe of unique words in sarcastic headlines
freq_df = pd.DataFrame.from_dict(D, orient='index', columns=['Frequency']).reset_index()
freq_df = freq_df.rename(columns={"index": "Word"})
freq_df['Word'][69] = 'f*ck*ng' # censor explicit word

freq_df['Percentage'] = 0

for i in range(len(freq_df)):
    freq_df['Percentage'][i] = freq_df['Frequency'][i]/sum(freq_df['Frequency'])
    

# VISUALIZATION 1
# make frequency chart of most commonly used sarcastic words

# change seaborn plot size
fig = plt.gcf()
fig.set_size_inches(10,8)

sns.set_theme(style="whitegrid")

g = sns.barplot(data=freq_df[:30], 
                y="Word", 
                x="Frequency").set(title='Frequency of Most Commonly Used Words Uniquely in Sarcastic Headlines')


# VISUALIZATION 2
# rough draft; need to replace all common words with uniquely sarcastic common words
wc = WordCloud(background_color="white", width=1200, height=600, max_words=100, relative_scaling=0.5, normalize_plurals=False).generate_from_frequencies(D)
fig = plt.imshow(wc)
fig.axes.get_xaxis().set_visible(False)
fig.axes.get_yaxis().set_visible(False)

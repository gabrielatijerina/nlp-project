import unicodedata
import re
import json

import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd

import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split

import acquire


################ Functions to prepare textual data ################


def basic_clean(string):
    '''
    This function takes in a string and applies basic text cleaning by:
    lowercasing everything,
    normalizing unicode characters,
    replacing anything that is not a letter, number, whitespace, or a single quote
    
    and returns the cleaned string.
    '''
    
    #lowercase
    string = string.lower()
    
    #normalize unicode chars
    string = unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    #replace anything not a letter, number, whitespace
    string = re.sub(r'[^a-z0-9\s]', '', string)
    
    return string



def tokenize(string):
    '''
    This function takes in a string, 
    tokenizes all the words in the string,
    
    and returns the tokenized string.
    '''
    
    #create the tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    
    string = tokenizer.tokenize(string, return_str=True)
    
    return string


def lemmatize(string):
    '''
    This function takes in some text
    
    and returns the text after applying lemmatization to each word.
    '''
    
    #create the lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    
    #use the lemmatizer on each word in the list of words created by using split
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    
    #join lemmatized list of words into a string again
    string_lemmatized = ' '.join(lemmas)
    
    return string_lemmatized



def remove_stopwords(string, extra_words = [], exclude_words = []): 
    '''
    This function takes in a string, 
    optional extra_words (additional stop words),
    and optional exclude_words (words that won't be removed) parameters with default empty lists,
    
    and returns a string after removing all the stopwords.
    '''

    #create stopword_list
    stopword_list = stopwords.words('english')
    
    #remove 'exclude_words' from stopword_list to keep these in my text
    stopword_list = set(stopword_list) - set(exclude_words)
    
    #add in 'extra_words' to stopword_list
    stopword_list = stopword_list.union(set(extra_words))
    
    #split words in string
    words = string.split()
    
    #create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    
    #join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    
    return string_without_stopwords



########################### Clean DF Content Column Function ############################

def clean_content(df, column, extra_words=[], exclude_words=[]):
    '''
    This function takes in a pandas DataFrame, 
    the string name for a text column, 
    with option to pass lists for extra words and exclude words as arguments,
    drops the nulls in the df, 
    adjusts 'jupyter notebook' values to be added to the 'python' language,
    removes languages with less than 9 value counts,

    and returns a df with the GitHub repo, programming language, and the readme_contents 
    cleaned, tokenized, and lemmatized text with stopwords removed.
    '''

    #apply functions to clean up text
    df['clean_content'] = df[column].apply(basic_clean)\
                            .apply(tokenize)\
                            .apply(lemmatize)\
                            .apply(remove_stopwords, 
                                   extra_words=extra_words, 
                                   exclude_words=exclude_words)

    #drop nulls
    df = df.dropna()

    #replace jupyter notebook w/ python
    df.language = df.language.replace('Jupyter Notebook', 'Python')

    #remove languages with 9 or less value_counts
    df = df.groupby('language').filter(lambda x : len(x) >= 5)

    return df[['repo', 'clean_content', column, 'language']]


########################### Split Function ############################

def split(df, stratify_by=None):
    '''
    Crude train, validate, test split
    To stratify, send in a column name
    '''
    
    if stratify_by == None:
        train, test = train_test_split(df, test_size=.2, random_state=123)
        train, validate = train_test_split(train, test_size=.3, random_state=123)
    else:
        train, test = train_test_split(df, test_size=.2, random_state=123, stratify=df[stratify_by])
        train, validate = train_test_split(train, test_size=.3, random_state=123, stratify=train[stratify_by])
    
    return train, validate, test
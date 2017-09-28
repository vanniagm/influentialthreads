import re
import fuzzywuzzy 
from fuzzywuzzy import fuzz
import operator
import pandas as pd

def tagextractor(taglist,N):
    '''Extracts the top N frequent words from the taglist column of the posts dataframe
    where each row is a set of tags such like: ' "street style","streetstyle","fashion" '
    taglist is an array such as df['taglist']
    '''
    #N number of top repeated words
    
    array_tags=[]
#nested list size 20000
    for i,row in enumerate(taglist):
        r=[]
        if not pd.isnull(row):
            s=re.findall(r'"[a-zA-Z\s]*"',row)
            for item in s:
                r.append(re.sub(r'[^a-zA-Z ]','',item))
            array_tags.append(r)
        else:
            array_tags.append('')
#flatten and clean list to search for most frequent
    flatten_tags=[]
    for i,row in enumerate(taglist):
        if not pd.isnull(row):
            s=re.findall(r'"[a-zA-Z\s]*"',row)
            for item in s:
                flatten_tags.append(re.sub(r'[^a-zA-Z ]','',item))
        else:
            flatten_tags.append('')
    # remove the tags I used to find the posts
    flatten=[w for w in flatten_tags if re.search(r'street',w)is None \
             and re.search(r'fashion',w)is None \
             and re.search(r'style',w) is None\
            and re.search(r'fashion',w)is None \
             and re.search(r'wear',w) is None\
             and re.search(r'moda',w) is None\
            and re.search(r'cloth',w) is None\
            and re.search(r'men',w) is None\
            and re.search(r'outfit',w) is None\
             and re.search(r'ootd',w) is None\
            and re.search(r'man',w) is None\
            and re.search(r'male',w) is None\
            and re.search(r'girl',w) is None\
            and re.search(r'woman',w) is None\
            and re.search(r'curvy',w) is None]
     #streetstyle,street_style,mens_wear,menswear,mensfashion,mensfashion,fashion,high_fashion
    ## find similar misspelled words and drop similars before counting
    ## fuzz.token_set_ratio(x,y) compares x and y and gives probability of similarity,
    # >65 are probably the same Proper nouns        
        
    word_counter = {}
    for word in flatten:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    if '' in word_counter:
        del word_counter['']
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    popular_freq=sorted(word_counter.items(), key=operator.itemgetter(1),reverse=True) 
    top = popular_words[:N]
    
    return array_tags, top

def wordextractor(wordlist,N):

    words_list=[row.split() for row in wordlist]
    flatten_words=[item for sublist in words_list for item in sublist]
    flatten=[w for w in flatten_words if re.search(r'street.',w)is None\
             and re.search(r'fashion.',w)is None\
             and re.search(r'style.',w) is None \
             and re.search(r'womenswear. ',w) is None\
            and re.search(r'menswear. ',w) is None]        
  
    word_counter = {}
    for word in flatten:
        if word in word_counter:
            word_counter[word] += 1
        else:
            word_counter[word] = 1
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    popular_freq=sorted(word_counter.items(), key=operator.itemgetter(1),reverse=True) 
    top = popular_words[:N]
    
    return words_list,top,flatten

def freqtags(array_tags,topN):
    freq_tags=[]
    count=0
    for tags in array_tags:
        count=0
        for tag in tags:
            if tag in topN:
                count+=1
        freq_tags.append(count)
    
    return freq_tags
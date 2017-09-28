from bs4 import BeautifulSoup  
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def make_text(x):
    """Concatenate tumblr text fields from post x
    wtitle = include title?
    """
        
    tot_txt = ""

    #Add together various fields based on type:
    if x['type'] == 'text':    
        tot_txt = x['body']
    elif x['type'] == 'photo':
        tot_txt= x['caption']
    elif x['type'] == 'answer':
        tot_txt = x['question'] + x['answer']
    elif x['type'] == 'chat':
        tot_txt = ""#x['text']#""

    #Clean out html:
    soup = BeautifulSoup(tot_txt,'lxml')
        
    return soup.get_text()

def cleaner(x):
    """Clean text x by removing non-alphanumerics and case, and lemmatizing.
    wtitle = include title?
    """
    
    post_txt=make_text(x)

    # Use regular expressions to do a find-and-replace
    letters_only = re.sub("[^a-zA-Z]"," ", post_txt )  # The text to search

    #Lower-bcase"
    lower_case = letters_only.lower()        # Convert to lower case

    #split them up:
    words = lower_case.split(" ")
    str_return=""

    #Lemmatizer!
    wnl = WordNetLemmatizer()

    #Loop over words and lemmatize before re-joining:
    for w in words:
        if (len(w) > 1) and (w not in stopwords.words("english")):
            str_return += wnl.lemmatize(w)
            str_return += " "

    #Encde as ascii:
    return str_return.encode('ascii')

def count(x):
    """Count words in x.
    """
          
    post_txt=make_text(x)

    count = len(re.findall(r'\w+', post_txt))
    return count

def gather_tags(x):
    """Grab tags in x, clean them, and turn them into a list of quoted strings.
    """
        
    tag_txt = ""
    
    for t in x['tags']:
        t = re.sub("[^a-zA-Z ]","", t )
        t = t.lower()  
        words = t.split(" ")
        str_return=""
        wnl = WordNetLemmatizer()
    
        for w in words:
            if (len(w) > 1) and (w not in stopwords.words("english")):
                str_return += wnl.lemmatize(w)
                str_return += " "   

        tag_txt += '"%s",' % str_return
    return tag_txt.encode('ascii')

def count_photos(x):
    """Count photos in x
    """
    count=len(x['photos'])
    return count


def ratio(x):
    """ratio or mean of ratios
    """
    
    ratios=[]
    if len(x['photos']) > 1:
        for i,photo in enumerate(x['photos']):
            ratios.append(float(x['photos'][i]['original_size']['height'])/(x['photos'][i]['original_size']['width']))
        rat=np.mean(ratios)
    elif x['photos']!=' ' :
        rat=float(x['photos'][0]['original_size']['height'])/(x['photos'][0]['original_size']['width'])
        #print x['photos'][0]['original_size']['height']
    else:
        rat=' '
    return rat

    




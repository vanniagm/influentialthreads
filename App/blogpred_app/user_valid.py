
import pytumblr
import requests
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import math

import cleaning 
import cleantags


def Userposts(blog_name,top,tag='streetstyle'):

    consumer_key = 'zl9VsMpQcExcL1DptEqHFYHnmUVgr33wb29ygB6NU2BxYpLKFU'
    consumer_secret = 'aDFAwVWEDtvVA02CY9oe8HiUAoP9LcYVECjvQIG5rAa4RK4yJX'
    oauth_token = 'EkSwbxg1E09rMQWNXUnvOwmKncuwrSF98RuVSVctdbgKATi1Yi'
    oauth_secret = '0Khms8Q0Q6OWSQTARmFHATcTjchcZmGFQYrSbjZhmBKlbFT5jp'
    
    client = pytumblr.TumblrRestClient(consumer_key,consumer_secret, \
        oauth_token, oauth_secret)
    
    #Lists to hold all the posts:
    posts = []
    
    
    
    tgs=['street style','streetstyle','fashion','high fashion','menswear','mens wear','curvy style','streetstyle']

    posts=[]
    response=''
    #count = 0
    #while (count < 3):
    #    try:
    #        temp=client.posts(blog_name,limit=1)
            
    #    except:
    #        temp='Please try again or try with anotheer blog'
    #        response=temp
    #        df=[]
    #        x_test1=[]
    #        x_test2=[]
    #        topN=[]
    #        pass
    #    count+=1
    #    time.sleep(2)
        
    if client.posts(blog_name,limit=1).has_key('response'): #temp.has_key('response'):
        response='This blogger does not exist, try another one!'
        df=[]
        x_test1=[]
        x_test2=[]
        topN=[]
    else:
        if tag!='streetstyle':
            posts=client.posts(blog_name,tag=tag,limit=2)['posts']
        else:
            for tg in tgs:
                posts.append(client.posts(blog_name,tag=tg,limit=2)['posts'])
        if not posts or not [item for sublist in posts for item in sublist]:
            response="This blogger has no fashion related posts"
            df=[]
            x_test1=[]
            x_test2=[]
            topN=[]
        else:
            all_posts=[item for sublist in posts for item in sublist]

            df_all = pd.DataFrame(all_posts)
            df_all = df_all.replace(np.nan,' ', regex=True)
            df = df_all[['id']].copy()
            df.loc[:,'num_photos']=df_all.apply(cleaning.count_photos,axis=1).astype(float)
            df.loc[:,'photo_ratio']=df_all.apply(cleaning.ratio,axis=1)#.astype(float)
            df.loc[:,'words'] = df_all.apply(cleaning.cleaner,axis=1)
            df.loc[:,'wcount'] = df_all.apply(cleaning.count,axis=1).astype(float)
            df.loc[:,'taglist'] = df_all.apply(cleaning.gather_tags,axis=1)
            df.loc[:,'cphotos']=df_all.apply(cleaning.gather_tags,axis=1)
            df.loc[:,'blog_name'] = df_all['blog_name'].astype(str)
            df.loc[:,'note_count'] = df_all['note_count']
            df.loc[:,'note_countlog'] = df['note_count'].transform(lambda x: math.log10(x+1))
            df.loc[:,'short_url'] = df_all['short_url']
            df.loc[:,'date']=df_all['date']
            df.loc[:,'hour']=[pd.to_datetime(item).hour for item in df_all['date']]
            df.loc[:,'type']=df_all['type']
            #clean tags variable and return topN tags and array of lists of tags per post
            array_tags,topN=cleantags.tagextractor(df['taglist'],200)
            # count how many tags for each post belong to the set of frequent tags
            df.loc[:,'freq_tags']=cleantags.freqtags(array_tags,top)#,topN)
            
            dat=pd.to_datetime(df_all['date'])
            dat=dat.sort_values(ascending=False)
            dat=dat.reset_index(drop=True)
            das=(dat.iloc[0]-dat.iloc[-1]).days

            if das<30:
                isfreq=1
            else:
                isfreq=0

            photoset=[]
            for i in range(len(posts)) :
                try :
                    df_all[i]['photoset_layout']
                except KeyError:
                    photoset.append(0)
                else :
                    photoset.append(1)

            x_test1=[]
            x_test2=[]
            x_test1.append(df.loc[0,:]['num_photos'])
            x_test1.append(df.loc[0,:]['photo_ratio'])
            x_test1.append(df.loc[0,:]['wcount'])
            x_test1.append(df.loc[0,:]['hour'])
            x_test1.append(df.loc[0,:]['freq_tags'])
            x_test1.append(isfreq)
            x_test1.append(photoset[0])

            x_test2.append(df.loc[1,:]['num_photos'])
            x_test2.append(df.loc[1,:]['photo_ratio'])
            x_test2.append(df.loc[1,:]['wcount'])
            x_test2.append(df.loc[1,:]['hour'])
            x_test2.append(df.loc[0,:]['freq_tags'])
            x_test2.append(isfreq)
            x_test2.append(photoset[1])




    return df,x_test1,x_test2,response,topN # df.to_csv(fl,index='true')


def Usertags(tag):
    '''Since this is going to compare among different users, this will assume that any input post is from a non frequent user. 
    This feature however is not important for the algorithm 
    '''
    consumer_key = 'zl9VsMpQcExcL1DptEqHFYHnmUVgr33wb29ygB6NU2BxYpLKFU'
    consumer_secret = 'aDFAwVWEDtvVA02CY9oe8HiUAoP9LcYVECjvQIG5rAa4RK4yJX'
    oauth_token = 'EkSwbxg1E09rMQWNXUnvOwmKncuwrSF98RuVSVctdbgKATi1Yi'
    oauth_secret = '0Khms8Q0Q6OWSQTARmFHATcTjchcZmGFQYrSbjZhmBKlbFT5jp'
    
    client = pytumblr.TumblrRestClient(consumer_key,consumer_secret, \
        oauth_token, oauth_secret)
    
    #Lists to hold all the posts:
    posts = []
    
 
    posts=client.tagged(tag, limit=2)
    
    response=''
    if not posts:
        response='There were no posts for this tag'
        df=[]
        x_test1=[]
        x_test2=[]
     
    else: 
        all_posts=[item for sublist in posts for item in sublist]

        df_all = pd.DataFrame(all_posts)
        df_all = df_all.replace(np.nan,' ', regex=True)
        df = df_all[['id']].copy()
        df.loc[:,'num_photos']=df_all.apply(cleaning.count_photos,axis=1).astype(float)
        df.loc[:,'photo_ratio']=df_all.apply(cleaning.ratio,axis=1).astype(float)
        df.loc[:,'words'] = df_all.apply(cleaning.cleaner,axis=1)
        df.loc[:,'wcount'] = df_all.apply(cleaning.count,axis=1).astype(float)
        df.loc[:,'taglist'] = df_all.apply(cleaning.gather_tags,axis=1)
        df.loc[:,'cphotos']=df_all.apply(cleaning.gather_tags,axis=1)
        df.loc[:,'blog_name'] = df_all['blog_name'].astype(str)
        df.loc[:,'note_count'] = df_all['note_count']
        df.loc[:,'short_url'] = df_all['short_url']
        df.loc[:,'date']=df_all['date']
        df.loc[:,'hour']=[pd.to_datetime(item).hour for item in df_all['date']]
        df.loc[:,'type']=df_all['type']

        photoset=[]
        for i in range(len(posts)) :
            try :
                df_all[i]['photoset_layout']
            except KeyError:
                photoset.append(0)
            else :
                photoset.append(1)

        x_test1=[]
        x_test2=[]
        x_test1.append(df.loc[0,:]['num_photos'])
        x_test1.append(df.loc[0,:]['photo_ratio'])
        x_test1.append(df.loc[0,:]['wcount'])
        x_test1.append(df.loc[0,:]['hour'])
        x_test1.append(0)
        x_test1.append(photoset[0])

        x_test2.append(df.loc[1,:]['num_photos'])
        x_test2.append(df.loc[1,:]['photo_ratio'])
        x_test2.append(df.loc[1,:]['wcount'])
        x_test2.append(df.loc[1,:]['hour'])
        x_test2.append(0)
        x_test2.append(photoset[1])



    
    return df,x_test1,x_test2,response # df.to_csv(fl,index='true')
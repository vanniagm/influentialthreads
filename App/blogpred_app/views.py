from flask import render_template
from flask import request
from blogpred_app import app
import pandas as pd
import numpy as np
import psycopg2
import sklearn
from sklearn.externals import joblib
import random
import os
import json
import plotly
from settings import APP_STATIC
from user_valid import Userposts
import makecolormap
import io
import base64
import plotfeat
import plotfeat_hour
import plotfeat_wcount

@app.route('/')
@app.route('/input')
def blog_input():
    return render_template("input.html")


@app.route('/output',methods=['POST'])

def blog_output():
    fil=open(os.path.join(APP_STATIC,'topN.txt'),'r')
    top = fil.read().splitlines()
    blogname=request.form['blog_name']
    #tag=request.form['tag'] #
    #if tag is None:
    #    tag='streetstyle'
    df2=pd.read_csv(os.path.join(APP_STATIC, 'data.csv'))
    df,x_test1,x_test2,response,topN=Userposts(blogname,top)#,tag)#Userposts(blogname)
    if response!='':
        result=response
        url="#"
        the_tags=[]
        
        return render_template('output_noposts.html',the_result=result)
    else:
        url=df['short_url'].iloc[1]
        note_count=df['note_count']
        x_t=np.reshape(x_test1,(1, -1))
        mod = joblib.load(os.path.join(APP_STATIC, 'rfmodel_multi.pkl')) 
        predict=mod.predict(x_t)
        if predict[0]=='NotFollowed':
            result='May not be followed, improve your post to get attention!'
        elif predict[0]=='Followed': 
            result='Your post will be followed'
        else :
            result='Your post will be popular'
        #result indicator colormap
        makecolormap.save_plot(predict[0])
        #graphs with user data overlayed
        hour=df.loc[0,:]['hour']
        ncountlog=df.loc[0,:]['note_countlog']
        aspect=1./df.loc[0,:]['photo_ratio']
        wcoun=df.loc[0,:]['wcount']
        plotfeat.save_plot(predict[0],aspect,df2,'aspect_ratio','/blogpred_app/static/aspect.png')
        plotfeat_hour.save_plot(hour,ncountlog,df2)
        plotfeat_wcount.save_plot(wcoun,ncountlog,df2)
        
        return render_template('output.html', the_result=result,the_url=url,the_tags=topN)#,mimetype='image/png')

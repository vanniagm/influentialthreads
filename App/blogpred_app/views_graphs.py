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

@app.route('/')
@app.route('/input')
def blog_input():
    return render_template("input.html")


@app.route('/output',methods=['POST'])

def blog_output():
    blogname=request.form['blog_name']
    df2=pd.read_csv(os.path.join(APP_STATIC, 'data.csv'))
    df,x_test1,x_test2,response=Userposts(blogname)
    if response!='':
        result=response
        url="#"
    else:
        url=df['short_url'].iloc[1]
        note_count=df['note_count']
        x_t=np.reshape(x_test1,(1, -1))
        mod = joblib.load(os.path.join(APP_STATIC, 'rfmodel_multi.pkl')) 
        predict=mod.predict(x_t)
        if predict[0]=='NotFollowed':
            result='Improve your post to get attention!'
        elif predict[0]=='Followed': 
            result='Your post will be followed'
        else :
            result='Your post will be popular'
            
    

    graphs = [

        dict(
            data=[
                dict(
                    x=df2['hour'],  # Can use the pandas data structures directly
                    y=df2['note_countlog'],
                    type='bar'
                )
            ],
            layout=dict(
                title='Log(Note counts) vs Hour of the day'
            )
        ),
        dict(
            data=[
                dict(
                    x=df2['aspect_ratio'],
                    y=df2['note_countlog'],
                    mode='markers',
                    type='scatter'
                ),
            ],
            layout=dict(
                title='Log(Note counts) vs Aspect ratios'
            )
        ),
        dict(
            data=[
                dict(
                    x=df2['freq_tags'],  # Can use the pandas data structures directly
                    y=df2['note_countlog'],
                    type='bar'
                )
            ],
            layout=dict(
                title='Log(Note counts) vs Number of most frequent tags'
            )
        )
    ]

    # Add "ids" to each of the graphs to pass up to the client
    # for templating
    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]

    # Convert the figures to JSON
    # PlotlyJSONEncoder appropriately converts pandas, datetime, etc
    # objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('output.html', the_result=result, the_url=url,
                           ids=ids,
                           graphJSON=graphJSON)

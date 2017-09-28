
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import os


def make_plot(userx,usery,filename,df):

    df=df.sample(frac=0.01, replace=False)

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 9
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size
    plt.subplots_adjust(left=0,right=1, top=0.8, bottom=0.1)
    plt.rcParams.update({'font.size': 21})

    font = {'family': 'sans-serif',
                    'color':  'black',
                    'weight': 'normal',
                    'size': 16,
                    }
    pink0='#a50b5e'

    x=df['wcount'].reset_index(drop=True)
    y=df['note_countlog'].reset_index(drop=True)

    fig, ax = plt.subplots()
    ax.scatter(x, y,  color=pink0)

    #plt.bar(x,y,color=pink0)
    #ax = plt.gca()
    ax.set_title('')
    ax.set_xlabel('Word counts',color='white')
    ax.set_ylabel('Note count (log10)',color='white')


    el = Ellipse((2, -1), 0.5, 0.5)
    ax.add_patch(el)
    ann = ax.annotate('X',xy=(userx, usery),size=14, color='white',va="center",ha="left",
                                  bbox=dict(boxstyle="round", fc=pink0, ec="k"),
                                  arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                                  fc=pink0, ec="k",
                                                  patchA=None,
                                                  patchB=el,
                                                  relpos=(0, 0.5)))

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')



    plt.savefig(filename,transparent=True, box_inches='tight',dpi=800)

    
###################3

def save_plot(user_result,yval,df):
    
    
    
    dir_path=os.getcwd()
    filename = dir_path+'/blogpred_app/static/wcount.png' #/blogpred_app/static/indicator.png'

    make_plot(user_result,yval,filename,df)

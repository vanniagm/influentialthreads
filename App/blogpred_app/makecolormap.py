
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.ticker as mtick
import os
import io
import base64

def make_plot(user_result,filename):
    '''Creates colormap and annotates over the result of the app prediction over three values.
    Edited from Jamie Antonelli visualizations.py for silvertongue app.
    '''

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 15
    fig_size[1] = .7
    plt.rcParams["figure.figsize"] = fig_size
    plt.subplots_adjust(left=0,right=1, top=0.8, bottom=0.1)
    plt.rcParams.update({'font.size': 21})


    font = {'family': 'sans-serif',
            'color':  'white',
            'weight': 'normal',
            'size': 28,
            }

    weights=[[0],[33],[37],[100]]
    data = [[1] for weight in weights]

    pink0='#a50b5e'
    pink1='#a50b5e'
    pink2='#e30b5c'
    pink3='#ff355e'
    colors=[pink0,pink1,pink2,pink3]

    plt.hist(data, weights = weights, bins=1, color=colors,orientation="horizontal", stacked=True)
    ax = plt.gca()
    ax.set_xlim(0,100)
    ax.set_ylim(0.8,1.2)
    ax.get_yaxis().set_visible(False)
    plt.xticks([0,33,70,100])
    plt.text(10,.9, r'Not Followed',fontdict=font)
    plt.text(45,.9, r'Followed',fontdict=font)
    plt.text(80,.9, r'Popular',fontdict=font)
    #fig, ax = plt.subplots()
    plt.xlabel('Note counts',fontdict=font)

    labels = [item.get_text() for item in ax.get_xticklabels()]
    labels[1] = 1
    labels[2]=11

    ax.set_xticklabels(labels,fontdict=font)


    index=0
    if user_result =='NotFollowed':
        placement = 10.
        index=1
    elif user_result=='Followed' :
        placement = 45.
        index=2
    elif user_result=='Popular':
        placement =80.
        index=3


    display_color = colors[index]


    el = Ellipse((2, -1), 0.5, 0.5)
    ax.add_patch(el)
    ann = ax.annotate('X',xy=(placement, 1), xycoords='data',
                          xytext=(-33, 0), textcoords='offset points',
                          size=35, color='white',va="center",ha="left",
                          bbox=dict(boxstyle="round", fc=display_color, ec="k"),
                          arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                          fc=display_color, ec="k",
                                          patchA=None,
                                          patchB=el,
                                          relpos=(0, 0.5)))
    ax.tick_params(axis='x', which='major', pad=12)
    #filename=io.BytesIO()
    plt.savefig(filename, transparent=True, bbox_inches='tight',dpi=800)
    plt.clf()
    #filename.seek(0)
    #img_png = filename.getvalue()
    #return base64.b64encode(img_png)
###############################################

def save_plot(user_result):
    
    
    
    dir_path=os.getcwd()
    filename = dir_path+'/blogpred_app/static/indicator.png'

    make_plot(user_result,filename)

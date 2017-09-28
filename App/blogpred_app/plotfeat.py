
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import os


def make_plot(user_result,yvalue,filename,df,coldf):

    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 9
    fig_size[1] = 7
    plt.rcParams["figure.figsize"] = fig_size
    plt.subplots_adjust(left=0,right=1, top=0.8, bottom=0.1)
    plt.rcParams.update({'font.size': 21})

    userx=user_result
    userya=yvalue
    if userx=='NotFollowed':
        annx=0.9
    elif userx=='Followed':
        annx=1.98
    elif userx=='Popular':
        annx=2.9


    font = {'family': 'sans-serif',
                'color':  'black',
                'weight': 'normal',
                'size': 16,
                }
    pink0='#a50b5e'

    # multiple box plots on one figure
    fig, ax = plt.subplots()

    boxprops = dict(linewidth=2,color='white')
    medianprops = dict(linestyle='-', linewidth=3,color='white')
    df.boxplot(ax=ax,column=coldf, by='Popularity',boxprops=boxprops,
                    medianprops=medianprops)

    ax.set_title('')
    ax.set_xlabel('')
    plt.ylabel('Aspect ratios',color='white')
    ax.set_xticklabels(['NotFollowed','Followed','Popular'],fontdict=font)


    el = Ellipse((2, -1), 0.5, 0.5)
    ax.add_patch(el)
    ann = ax.annotate('X',xy=(annx, userya),size=11, color='white',va="center",ha="left",
                              bbox=dict(boxstyle="round", fc=pink0, ec="k"),
                              arrowprops=dict(arrowstyle="wedge,tail_width=1.",
                                              fc=pink0, ec="k",
                                              patchA=None,
                                              patchB=el,
                                              relpos=(0, 0.5)))
    #ann = ax.annotate('User',xy=(annx, usery))

    fig.suptitle('')

    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.label.set_color('white')

    plt.savefig(filename,transparent=True, box_inches='tight',dpi=800)
    plt.clf()
    
############################
def save_plot(user_result,yval,df,coldf,namefile):
    
    
    
    dir_path=os.getcwd()
    filename = dir_path+namefile #/blogpred_app/static/indicator.png'

    make_plot(user_result,yval,filename,df,coldf)
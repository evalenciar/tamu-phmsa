# -*- coding: utf-8 -*-
"""
Data Plotting

Plot the results of the predictions. Use various methods of multi-dimensional
plotting, such as seaborn.pairplot(), t-SNE, overlapped scatter plots.
"""

import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# DATA ANALYSIS: PLOTTING
# =============================================================================

def hist(data, df):

    # Plot a Histogram of the PART_LIFETIME
    hist_data = data['LIFE_INSTALLED']
    
    n, bins, patches = plt.hist(x=hist_data, bins='auto', color='#0504aa', 
                                alpha=0.75, rwidth=0.9)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Lifetime from Installation')
    plt.ylabel('Frequency')
    plt.title('Detection Time Histogram')
    # plt.text(23, 60, r'$\mu=15, b=3$')
    # maxfreq = n.max()
    # Set a clean upper y-axis limit
    # plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    # plt.xlim(xmax=np.ceil(maxfreq / 5) * 5 if maxfreq % 5 else maxfreq + 5)
    
def scatter_matrix(data, df):
    # Scatter Plots: Observe the change in PART_LIFETIME
    # fig2, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2, sharey=True, figsize=(10,8))
    fig2, axs = plt.subplots(2,2, 
                             # sharey=True, 
                             figsize=(10,8))
    fig2.suptitle('Variables vs Part Lifetime in Years', fontsize=24)
    y_val = 'LIFE_INSTALLED'
    x_val = ['PIPE_DIAMETER',
             'PIPE_WALL_THICKNESS',
             'PIPE_SMYS']
    # x_val = [variables[8],
    #          variables[9],
    #          variables[10]]
    s = 2
    c = ['blue','red','green','orange']
    label = ['PIPE_DIAMETER',
             'PIPE_WALL_THICKNESS',
             'PIPE_SMYS']
    # label = [variables[8],
    #          variables[9],
    #          variables[10]]
    # xlim = np.array([[0,0,0,0],[500,500,20,1]])
    
    j = 0
    k = 0
    for i in range(len(x_val)):
        if i == 2:
            j += 1
            k -= 2
        axs[j,k].scatter(x=np.array(data[x_val[i]]),
                         y=np.array(data[y_val]),
                         s=s,
                         c=c[i],
                         label=label[i])
        # axs[j,k].set_xlim(xlim[:,i])
        axs[j,k].set_ylabel('Part Lifetime [years]')
        axs[j,k].legend()
        axs[j,k].grid()
        k += 1
        
    # Combined in one plt
    # x_val = 'LIFE_INSTALL'
    # y1_val = 'MAX_ALLOWABLE_PRESSURE'
    # y2_val = 'ESTIMATE_INCIDENT_PRESSURE'
    # plt.scatter(x=np.array(data[x_val]),y=np.array(data[y1_val]), s=0.75, c='blue')
    # plt.scatter(x=np.array(data[x_val]),y=np.array(data[y2_val]), s=0.75, c='red')
    # plt.ylim([0, 100])
    # plt.show()
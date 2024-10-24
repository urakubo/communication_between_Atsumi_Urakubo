import os, sys, glob, pickle
import numpy as np

import src.utils as u
import src.utils_graph as u_graph
import configuration as c

import matplotlib.pyplot as plt

# Matplotlib
plt.rcParams.update( c.rc_param )

def plot_Ith_timing_dependence(dist_ids, p):
    #'''	
    ctl  = p['stim_types'][1]
    targ = p['stim_types'][2]
    Iths_ctl   = {}
    Iths_targ  = {}
    Iths_delay = {}
    for dist_id in dist_ids:
        filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode )
        input_amp, v_apic_max, input_amp_th = u.load(filename_data)
        Iths_ctl[dist_id]  = list(input_amp_th[ctl].values())[0]
        Iths_targ[dist_id] = list(input_amp_th[targ].values())
        Iths_delay[dist_id] = list(input_amp_th[targ].keys())
    
    
    dir_imgs = p['dir_imgs']
    filename = 'test'

    y_lim = [-35, 35]

    nrows = len( dist_ids )
    ncols = 1
    fig, axes= plt.subplots(nrows, ncols, figsize=(5.0, 10.0))
    left, right, bottom, top = 0.15, 0.9, 0.1, 0.9
    wspace, hspace = 0.2, -0.02
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
    for i, dist_id in enumerate( dist_ids ):
        row  = nrows - i - 1
        ax = axes[row]
        Ith_ctl  = Iths_ctl[dist_id]
        Ith_targ = Iths_targ[dist_id]
        delays   = Iths_delay[dist_id]
        x_lim = [np.min(delays)*1.1, np.max(delays)*1.1]
        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_yticks([-20,0,20])
        ax.set_title('{:.0f} um'.format(p['dists'][dist_id]), loc='right', y = 0.6)
        
        if row != nrows - 1:
            ax.spines['bottom'].set_visible(False)
            ax.axes.xaxis.set_ticklabels([])
            ax.set_xticks([])
        else:
            ax.set_xlabel('T(start,Idend)- T(end,Isoma) (ms)')

        #ax.set_xlabel('T(start,Idend)- T(end,Isoma) (ms)')
	#ax.set_ylabel('(Ith_targ - Ith_ctl)/Ith_ctl (%)')
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.plot(x_lim,[0, 0], 'k:')
        ax.plot( delays, (Ith_targ - Ith_ctl)/Ith_ctl * 100,
				'o-', markersize=5, color='k', markerfacecolor='k', markeredgecolor="k" )

    plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
    plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
    plt.show(block=False)
    plt.pause(2)
    plt.close()
    

def init_panel_rows(axes, row, dist, x_lim, y_lim, yticks, xlabel = 'Time (ms)' ):
    ax = axes[row]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_yticks( yticks )
    ax.set_title('{:.0f} um'.format(dist), loc='right', y = 0.6)
    ax.set_xlim(x_lim)
    ax.set_ylim(y_lim)
    if row != axes.shape[0]-1:
        ax.spines['bottom'].set_visible(False)
        ax.axes.xaxis.set_ticklabels([])
        ax.set_xticks([])
    else:
        ax.set_xlabel(xlabel)
    return ax
            
    
if __name__ == "__main__":
	
	
    mode    = 'sic' # 'sic', 'bac', 'ttx'
    dist_id = 0     # 0, ..., 11
    num_cpu = 32
    p = c.set_params(mode, dist_id)

    '''
    dist_ids = list(range(2,12))
    plot_Ith_timing_dependence(dist_ids, p)
    '''
    
    dist_ids = list(range(0,12))
    filename = 'membrane_pot'    
    dir_imgs    = p['dir_imgs']
    dir_data    = p['dir_data']
    time_prerun = p['time_prerun'] + 150
    time_run    = p['time_run_after_prerun'] -150

    t      = {}
    v_dend = {}
    for dist_id in dist_ids:
        filename_data   = dir_data + os.sep + \
            'distid{}_stimtype_soma_only_dend_Idelay0_dend_Iamp0.00'.format(dist_id)
        data            = u.load(filename_data)
        t[dist_id]      = data['t']
        v_dend[dist_id] = data['v_apic']
    t_soma = data['t']
    v_soma = data['v_soma']

    y_lim = [-110, -60]
    x_lim = [-50 -150, time_run]
    yticks= [-100, -90, -80,-70]
    nrows = len( dist_ids ) + 1
    ncols = 1
    fig, axes= plt.subplots(nrows, ncols, figsize=(5.0, 10.0))
    left, right, bottom, top = 0.15, 0.9, 0.1, 0.9
    wspace, hspace = 0.2, -0.02
    #wspace, hspace = 0.2, 0.02
    plt.subplots_adjust(left, bottom, right, top, wspace, hspace)
    for i, dist_id in enumerate( dist_ids ):
        row  = nrows - i - 2
        dist = p['dists'][dist_id]
        ax = init_panel_rows(axes, row, dist, x_lim, y_lim, yticks)
        v_dend_end = v_dend[dist_id][-1]
        ax.plot(x_lim, [v_dend_end, v_dend_end], 'k:')
        ax.plot( t[dist_id]-time_prerun, v_dend[dist_id],'k-', linewidth =1 )

    row  = nrows - 1
    dist = 0
    ax = init_panel_rows(axes, row, dist, x_lim, y_lim, yticks)
    v_dend_end = v_soma[-1]
    ax.plot( x_lim, [v_dend_end, v_dend_end], 'k:' )
    ax.plot( t_soma-time_prerun, v_soma,'k-', linewidth =1 )
    
    
    plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
    plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
    #plt.show(block=False)
    #plt.pause(2)
    plt.show()
    plt.close()
    


    '''
    for dist_id in range(2,12):
        p  = c.set_params(mode, dist_id)
        filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode )
        input_amp, v_apic_max, input_amp_th = u.load(filename_data)
        u_graph.plot_Ith_for_V_timing_dependence(input_amp_th, p)
    '''


import os, sys, glob, pickle
import numpy as np

import src.utils as u
import src.utils_graph as u_graph
import configuration as c

import matplotlib.pyplot as plt

# Matplotlib
plt.rcParams.update( c.rc_param )


    
class PanelStackingHandler():
    def init_panel(self, row, dist):
        ax = self.axes[row]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_yticks( self.yticks )
        ax.set_title('{:.0f} um'.format(dist), loc='right', y = 0.6)
        ax.set_xlim(self.x_lim)
        ax.set_ylim(self.y_lim)
        if row != self.axes.shape[0]-1:
            ax.spines['bottom'].set_visible(False)
            ax.axes.xaxis.set_ticklabels([])
            ax.set_xticks([])
        else:
            ax.set_xlabel(self.xlabel)
        return ax
            
    def __init__(self, p, dist_ids):
        self.p = p
        self.dist_ids = dist_ids
        self.nrows = len( dist_ids )
        self.wspace, self.hspace = 0.2, -0.02
        self.figsize = (5.0, 10.0)
        self.nrows_add_bottom = 0
        
    def create_fig(self):
        self.fig, self.axes= plt.subplots( self.nrows + self.nrows_add_bottom, 1, figsize=self.figsize )
        left, right, bottom, top = 0.15, 0.9, 0.1, 0.9
        plt.subplots_adjust(left, bottom, right, top, self.wspace, self.hspace)
        self.preprocessing()
        for i, dist_id in enumerate( self.dist_ids ):
            row = self.nrows - i - 1
            dist = p['dists'][dist_id]
            ax = self.init_panel(row, dist)
            self.plot_panel(ax, dist_id)
        self.postprocessing()
        
        dir_imgs = p['dir_imgs_summary']
        os.makedirs(dir_imgs, exist_ok=True)
        u_graph.savefig_showfig(self.filename, dir_imgs)
                
    def preprocessing(self):
        pass
    def plot_panel(self, ax):
        pass
    def postprocessing(self):
        pass


class PlotIthresholdTimingDistanceDependence(PanelStackingHandler):
    def load_data(self, p, dist_ids, time_prerun):
        ctl  = p['stim_types'][1]
        targ = p['stim_types'][2]
        Iths_ctl   = {}
        Iths_targ  = {}
        Iths_delay = {}
        for dist_id in dist_ids:
            filename_data = p['dir_data'] + os.sep + 'distid_{}_mode_{}'.format(dist_id, mode)
            input_amp, v_apic_max, input_amp_th = u.load(filename_data)
            Iths_ctl[dist_id]  = list(input_amp_th[ctl].values())[0]
            Iths_targ[dist_id] = list(input_amp_th[targ].values())
            Iths_delay[dist_id] = list(input_amp_th[targ].keys())
        return Iths_ctl, Iths_targ, Iths_delay
        
    def __init__(self, p):
        dist_ids = list(range(2,12))
        PanelStackingHandler.__init__(self, p, dist_ids)
        time_prerun = p['time_prerun'] + 150
        time_run    = p['time_run_after_prerun'] -150
        self.Iths_ctl, self.Iths_targ, self.Iths_delay = self.load_data(p, dist_ids, time_prerun)
        
        self.xlabel = 'Time (ms)'
        self.y_lim  = [-35, 35]
        self.x_lim  = [-85, 85]
        self.yticks = [-20, 0, 20]
        self.filename = 'timing_distance_dependence_i_threshold'
  
    def plot_panel(self, ax, dist_id):
        Ith_ctl  = self.Iths_ctl[dist_id]
        Ith_targ = self.Iths_targ[dist_id]
        delays   = self.Iths_delay[dist_id]
        ax.plot(self.x_lim,[0, 0], 'k:')
        ax.plot( delays, (Ith_targ - Ith_ctl)/Ith_ctl * 100,
		 'ko-',
                 markersize=5,
                 markerfacecolor='k',
                 markeredgecolor="k" )


class PlotSomaticHyperpolarization(PanelStackingHandler):
    def load_data(self, p, dist_ids, time_prerun):
        t_dend = {}
        v_dend = {}
        for dist_id in dist_ids:
            filename_data   = p['dir_data'] + os.sep + \
                'distid{}_stimtype_soma_only_dend_Idelay0_dend_Iamp0.00'.format(dist_id)
            data            = u.load(filename_data)
            t_dend[dist_id] = data['t'] - time_prerun
            v_dend[dist_id] = data['v_apic']
        t_soma = data['t'] - time_prerun
        v_soma = data['v_soma']
        return t_dend, v_dend, t_soma, v_soma

    def __init__(self, p):
        dist_ids = list(range(0,12))
        PanelStackingHandler.__init__(self, p, dist_ids)
        time_prerun = p['time_prerun'] + 150
        time_run    = p['time_run_after_prerun'] -150
        self.t_dend, self.v_dend, self.t_soma, self.v_soma = self.load_data(p, dist_ids, time_prerun)
        
        self.xlabel = 'Time (ms)'
        self.y_lim  = [-110, -60]
        self.x_lim  = [-50 -150, time_run]
        self.yticks = [-100, -90, -80,-70]
        self.nrows_add_bottom = 1
        self.filename = 'membrane_pot_somatic_inhibition'
        
    def plot_panel(self, ax, dist_id):
        v_dend_end = self.v_dend[dist_id][-1]
        ax.plot(self.x_lim, [v_dend_end, v_dend_end], 'k:')
        ax.plot(self.t_dend[dist_id], self.v_dend[dist_id],'k-', linewidth = 1 )
        
    def postprocessing(self):
        row  = self.axes.shape[0]-1
        dist = 0
        ax = self.init_panel(row, dist)
        v_soma_end = self.v_soma[-1]
        ax.plot( self.x_lim, [v_soma_end, v_soma_end], 'k:' )
        ax.plot( self.t_soma, self.v_soma, 'k-', linewidth =1 )
        
        
    
if __name__ == "__main__":
	
	
    mode    = 'sic' # 'sic', 'bac', 'ttx'
    dist_id = 0     # 0, ..., 11
    num_cpu = 32
    p = c.set_params(mode, dist_id)

    #g1 = PlotSomaticHyperpolarization(p)
    #g1.create_fig()
    
    g2 = PlotIthresholdTimingDistanceDependence(p)
    g2.create_fig()
    

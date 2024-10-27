import os, sys, glob, pickle
import numpy as np


import src.utils as u
import configuration as c

import matplotlib.pyplot as plt

# Matplotlib
plt.rcParams.update( c.rc_param )



def savefig_showfig(filename, dir_imgs = ''):
	plt.savefig(os.path.join(dir_imgs, filename + '.pdf'))
	plt.savefig(os.path.join(dir_imgs, filename + '.png'), dpi=300)
	plt.show(block=False)
	plt.pause(0.1)
	plt.close()
	
	
	
def plot_profile(filename, recs, p, i_delay):
	
	time_prerun = p['time_prerun']
	time_run    = p['time_run_after_prerun']
	dist        = p['dist']
	time_set_zero = p['time_prerun'] + p['i_soma_duration']
	
	## Preparation of plot panels
	height_ratios = [1,1,3,3]
	nrows = len(height_ratios)
	fig   = plt.figure(constrained_layout=True, figsize=(4.0, 8.0))
	spec  = fig.add_gridspec(ncols=1, nrows=nrows, height_ratios=height_ratios)
	axs   = [fig.add_subplot(spec[i, 0]) for i in range(nrows)]
	fig.suptitle(  'Distance from soma: {:.0f} um\nT(start,Idend)- T(end,Isoma) = {} ms'.format(
                dist, str(i_delay)) )
	
	#xmin = -150 # -time_prerun
	#xmax = time_run -100
	x_lim  = [-200, 200]
	
	titles  = ['Current injection (dend)',
		  'Current injection (soma)',
		  'Membrane potential (dend)',
		  'Membrane potential (soma)'
		 ]
	ylabels = ['(nA)',
                   '(nA)',
                   'Membrane pot (mV)',
                   'Membrane pot (mV)'
		 ]
	y_lims   = [[-0.1, 1.1],
                   [-0.8, 0.2],
                   [-120, 60],
                   [-120, 50]
		 ]
	yticks = [[0,1],
                  [-0.5,0],
                  np.arange(-100, 60, 40),
                  np.arange(-100, 60, 40)
		 ]

	for i in range(4):
		ax = axs[i]
		ax.set_title(titles[i])
		ax.set_xlabel('Time (ms)')
		ax.set_ylabel(ylabels[i])
		ax.set_xlim(x_lim)
		ax.set_ylim(y_lims[i])
		ax.set_yticks(yticks[i])
        
	
	cmap     = plt.get_cmap("jet")
	#cmap = plt.get_cmap("Blues")
	cmap_max = len(recs.keys())
	lw   = 0.5	
	for i, v in enumerate(recs.values()):
		#print(i)
		col = cmap( int(i) / cmap_max )
		axs[0].plot(v['t'] - time_set_zero, v['i_dend'], color=col, linewidth = lw )
		axs[1].plot(v['t'] - time_set_zero, v['i_soma'], color=col, linewidth = lw )
		axs[2].plot(v['t'] - time_set_zero, v['v_apic'], color=col, linewidth = lw )
		axs[3].plot(v['t'] - time_set_zero, v['v_soma'], color=col, linewidth = lw )
	
	savefig_showfig(filename)
	
	
class PlotProfiles(u.RepeatHandler):
	def __init__(self, p):
		u.RepeatHandler.__init__(self, p)
	def preprocessing_dend_amp(self):
		self.recs = {}
		self.i   = 0
		# print("self.p['i_dend_amps'][self.stim_type]", self.p['i_dend_amps'][self.stim_type])
	def function(self):
		self.recs[self.i]   = u.load(self.get_filename_simdata())
		self.i += 1
		# print('i ', self.i)
	def postprocessing_dend_amp(self):
		#pprint.pprint(self.recs)
		plot_profile(self.get_filename_fig(), self.recs, self.p, self.i_dend_delay )


class PlotIforSpike():
	def __init__(self, input_amp, v_apic_max, p):
		self.ctl      = p['stim_types'][1]
		self.targ     = p['stim_types'][2]
		self.dist     = p['dist']
		self.Vth      = p['Vth']
		self.dir_imgs = p['dir_imgs']
		self.dir_imgs_summary = p['dir_imgs_summary']
		self.dist_id  = p['dist_id']
		self.delays   = p['i_dend_delays'][self.targ]
		self.p        = p

		self.ctl_v_apic_max  = np.array( v_apic_max[ self.ctl ][0] ) # 'dend_only'
		self.targ_v_apic_max = v_apic_max[ self.targ ] # 'sic'/'bac'
		self.i_dend = np.array(input_amp[ self.ctl ][0]) * 1000
	
	def plot_a_panel(self, ax, i_delay, type):
		if type == 'large':
			ax.set_xlabel('Dendritic I (pA)')
			ax.set_ylabel('Peak V (mV)')
			markersize = 5
		elif type == 'small':
			ax.set_title('{:.0f} ms'.format(i_delay) )
			ax.set_xlabel('Dend I (pA)')
			markersize = 2
		
		ax.plot( self.i_dend, self.ctl_v_apic_max, 'ko-',
				markersize=markersize,
				markerfacecolor='w',
				markeredgecolor="k",
				markeredgewidth=1,
				label = self.ctl)
		ax.plot( self.i_dend, np.array( self.targ_v_apic_max[i_delay] ), 'ko-',
				markersize=markersize, 
				markerfacecolor='k', 
				markeredgecolor="k",
				markeredgewidth=1,
				label = self.targ)
		ax.plot( [np.min(self.i_dend), np.max(self.i_dend)], [self.Vth, self.Vth], 'r-' )
		ax.set_ylim([-80, 40])
		ax.set_box_aspect(1)

        
	def repeat_plots(self):
		p = self.p
		for i_delay in self.delays:
			fig = plt.figure(constrained_layout=True, figsize=(3.0, 3.0))
			fig.suptitle('Distance from soma {:.0f} um\nT(start,Idend)- T(end,Isoma) = {} ms'.\
                                       format(self.dist, str(i_delay) ) )
			ax = fig.add_subplot()
			self.plot_a_panel(ax, i_delay, type = 'large')
			ax.legend()
			filename =  'distid{}_delay{}_i_v'.format( self.dist_id, str(i_delay).replace('-','m') )
			savefig_showfig(filename, self.dir_imgs)
		
	def plot_delays(self):
		nrows = 1
		ncols = len( self.delays )
		fig, axes= plt.subplots(nrows, ncols, figsize=(20.0, 2.5))
		fig.suptitle( 'Distance from soma: {:.0f} um'.format(self.dist) )
		for i, i_delay in enumerate( self.delays ):
			ax = axes[i]
			self.plot_a_panel(ax, i_delay, type = 'small' )
			if i == 0:
				ax.set_ylabel('Dend peak V (mV)')
			else:
				ax.axes.yaxis.set_ticklabels([])
		
		filename =   'distid{}_i_v'.format( self.dist_id )
		savefig_showfig(filename, self.dir_imgs_summary)


def plot_timing_dependent_i_for_spike(input_amp_th, p):
	
	Vth      = p['Vth']
	dist     = p['dist']
	dir_imgs = p['dir_imgs']
	dist_id  = p['dist_id']
	
	ctl     = p['stim_types'][1]
	sic_bac = p['stim_types'][2]
	Ith_ctl  = input_amp_th[ ctl ][0] # 'dend_only'
	Ith_targ = np.array(list(input_amp_th[ sic_bac ].values()))
	delays   = np.array(list(input_amp_th[ sic_bac ].keys()))

	print('Ith_ctl : ', Ith_ctl )
	print('Ith_targ: ', Ith_targ )
	print('delays  : ', delays )
	
	x_lim = [np.min(delays)*1.1, np.max(delays)*1.1]
	y_lim = [-80, 80]
	fig = plt.figure(constrained_layout=True, figsize=(5.0, 3.0))
	ax = fig.add_subplot()
	ax.set_xlabel('T(start,Idend)- T(end,Isoma) (ms)')
	ax.set_ylabel('(Ith_targ - Ith_ctl)/Ith_ctl (%)')
	ax.set_xlim(x_lim)
	ax.set_ylim(y_lim)
	fig.suptitle( 'Distance from soma: {:.0f} um, Ith: {:.0f} pA (ctl)'.format(dist, Ith_ctl) )
	
	ax.plot(x_lim,[0, 0], 'k:')
	ax.plot( delays, (Ith_targ - Ith_ctl)/Ith_ctl * 100,
				'o-', markersize=5, color='k', markerfacecolor='k', markeredgecolor="k" )
	
	filename = 'dist_{}_timing_dependent_i_for_spike'.format( dist_id )
	savefig_showfig(filename, dir_imgs)
        
	
def plot_distance_Ih(dir_imgs, func, label):
	
	maxLength = 1300.53
	dist = np.linspace(0,maxLength,100)
	
	fig = plt.figure(constrained_layout=True, figsize=(4.0, 3.0))
	ax  = fig.add_subplot()
	ax.set_xlabel('Distance from soma (um)')
	ax.set_ylabel('gIhbar_Ih (mA/cm2)')
	
	# Control
	x3, x4, x5, x6, x7 = -0.8696, 3.6161, 0.0, 2.0870, 0.0001
	Ih  = x3 + x6*np.exp(x4*(dist/maxLength-x5))
	Ih *= x7
	
	ax.plot(dist, Ih, 'k-',label='control')
	ax.plot(dist, func(dist), 'r-',label=label)
	ax.legend()
	
	filename = 'distrib_Ih'
	savefig_showfig(filename, dir_imgs)
	
	
	

